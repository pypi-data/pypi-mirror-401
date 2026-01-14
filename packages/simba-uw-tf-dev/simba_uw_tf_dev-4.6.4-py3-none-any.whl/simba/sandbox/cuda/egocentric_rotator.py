import functools
import multiprocessing
import os
from typing import Optional, Tuple, Union

import cv2
import numpy as np

try:
    import cupy as cp
    from cupyx.scipy.ndimage import affine_transform
    CUPY_AVAILABLE = True
except ImportError:
    import numpy as cp
    from scipy.ndimage import affine_transform
    CUPY_AVAILABLE = False

from simba.utils.checks import (check_file_exist_and_readable,
                                check_if_dir_exists, check_if_valid_rgb_tuple,
                                check_int, check_valid_array,
                                check_valid_boolean, check_valid_tuple)
from simba.utils.data import (align_target_warpaffine_vectors,
                              center_rotation_warpaffine_vectors,
                              egocentrically_align_pose)
from simba.utils.enums import Defaults, Formats
from simba.utils.printing import SimbaTimer, stdout_success
from simba.utils.read_write import (concatenate_videos_in_folder,
                                    create_directory, find_core_cnt,
                                    get_fn_ext, get_video_meta_data, read_df,
                                    read_frm_of_video,
                                    read_img_batch_from_video_gpu,
                                    remove_a_folder,
                                    _read_img_batch_from_video_helper)


def egocentric_video_aligner(frm_range: np.ndarray,
                             video_path: Union[str, os.PathLike],
                             temp_dir: Union[str, os.PathLike],
                             video_name: str,
                             centers: np.ndarray,
                             rotation_vectors: np.ndarray,
                             target: Tuple[int, int],
                             fill_clr: Tuple[int, int, int] = (255, 255, 255),
                             verbose: bool = False,
                             gpu: bool = True):

    video_meta = get_video_meta_data(video_path=video_path)

    batch, frm_range = frm_range[0], frm_range[1]
    save_path = os.path.join(temp_dir, f'{batch}.mp4')
    fourcc = cv2.VideoWriter_fourcc(*f'{Formats.MP4_CODEC.value}')
    writer = cv2.VideoWriter(save_path, fourcc, video_meta['fps'], (video_meta['width'], video_meta['height']))
    batch_rotation_vectors = rotation_vectors[frm_range[0]: frm_range[-1]+1]
    batch_centers = centers[frm_range[0]: frm_range[-1]+1]
    m_rotates = center_rotation_warpaffine_vectors(rotation_vectors=batch_rotation_vectors, centers=batch_centers)
    m_translations = align_target_warpaffine_vectors(centers=batch_centers, target=np.array(target))

    if gpu:
        # Combine rotation and translation matrices into single transform
        # This reduces two sequential operations to one
        batch_size = len(frm_range)
        m_combined = np.zeros((batch_size, 2, 3), dtype=np.float32)
        
        for i in range(batch_size):
            # Convert rotation matrix (2x3) to 3x3 homogeneous
            m_rot_3x3 = np.eye(3, dtype=np.float32)
            m_rot_3x3[:2, :] = m_rotates[i].astype(np.float32)
            
            # Convert translation matrix (2x3) to 3x3 homogeneous
            m_trans_3x3 = np.eye(3, dtype=np.float32)
            m_trans_3x3[:2, :] = m_translations[i].astype(np.float32)
            
            # Combine: translation after rotation (matches sequential cv2.warpAffine order)
            m_combined_3x3 = m_trans_3x3 @ m_rot_3x3
            
            # Convert back to 2x3 for warpAffine compatibility
            m_combined[i] = m_combined_3x3[:2, :]
        
        # Process frames in batches using GPU reading
        # Use same batch size as original (30) for optimal I/O overlap
        # Main optimization: combined matrix (one warpAffine instead of two)
        img_counter = 0
        frm_batches = np.array_split(frm_range, (len(frm_range) + 30 - 1) // 30)
        for frm_batch_cnt, frm_ids in enumerate(frm_batches):
            frms = read_img_batch_from_video_gpu(video_path=video_path, start_frm=frm_ids[0], end_frm=frm_ids[-1], verbose=False)
            frms = np.stack(list(frms.values()), axis=0)
            for img_cnt, img in enumerate(frms):
                # Use combined matrix for single warpAffine (faster than two separate calls)
                m = m_combined[img_counter].astype(np.float32)
                final_frame = cv2.warpAffine(img, m, (video_meta['width'], video_meta['height']), borderValue=fill_clr)
                writer.write(final_frame)
                if verbose:
                    frame_id = frm_ids[img_cnt]
                    print(f'Creating frame {frame_id}/{video_meta["frame_count"]} ({video_name}, CPU core: {batch + 1}).')
                img_counter += 1
        
        # Legacy CuPy code (commented out - CPU is faster for this use case)
        if False and CUPY_AVAILABLE:
            # Pre-compute all inverse matrices upfront (much faster than per-frame)
            # For CuPy affine_transform, we need inverse matrices
            m_inv_matrices = []
            m_offsets = []
            for i in range(batch_size):
                m = m_combined[i]
                matrix_2x2 = m[:2, :2].astype(np.float32)
                offset = m[:2, 2].astype(np.float32)
                m_inv_matrices.append(cp.asarray(matrix_2x2))
                m_offsets.append(cp.asarray(offset))
            # Batch invert all matrices at once
            m_inv_matrices_gpu = cp.stack(m_inv_matrices)
            m_inv_matrices_gpu = cp.linalg.inv(m_inv_matrices_gpu)
            m_offsets_gpu = cp.stack(m_offsets)
            
            # Create async reader for GPU
            async_reader = AsyncVideoFrameReader(
                video_path=video_path,
                batch_size=batch_size_gpu,
                max_que_size=3,
                start_idx=frm_range[0],
                end_idx=frm_range[-1] + 1,
                gpu=True,  # Use GPU reading
                verbose=False
            )
            async_reader.start()
            
            # Process batches as they become available from async reader
            # Batch process and transfer to minimize GPU->CPU overhead
            processed_frames_batch = []
            frame_ids_batch = []
            
            while True:
                batch_result = get_async_frame_batch(batch_reader=async_reader, timeout=10)
                if batch_result is None:
                    # Write any remaining frames
                    if processed_frames_batch:
                        for frame in processed_frames_batch:
                            writer.write(frame)
                    break
                
                start_idx, end_idx, frms = batch_result
                batch_len = end_idx - start_idx + 1
                frms_gpu = cp.asarray(frms)
                
                # Process all frames in batch on GPU first
                batch_transformed = []
                batch_frame_indices = []
                
                for i in range(batch_len):
                    # Map frame index from video to frm_range index
                    frame_id = start_idx + i
                    frame_idx_in_range = np.where(frm_range == frame_id)[0]
                    if len(frame_idx_in_range) == 0:
                        continue
                    frame_idx_in_range = frame_idx_in_range[0]
                    batch_frame_indices.append((i, frame_idx_in_range))
                
                # Process all frames in this batch on GPU
                for i, frame_idx_in_range in batch_frame_indices:
                    img_gpu = frms_gpu[i]
                    matrix_inv = m_inv_matrices_gpu[frame_idx_in_range]
                    offset = m_offsets_gpu[frame_idx_in_range]
                    
                    if len(img_gpu.shape) == 3:  # Multi-channel
                        transformed_channels = []
                        for c in range(img_gpu.shape[2]):
                            transformed_ch = affine_transform(
                                img_gpu[:, :, c],
                                matrix=matrix_inv,
                                offset=offset,
                                output_shape=(video_meta['height'], video_meta['width']),
                                order=1,
                                mode='constant',
                                cval=fill_clr[c] if c < len(fill_clr) else fill_clr[0],
                                prefilter=False
                            )
                            transformed_channels.append(transformed_ch)
                        transformed = cp.stack(transformed_channels, axis=2)
                    else:  # Single channel
                        transformed = affine_transform(
                            img_gpu,
                            matrix=matrix_inv,
                            offset=offset,
                            output_shape=(video_meta['height'], video_meta['width']),
                            order=1,
                            mode='constant',
                            cval=fill_clr[0] if len(fill_clr) > 0 else 0,
                            prefilter=False
                        )
                    batch_transformed.append(transformed)
                
                # Batch transfer all frames from GPU to CPU at once
                if batch_transformed:
                    # Stack all transformed frames and transfer in one go
                    batch_transformed_stack = cp.stack(batch_transformed)
                    batch_cpu = cp.asnumpy(batch_transformed_stack).astype(np.uint8)
                    
                    # Write all frames from this batch
                    for frame_idx, (i, frame_idx_in_range) in enumerate(batch_frame_indices):
                        final_frame = batch_cpu[frame_idx]
                        writer.write(final_frame)
                        
                        if verbose:
                            frame_id = start_idx + i
                            print(f'Creating frame {frame_id}/{video_meta["frame_count"]} ({video_name}, CPU core: {batch + 1}).')
            
            async_reader.kill()
        
        else:
            # Fallback to CPU with combined matrix and batch reading
            # Process frames in batches
            # Use helper function directly to avoid nested multiprocessing (we're already in a worker process)
            # Larger batch size reduces overhead
            batch_size_gpu = 500
            frm_batches = np.array_split(frm_range, (len(frm_range) + batch_size_gpu - 1) // batch_size_gpu)
            
            # Create a mapping from frame_id to index in frm_range for fast lookup
            frm_id_to_idx = {frame_id: idx for idx, frame_id in enumerate(frm_range)}
            
            for frm_batch_cnt, frm_ids in enumerate(frm_batches):
                # Read batch of frames directly using helper (no multiprocessing)
                frm_idx_array = np.array(frm_ids)
                frms_dict = _read_img_batch_from_video_helper(
                    frm_idx=frm_idx_array,
                    video_path=video_path,
                    greyscale=False,
                    verbose=False,
                    black_and_white=False,
                    clahe=False
                )
                frms = np.stack([frms_dict[f] for f in frm_ids], axis=0)
                
                # Process all frames in batch using optimized CPU cv2.warpAffine with combined matrices
                for i, frame_id in enumerate(frm_ids):
                    # Fast dictionary lookup instead of np.where
                    frame_idx_in_range = frm_id_to_idx.get(frame_id)
                    if frame_idx_in_range is None:
                        continue
                    
                    img = frms[i]
                    m = m_combined[frame_idx_in_range].astype(np.float32)
                    final_frame = cv2.warpAffine(img, m, (video_meta['width'], video_meta['height']), borderValue=fill_clr)
                    writer.write(final_frame)
                    
                    if verbose:
                        print(f'Creating frame {frame_id}/{video_meta["frame_count"]} ({video_name}, CPU core: {batch + 1}).')
    else:
        cap = cv2.VideoCapture(video_path)
        for frm_idx, frm_id in enumerate(frm_range):
            img = read_frm_of_video(video_path=cap, frame_index=frm_id)
            rotated_frame = cv2.warpAffine(img, m_rotates[frm_idx], (video_meta['width'], video_meta['height']), borderValue=fill_clr)
            final_frame = cv2.warpAffine(rotated_frame, m_translations[frm_idx], (video_meta['width'], video_meta['height']), borderValue=fill_clr)
            writer.write(final_frame)
            if verbose:
                print(f'Creating frame {frm_id}/{video_meta["frame_count"]} ({video_name}, CPU core: {batch + 1}).')
    writer.release()
    return batch + 1

class EgocentricVideoRotator():
    """
    Perform egocentric rotation of a video using CPU multiprocessing.

    .. video:: _static/img/EgocentricalAligner_2.webm
       :width: 800
       :autoplay:
       :loop:

    .. seealso::
       To perform joint egocentric alignment of both pose and video, or pose only, use :func:`~simba.data_processors.egocentric_aligner.EgocentricalAligner`.
       To produce rotation vectors, use :func:`~simba.utils.data.egocentrically_align_pose_numba` or :func:`~simba.utils.data.egocentrically_align_pose`.

    :param Union[str, os.PathLike] video_path: Path to a video file.
    :param np.ndarray centers: A 2D array of shape `(num_frames, 2)` containing the original locations of `anchor_1_idx` in each frame before alignment. Returned by :func:`~simba.utils.data.egocentrically_align_pose_numba` or :func:`~simba.utils.data.egocentrically_align_pose`.
    :param np.ndarray rotation_vectors: A 3D array of shape `(num_frames, 2, 2)` containing the rotation matrices applied to each frame. Returned by :func:`~simba.utils.data.egocentrically_align_pose_numba` or :func:`~simba.utils.data.egocentrically_align_pose`.
    :param bool verbose: If True, prints progress. Deafult True.
    :param Tuple[int, int, int] fill_clr: The color of the additional pixels. Deafult black. (0, 0, 0).
    :param int core_cnt: Number of CPU cores to use for video rotation; `-1` uses all available cores.
    :param Optional[Union[str, os.PathLike]] save_path: The location where to store the rotated video. If None, saves the video as the same dir as the input video with the `_rotated` suffix.

    :example:
    >>> DATA_PATH = "C:\501_MA142_Gi_Saline_0513.csv"
    >>> VIDEO_PATH = "C:\501_MA142_Gi_Saline_0513.mp4"
    >>> SAVE_PATH = "C:\501_MA142_Gi_Saline_0513_rotated.mp4"
    >>> ANCHOR_LOC = np.array([250, 250])

    >>> df = read_df(file_path=DATA_PATH, file_type='csv')
    >>> bp_cols = [x for x in df.columns if not x.endswith('_p')]
    >>> data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int32)
    >>> _, centers, rotation_vectors = egocentrically_align_pose(data=data, anchor_1_idx=6, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=0)
    >>> rotater = EgocentricVideoRotator(video_path=VIDEO_PATH, centers=centers, rotation_vectors=rotation_vectors, anchor_location=ANCHOR_LOC, save_path=SAVE_PATH)
    >>> rotater.run()
    """

    def __init__(self,
                 video_path: Union[str, os.PathLike],
                 centers: np.ndarray,
                 rotation_vectors: np.ndarray,
                 anchor_location: Tuple[int, int],
                 verbose: bool = True,
                 fill_clr: Tuple[int, int, int] = (0, 0, 0),
                 core_cnt: int = -1,
                 save_path: Optional[Union[str, os.PathLike]] = None,
                 gpu: Optional[bool] = True):

        check_file_exist_and_readable(file_path=video_path)
        self.video_meta_data = get_video_meta_data(video_path=video_path)
        check_valid_array(data=centers, source=f'{self.__class__.__name__} centers', accepted_ndims=(2,), accepted_axis_1_shape=[2, ], accepted_axis_0_shape=[self.video_meta_data['frame_count']], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
        check_valid_array(data=rotation_vectors, source=f'{self.__class__.__name__} rotation_vectors', accepted_ndims=(3,), accepted_axis_0_shape=[self.video_meta_data['frame_count']], accepted_dtypes=Formats.NUMERIC_DTYPES.value)
        check_valid_tuple(x=anchor_location, source=f'{self.__class__.__name__} anchor_location', accepted_lengths=(2,), valid_dtypes=(int,))
        for i in anchor_location: check_int(name=f'{self.__class__.__name__} anchor_location', value=i, min_value=1)
        check_valid_boolean(value=[verbose], source=f'{self.__class__.__name__} verbose')
        check_if_valid_rgb_tuple(data=fill_clr)
        check_int(name=f'{self.__class__.__name__} core_cnt', value=core_cnt, min_value=-1, unaccepted_vals=[0])
        if core_cnt > find_core_cnt()[0] or core_cnt == -1:
            self.core_cnt = find_core_cnt()[0]
        else:
            self.core_cnt = core_cnt
        video_dir, self.video_name, _ = get_fn_ext(filepath=video_path)
        if save_path is not None:
            self.save_dir = os.path.dirname(save_path)
            check_if_dir_exists(in_dir=self.save_dir, source=f'{self.__class__.__name__} save_path')
        else:
            self.save_dir = video_dir
            save_path = os.path.join(video_dir, f'{self.video_name}_rotated.mp4')
        self.video_path, self.save_path = video_path, save_path
        self.centers, self.rotation_vectors, self.gpu = centers, rotation_vectors, gpu
        self.verbose, self.fill_clr, self.anchor_loc = verbose, fill_clr, anchor_location

    def run(self):
        video_timer = SimbaTimer(start=True)
        temp_dir = os.path.join(self.save_dir, 'temp')
        if not os.path.isdir(temp_dir):
            create_directory(paths=temp_dir)
        else:
            remove_a_folder(folder_dir=temp_dir)
            create_directory(paths=temp_dir)
        frm_list = np.arange(0, self.video_meta_data['frame_count'])
        frm_list = np.array_split(frm_list, self.core_cnt)
        frm_list = [(cnt, x) for cnt, x in enumerate(frm_list)]
        if self.verbose:
            print(f"Creating rotated video {self.video_name}, multiprocessing (chunksize: {1}, cores: {self.core_cnt})...")
        with multiprocessing.Pool(self.core_cnt, maxtasksperchild=Defaults.LARGE_MAX_TASK_PER_CHILD.value) as pool:
            constants = functools.partial(egocentric_video_aligner,
                                          temp_dir=temp_dir,
                                          video_name=self.video_name,
                                          video_path=self.video_path,
                                          centers=self.centers,
                                          rotation_vectors=self.rotation_vectors,
                                          target=self.anchor_loc,
                                          verbose=self.verbose,
                                          fill_clr=self.fill_clr,
                                          gpu=self.gpu)
            for cnt, result in enumerate(pool.imap(constants, frm_list, chunksize=1)):
                if self.verbose:
                    print(f"Rotate batch {result}/{self.core_cnt} complete...")
            pool.terminate()
            pool.join()

        concatenate_videos_in_folder(in_folder=temp_dir, save_path=self.save_path, remove_splits=True, gpu=self.gpu, verbose=self.verbose)
        video_timer.stop_timer()
        stdout_success(msg=f"Egocentric rotation video {self.save_path} complete", elapsed_time=video_timer.elapsed_time_str, source=self.__class__.__name__)

if __name__ == "__main__":
    DATA_PATH = r"C:\Users\sroni\OneDrive\Desktop\desktop\rotate_ex\data\501_MA142_Gi_Saline_0513.csv"
    VIDEO_PATH = r"C:\Users\sroni\OneDrive\Desktop\desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513.mp4"
    SAVE_PATH = r"C:\Users\sroni\OneDrive\Desktop\desktop\rotate_ex\videos\501_MA142_Gi_Saline_0513_rotated.mp4"
    ANCHOR_LOC = np.array([250, 250])

    df = read_df(file_path=DATA_PATH, file_type='csv')
    bp_cols = [x for x in df.columns if not x.endswith('_p')]
    data = df[bp_cols].values.reshape(len(df), int(len(bp_cols)/2), 2).astype(np.int32)

    _, centers, rotation_vectors = egocentrically_align_pose(data=data, anchor_1_idx=5, anchor_2_idx=2, anchor_location=ANCHOR_LOC, direction=0)
    rotater = EgocentricVideoRotator(video_path=VIDEO_PATH, centers=centers, rotation_vectors=rotation_vectors, anchor_location=(400, 100), save_path=SAVE_PATH, verbose=True, core_cnt=16, gpu=True)
    rotater.run()

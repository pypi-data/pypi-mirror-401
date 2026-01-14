from simba.utils.read_write import find_files_of_filetypes_in_directory, read_df


class ReverseFeatures():

    def __init__(self,
                 input_dir: str,
                 output_dir: str):

        self.data_paths = find_files_of_filetypes_in_directory(directory=input_dir, extensions=['.csv'], raise_error=True, as_dict=True)

    def run(self):
        for file_cnt, (file_name, file_path) in enumerate(self.data_paths.items()):
            data_df = read_df(file_path=file_path)
            original_cols, out_df = list(data_df.columns), data_df.copy()
            col_mapping = { col: col.replace('resident', 'TEMP_PLACEHOLDER') .replace('intruder', 'resident') .replace('TEMP_PLACEHOLDER', 'intruder') for col in original_cols}
            out_df = out_df.rename(columns=col_mapping)
            swapped_cols_in_original_order = [col_mapping[col] for col in original_cols]
            out_df = out_df[swapped_cols_in_original_order]


            #out_df = out_df[original_cols]











d = ReverseFeatures(input_dir=r'E:\maplight_reverse_clf\test', output_dir=r'E:\maplight_reverse_clf\out')
d.run()

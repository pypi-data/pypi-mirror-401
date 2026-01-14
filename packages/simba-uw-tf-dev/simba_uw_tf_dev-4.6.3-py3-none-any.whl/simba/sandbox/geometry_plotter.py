from simba.plotting.geometry_plotter import GeometryPlotter
from simba.sandbox.ares.ares_data_to_polygons import Ares2Polygons

from simba.utils.lookups import get_random_color_palette

VIDEO_PATH = r"D:\troubleshooting\termite_tow\Test Data\Termite Test 3.mp4"
SAVE_PATH = r"D:\troubleshooting\termite_tow\Test Data\Termite Test 3_geo.mp4"

x = Ares2Polygons(data=r"D:\troubleshooting\termite_tow\ProcessedTracks.pkl", core_cnt=12, parallel_offset=40)
x.run()

geometries = [x.results[f] for f in x.results.keys()]


colors = get_random_color_palette(n_colors=27)


plotter = GeometryPlotter(geometries=geometries, video_name=VIDEO_PATH, save_dir=r'D:\troubleshooting\termite_tow\Test Data\out', core_cnt=16, colors=colors, intersection_clr=None, shape_opacity=0.6)
plotter.run()
#
#
#
# x.results
#





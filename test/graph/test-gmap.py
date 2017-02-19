from src.util import gmplot_mod

gmap = gmplot_mod.GoogleMapPlotter(54.0020096, 21.7779824, 4)

latitudes = [59.939039, 55.755786]
longitudes = [30.315785, 37.617633]
# for i in range(0, len(latitudes)):
#     gmap.marker(latitudes[i], longitudes[i], color="blue", title="City{}".format(i))
gmap.plot(latitudes, longitudes, 'red', edge_width=3, edge_text="Test message", edge_alpha=0.7)

latitudes = [52.5234051, 56.18113]
longitudes = [13.4113999, 92.48286]
# for i in range(0, len(latitudes)):
#     gmap.marker(latitudes[i], longitudes[i], color="blue", title="City{}".format(i))
gmap.plot(latitudes, longitudes, 'red', edge_width=3, edge_text="Test message", edge_alpha=0.7)

gmap.draw("mymap.html")

import mapnik


m = mapnik.Map(600,300)
m.background = mapnik.Color('steelblue')
s = mapnik.Style()
r = mapnik.Rule()
polygon_symbolizer = mapnik.PolygonSymbolizer(mapnik.Color('#f2eff9'))
r.symbols.append(polygon_symbolizer)
line_symbolizer = mapnik.LineSymbolizer(mapnik.Color('rgb(50%,50%,50%)'),0.1)
point_symbolizer = mapnik.PointSymbolizer()
r.symbols.append(line_symbolizer)
r.symbols.append(point_symbolizer)
s.rules.append(r)
m.append_style('My Style',s)

file = "C:\Users\Work\Documents\Files\Projects\RadioCollar\SampleData\RCT_SAMPLE\RUN_002027\RUN_002027_COL_000001\RUN_002027_COL_000001.shp"

ds = mapnik.Shapefile(file=file)
layer = mapnik.Layer('world')
layer.datasource = ds
layer.styles.append('My Style')

print("ds")
print(ds)

print("envelope")
print(layer.envelope())
print("values")
print(layer.styles)

m.layers.append(layer)
m.zoom_all()
mapnik.render_to_file(m,'world.png', 'png')
print "rendered image to 'world.png'"
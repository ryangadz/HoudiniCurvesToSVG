node = hou.pwd()
geo = node.geometry()

# Add code to modify contents of geo.
# Use drop down menu to select examples.

filename = node.evalParm('filename')
maxsize = node.evalParm('maxsize')
stroke_width = node.evalParm('stroke_width')

box = geo.boundingBox()
minv = box.minvec()
size = box.sizevec()

if size.x() > size.z():
  width = maxsize
  height = maxsize * size.z() / size.z()
else:
  height = maxsize
  width = maxsize * size.x() / size.z()
  
def write_path(fp, points):
  if not points:
    return
  data = 'M{} {} '.format(points[0].x(), points[0].y())
  midpoint = hou.Vector2((points[1].x() + points[2].x())/2, 
                         (points[1].y() + points[2].y())/2)
  data += 'Q{} {} {} {} '.format(points[1].x(), points[1].y(), midpoint.x(), midpoint.y())
  length = len(points)-1
  i = 2 

  for i in range(2, length):
    midpoint = hou.Vector2((points[i].x() + points[i+1].x())/2, 
                           (points[i].y() + points[i+1].y())/2)                                             
    data += 'T{} {} '.format(midpoint.x(), midpoint.y())
  data += 'T{} {} '.format(points[length].x(), points[length].y())
  fp.write('<path d="{}" stroke="blue" stroke-width="{}px" fill="none"/>\n'.format(data, stroke_width))

   
def transform_points(points):
  for p in points:
    p = hou.Vector2(
      (p.x() - minv.x()) / size.x() * width,
      ( (p.z() - minv.z()) / size.z()) * height
    )
    yield p
  
with open(filename, 'w') as fp:
  fp.write('<?xml version="1.0" standalone="no"?>\n')
  fp.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n')
  fp.write('<svg width="{}px" height="{}px" version="1.1" xmlns="http://www.w3.org/2000/svg">\n'.format(width, height))
  for prim in geo.iterPrims():
   # if prim.type() != hou.primType.Polygon:
   #   continue
    points = [v.point().position() for v in prim.vertices()]
    points = list(transform_points(points))
    write_path(fp, points)
  fp.write('</svg>')
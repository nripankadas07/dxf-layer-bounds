import unittest,math
from dxf_layer_bounds import analyze
def entity(kind,**values):
 return [(0,kind)]+[(int(k[1:]),str(v)) for k,v in values.items()]
def drawing(*entities):
 tags=[(0,'SECTION'),(2,'ENTITIES')]+[t for e in entities for t in e]+[(0,'ENDSEC'),(0,'EOF')];return '\n'.join(str(v) for t in tags for v in t)+'\n'
L=entity('LINE',c8='cuts',c10=0,c20=0,c11=3,c21=4)
class DrawingTests(unittest.TestCase):
 def test_line_layer_length(self):
  r=analyze(drawing(L));self.assertEqual(r['layers'][0]['bounds_xy'],[0,0,3,4]);self.assertEqual(r['layers'][0]['length_approx'],5)
 def test_circle_bounds(self):
  r=analyze(drawing(entity('CIRCLE',c10=2,c20=3,c40=5)));self.assertEqual(r['layers'][0]['bounds_xy'],[-3,-2,7,8])
 def test_arc_cardinal_extrema(self):
  b=analyze(drawing(entity('ARC',c10=0,c20=0,c40=2,c50=45,c51=225)))['entities'][0]['bounds_xy'];self.assertEqual(b[:1],[-2]);self.assertAlmostEqual(b[1],-math.sqrt(2));self.assertEqual(b[3],2)
 def test_arc_cross_zero(self):
  e=analyze(drawing(entity('ARC',c10=0,c20=0,c40=1,c50=350,c51=10)))['entities'][0];self.assertEqual(e['bounds_xy'][2],1);self.assertAlmostEqual(e['length_approx'],math.radians(20))
 def test_layer_union(self):
  r=analyze(drawing(L,entity('CIRCLE',c8='cuts',c10=10,c20=10,c40=1),entity('LINE',c8='other',c10=-4,c20=-4,c11=-3,c21=-3)));self.assertEqual(len(r['layers']),2);self.assertEqual(r['layers'][0]['bounds_xy'],[0,0,11,11]);self.assertEqual(r['layers'][0]['counts'],{'CIRCLE':1,'LINE':1})
 def test_zero_length_finding(self):self.assertEqual(analyze(drawing(entity('LINE',c10=1,c20=1,c11=1,c21=1)))['zero_length_entities'],[1])
 def test_default_layer_and_extrusion(self):self.assertEqual(analyze(drawing(entity('CIRCLE',c10=0,c20=0,c40=1,c210=0,c220=0,c230=1)))['layers'][0]['layer'],'0')
 def test_hidden_entities_retained(self):self.assertEqual(len(analyze(drawing(L+[(60,'1')]))['entities']),1)
 def test_unsupported_entities(self):
  for kind in ['INSERT','TEXT','LWPOLYLINE','SPLINE']:
   with self.assertRaises(ValueError):analyze(drawing(entity(kind)))
 def test_3d_thickness_and_layout_refused(self):
  for tag in [(30,'1'),(39,'1'),(210,'1'),(230,'-1'),(67,'1'),(410,'Layout1')]:
   with self.assertRaises(ValueError):analyze(drawing(L+[tag]))
 def test_duplicate_geometry(self):
  with self.assertRaises(ValueError):analyze(drawing(L+[(10,'2')]))
 def test_nonfinite_and_radius(self):
  for radius in ['0','-1','NaN','1e999']:
   with self.assertRaises(ValueError):analyze(drawing(entity('CIRCLE',c10=0,c20=0,c40=radius)))
 def test_zero_sweep_arc(self):
  with self.assertRaises(ValueError):analyze(drawing(entity('ARC',c10=0,c20=0,c40=1,c50=0,c51=360)))
 def test_missing_coordinate(self):
  with self.assertRaises(ValueError):analyze(drawing(entity('LINE',c10=0,c20=0,c11=1)))
 def test_section_integrity(self):
  text=drawing(L)
  for bad in [text.replace('ENDSEC','NOPE'),text+'0\nEOF\n',text+'1\n',text.replace('2\nENTITIES','3\nENTITIES')]:
   with self.assertRaises(ValueError):analyze(bad)
 def test_comments_and_ignored_sections(self):
  r=analyze('0\nSECTION\n2\nHEADER\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n999\ninvented\n'+drawing(L));self.assertEqual(r['sections'],{'ENTITIES':1,'HEADER':1})
 def test_byte_budget(self):
  with self.assertRaises(ValueError):analyze(' '*(2*1024*1024+1))
if __name__=='__main__':unittest.main()

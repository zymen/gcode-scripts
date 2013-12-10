import unittest

from core import Project, Element, Configuration, ElementGcodeGenerator
from parts.wall.wall import Wall

class WallGcodeGeneratorTest(unittest.TestCase):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    
  def test_is_output_correct(self):
    self.project.add_element(Wall(0, 0, 10, 10));
    output = self.project.generate_gcode();
    self.assertTrue("G1 x0.000000 y0.000000" in output)
    self.assertTrue("G1 x10.000000 y0.000000" in output)
    self.assertTrue("G1 x10.000000 y10.000000" in output)
      

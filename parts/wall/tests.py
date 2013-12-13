import unittest

from core import Project, Element, Configuration, ElementGcodeGenerator, Tool
from parts.wall.wall import WallBuilder

class WallGcodeGeneratorSimpleTest(unittest.TestCase):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    
  def test_is_output_correct(self):
    wall = WallBuilder \
            .new_wall(self.project) \
            .start_at(0, 0) \
            .with_size(10, 10) \
            .build()

    self.project.add_element(wall);
    output = self.project.generate_gcode();

    self.assertTrue("G1 x0.000000 y0.000000" in output)
    self.assertTrue("G1 x10.000000 y0.000000" in output)
    self.assertTrue("G1 x10.000000 y10.000000" in output)
      

class WallGcodeGeneratorToolUsageTest(unittest.TestCase):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    self.project.set_tool(Tool(cutter_diameter = 4))
    
  def test_is_output_correct(self):
    wall = WallBuilder \
            .new_wall(self.project) \
            .start_at(0, 0) \
            .with_size(10, 10) \
            .build()

    self.project.add_element(wall);
    output = self.project.generate_gcode();

    self.assertTrue("G1 x-2.000000 y-2.000000" in output)
    self.assertTrue("G1 x12.000000 y-2.000000" in output)
    self.assertTrue("G1 x12.000000 y12.000000" in output)
      


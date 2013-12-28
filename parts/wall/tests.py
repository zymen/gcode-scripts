import unittest

from gcode_parser.parser import GcodeParser, GcodeG1Command
from gcode_parser.tests import GcodeParserBaseTests
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

    gcode_generator = wall.get_gcode_generator()
    output = gcode_generator.generate_gcode()

    parser = GcodeParser(output)
    cmd = parser.next_code()

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
      

class WallGcodeGeneratorWithWoodenJointsTest(GcodeParserBaseTests):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    self.project.set_tool(Tool(cutter_diameter = 0))
    
  def test_is_output_correct(self):
    wall = WallBuilder \
            .new_wall(self.project) \
            .start_at(0, 0) \
            .with_size(30, 10) \
            .with_wooden_joints(on_bottom = True) \
            .build()

    self.project.add_element(wall);
    output = self.project.generate_gcode();

    #print output

    parser = GcodeParser(output)
    code = parser.find(GcodeG1Command(x = 0, y = 5))

    self.assertTrue(code != None)

    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 5), code)
    self.assertTrue("G1 x0.000000 y15.000000" in output)
    self.assertTrue("G1 x30.000000 y15.000000" in output)
    self.assertTrue("G1 x30.000000 y5.000000" in output)
      
    self.assertTrue("G1 x25.000000 y5.000000" in output)
    self.assertTrue("G1 x25.000000 y0.000000" in output)
    self.assertTrue("G1 x20.000000 y0.000000" in output)
    self.assertTrue("G1 x20.000000 y5.000000" in output)


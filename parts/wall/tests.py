import unittest

from gcode_parser.parser import GcodeParser, GcodeG1Command
from gcode_parser.tests import GcodeParserBaseTests
from core import Project, Element, Configuration, ElementGcodeGenerator, Tool
from parts.wall.wall import WallBuilder

class WallGcodeGeneratorSimpleTest(GcodeParserBaseTests):
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
    code = parser.next_code()

    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 0), code)
    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 10), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 10, y = 10), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 10, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 0), parser.next_code())

class WallGcodeGeneratorToolUsageTest(GcodeParserBaseTests):
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

    gcode_generator = wall.get_gcode_generator()
    output = gcode_generator.generate_gcode()

    parser = GcodeParser(output)
    code = parser.next_code()

    self.assertAreEqualGcodes(GcodeG1Command(x = -2, y = -2), code)
    self.assertAreEqualGcodes(GcodeG1Command(x = -2, y = 12), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 12, y = 12), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 12, y = -2), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = -2, y = -2), parser.next_code())

class WallGcodeGeneratorWithWoodenJointsTest(GcodeParserBaseTests):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    self.project.set_tool(Tool(cutter_diameter = 0))
    
  def test_is_output_for_bottom_side_correct(self):
    wall = WallBuilder \
            .new_wall(self.project) \
            .start_at(0, 0) \
            .with_size(30, 10) \
            .with_wooden_joints(on_bottom = True) \
            .build()

    gcode_generator = wall.get_gcode_generator()
    output = gcode_generator.generate_gcode()

    parser = GcodeParser(output)

    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 5), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 15), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 30, y = 15), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 30, y = 5), parser.next_code())

    # now bottom side
    #first tit
    self.assertAreEqualGcodes(GcodeG1Command(x = 30, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 25, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 25, y = 5), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 20, y = 5), parser.next_code())

    #second tit
    self.assertAreEqualGcodes(GcodeG1Command(x = 20, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 15, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 15, y = 5), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 10, y = 5), parser.next_code())

    #second tit
    self.assertAreEqualGcodes(GcodeG1Command(x = 10, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 5, y = 0), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 5, y = 5), parser.next_code())
    self.assertAreEqualGcodes(GcodeG1Command(x = 0, y = 5), parser.next_code())

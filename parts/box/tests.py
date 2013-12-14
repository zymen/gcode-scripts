import unittest

from core import Project, Element, Configuration, ElementGcodeGenerator, Tool
from parts.box.box import BoxBuilder

class BoxTest(unittest.TestCase):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    
  def test_has_this_box_4_walls(self):
    box = BoxBuilder \
            .new_box(self.project) \
            .start_at(0, 0) \
            .with_size(40, 60, 80) \
            .build()

    self.project.add_element(box);
    self.assertEquals(4, len(box.walls))

class BoxGcodeGeneratorSimpleTest(unittest.TestCase):
  project = None

  def setUp(self):
    self.project = Project()
    self.project.set_configuration(Configuration())
    
  def test_should_return_non_empty_string(self):
    box = BoxBuilder \
            .new_box(self.project) \
            .start_at(0, 0) \
            .with_size(40, 60, 80) \
            .build()

    self.project.add_element(box);
    gcode_generator = box.get_gcode_generator()
    output = gcode_generator.generate_gcode()

    self.assertTrue(output != None and len(output) > 0)

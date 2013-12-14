import unittest

from core import Project

class ProjectGcodeGeneratorsOutputTest(unittest.TestCase):
  project = None
  output = None

  def setUp(self):
    self.project = Project()
    self.output = self.project.generate_gcode()

  def test_has_on_first_line_percentage_sign(self):
    self.assertEquals('%', self.output[0].strip())

  def test_has_on_last_line_percentage_sign(self):
    self.assertEquals('%', self.output[-1].strip())

  def test_should_have_defined_speed(self):
    self.assertTrue('G1 F' in self.output)

  def test_should_have_defined_speed(self):
    self.assertTrue('G21 ' in self.output)

  def test_should_go_back_to_home_in_last_steps(self):
    self.assertTrue('G0 Z3.000000' in self.output[:-5])
    self.assertTrue('G0 X0.000000 Y0.000' in self.output[:-5])


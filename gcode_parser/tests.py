import unittest

from parser import GcodeParser, GcodeCommand

class GcodeParserSimpleUsageTests(unittest.TestCase):
  def test_does_it_correctly_counts_number_of_lines(self):
    gcode = """
    G1 F1000
    G1 Z2.000 X-3 Y0.0001
    """

    parser = GcodeParser(gcode)
    self.assertEquals(2, parser.get_lines_number())

  def test_does_it_correctly_recognizes_g1(self):
    gcode = """
    G1 F1000
    G1 Z2.000 X-3 Y0.0001
    """

    parser = GcodeParser(gcode)

    code = parser.next_code()
    self.assertTrue(isinstance(code, GcodeCommand)) 

    code = parser.next_code()
    self.assertTrue(isinstance(code, GcodeCommand)) 
    self.assertEquals("G1", code.get_code())
    self.assertEquals(-3, code.get_x())
    self.assertEquals(0.0001, code.get_y())
    self.assertEquals(2, code.get_z())


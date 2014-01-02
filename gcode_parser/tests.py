import unittest

from parser import GcodeParser, GcodeCommand, GcodeG1Command, GcodeCommentCommand

class GcodeParserBaseTests(unittest.TestCase):
  def assertAreEqualGcodes(self, code1, code2):
    self.assertTrue(isinstance(code1, GcodeCommand)) 
    self.assertTrue(isinstance(code2, GcodeCommand)) 

    self.assertEquals(code1.get_code(), code2.get_code())
    self.assertEquals(code1.get_x(), code2.get_x())
    self.assertEquals(code1.get_y(), code2.get_y())
    self.assertEquals(code1.get_z(), code2.get_z())

class GcodeParserSimpleUsageTests(GcodeParserBaseTests):
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
    self.assertAreEqualGcodes(code, GcodeG1Command(x = -3, y = 0.0001, z = 2))

  def test_checking_movement_with_comments_inside_gcode(self):
    gcode = """
    (test)
    G1 F1000
    (test 2)
    G1 Z2.000 X-3 Y0.0001
    """

    parser = GcodeParser(gcode)

    code = parser.next_code(ignore_comments = False)
    self.assertTrue(isinstance(code, GcodeCommentCommand)) 

    code = parser.next_code(ignore_comments = False)
    self.assertTrue(isinstance(code, GcodeG1Command))     

    code = parser.next_code(ignore_comments = False)
    self.assertTrue(isinstance(code, GcodeCommentCommand)) 

    code = parser.next_code(ignore_comments = False)
    self.assertAreEqualGcodes(code, GcodeG1Command(x = -3, y = 0.0001, z = 2))


import unittest

from core import Element, ElementGcodeGenerator

class Wall(Element):
  start_x = 0 
  start_y = 0
  width = 0
  height = 0

  @property
  def start_x_width(self):
    return self.start_x + self.width

  @property
  def start_y_height(self):
    return self.start_y + self.height

  def get_gcode_generator(self):
    return WallGcodeGenerator(self)

  def __init__(self, start_x, start_y, width, height):
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height

class WallGcodeGenerator(ElementGcodeGenerator):
  wall = None

  def __init__(self, wall):
    self.wall = wall

  def generate_gcode(self):
    wall_data = self.wall.__dict__
    wall_data['start_x_width'] = self.wall.start_x_width
    wall_data['start_y_height'] = self.wall.start_y_height

    output = ""
    output = output + "G1 x%(start_x)f y%(start_y)f\n" % wall_data
    output = output + "G1 x%(start_x_width)f y%(start_y)f\n" % wall_data
    output = output + "G1 x%(start_x_width)f y%(start_y_height)f\n" % wall_data

    return output

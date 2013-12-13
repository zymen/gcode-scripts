import unittest

from core import Element, ElementGcodeGenerator

class Wall(Element):
  context = None
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

  def __init__(self, context, start_x, start_y, width, height):
    self.context = context
    self.start_x = start_x
    self.start_y = start_y
    self.width = width
    self.height = height

class WallBuilder(object):
  wall = None

  @staticmethod
  def new_wall(project):
    builder = WallBuilder()
    builder.wall = Wall(project.context, 0, 0, 0, 0)
    return builder

  def build(self):
    return self.wall

  def start_at(self, x, y):
    self.wall.start_x = x
    self.wall.start_y = y

    return self

  def with_size(self, width, height):
    self.wall.width = width
    self.wall.height = height 

    return self

class WallGcodeGenerator(ElementGcodeGenerator):
  context = None
  wall = None

  def __init__(self,  wall):
    self.context = wall.context
    self.wall = wall

  def generate_gcode(self):
    half_tool = self.context.tool.cutter_diameter / 2
    wall = self.wall

    output = ""
    output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool, wall.start_y - half_tool)
    output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool, wall.start_y_height + half_tool)
    output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool, wall.start_y_height + half_tool)
    output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool, wall.start_y - half_tool)
    output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool, wall.start_y - half_tool)

    return output

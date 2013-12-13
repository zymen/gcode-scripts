import unittest

from core import Element, ElementGcodeGenerator
from parts.wall.wall import WallBuilder

class Box(Element):
  context = None
  start_x = 0 
  start_y = 0
  width = 0
  height = 0
  depth = 0
  walls = []

  @property
  def start_x_width(self):
    return self.start_x + self.width

  @property
  def start_y_height(self):
    return self.start_y + self.height

  def get_gcode_generator(self):
    return BoxGcodeGenerator(self)

  def __init__(self, context):
    self.context = context
    self.walls = []

class BoxBuilder(object):
  box = None
  project = None

  @staticmethod
  def new_box(project):
    builder = BoxBuilder()
    builder.box = Box(project.context)
    builder.project = project
    return builder

  def build(self):

    for index in range(0, 4):
      wall = WallBuilder \
                .new_wall(self.project) \
                .build()

      self.box.walls.append(wall)

    return self.box

  def start_at(self, x, y):
    self.box.start_x = x
    self.box.start_y = y

    return self

  def with_size(self, width, height, depth):
    self.box.width = width
    self.box.height = height 
    self.box.depth = depth

    return self

class BoxGcodeGenerator(ElementGcodeGenerator):
  context = None
  box = None

  def __init__(self,  box):
    self.context = box.context
    self.box = box

  def generate_gcode(self):

    for wall_index in range(0, len(self.box.walls)):
      wall = self.box.walls[wall_index]

      wall_gcode_generator = wall.get_gcode_generator()
      output = output + wall_gcode_generator.generate_gcode()
      output = output + "\n\n"

    return output

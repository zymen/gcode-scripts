import unittest

from core import Element, ElementGcodeGenerator

class Wall(Element):
  context = None
  start_x = 0 
  start_y = 0
  width = 0
  height = 0
  wooden_joints = {}

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
    self.wooden_joints = {}

class WallBuilder(object):
  wall = None

  @staticmethod
  def new_wall(project):
    builder = WallBuilder()
    builder.wall = Wall(project.context, 0, 0, 0, 0)
    return builder

  def build(self):
    return self.wall

  def with_wooden_joints(self, on_left = False, on_right = False, on_top = False, on_bottom = False):
    self.wall.wooden_joints = {}

    if on_left:
      self.wall.wooden_joints['left'] = True

    if on_right:
      self.wall.wooden_joints['right'] = True

    if on_top:
      self.wall.wooden_joints['top'] = True

    if on_bottom:
      self.wall.wooden_joints['bottom'] = True

    return self
    
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

  def _generate_gcode_for_left_side(self, offset_in_width, offset_in_height, half_tool, tit_size):
    wall = self.wall
    output = ""
    output = output + "(wall left bottom)\n"

    if wall.wooden_joints.has_key('left'):
      output = output + "G1 x%f y%f\n" % (wall.start_x + offset_in_width, wall.start_y - half_tool + offset_in_height)

      steps = wall.height / tit_size
      last_x = 0
      last_y = 0

      for step_index in range(0, steps):
        if step_index % 2 == 0:
          #horizontal
          last_x = wall.start_x - half_tool
          last_y = wall.start_y - half_tool + step_index * tit_size
          output = output + "G1 x%f y%f\n" % (last_x, last_y)

          last_x = wall.start_x - half_tool
          last_y = wall.start_y + half_tool + (step_index + 1) * tit_size
          output = output + "G1 x%f y%f\n" % (last_x, last_y)
        else:
          #vertical
          last_x = wall.start_x - half_tool + tit_size
          last_y = wall.start_y + half_tool + step_index * tit_size
          output = output + "G1 x%f y%f\n" % (last_x, last_y)

          last_x = wall.start_x - half_tool + tit_size
          last_y = wall.start_y - half_tool + (step_index + 1) * tit_size
          output = output + "G1 x%f y%f\n" % (last_x, last_y)

      proposed_x = wall.start_x - half_tool + tit_size
      proposed_y = wall.start_y_height + half_tool + offset_in_height

      if last_x != proposed_x or last_y != proposed_y:
        output = output + "(wall left top)\n"
        output = output + "G1 x%f y%f\n" % (proposed_x, proposed_y)

    else:
      output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool + offset_in_width, wall.start_y - half_tool + offset_in_height)

      output = output + "(wall left top)\n"
      output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool, wall.start_y_height + half_tool + offset_in_height)

    return output

  def generate_gcode(self):
    half_tool = self.context.tool.cutter_diameter / 2
    wall = self.wall
    tit_size = 5

    offset_in_height = 0
    offset_in_width = 0

    if wall.wooden_joints.has_key('left'):
      offset_in_width = offset_in_width + tit_size

    if wall.wooden_joints.has_key('top'):
      offset_in_height = offset_in_height + tit_size

    if wall.wooden_joints.has_key('bottom'):
      offset_in_height = offset_in_height + tit_size

    output = ""
    output = output + self._generate_gcode_for_left_side(offset_in_width, offset_in_height, half_tool, tit_size)

    output = output + "(wall right top)\n"
    output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool, wall.start_y_height + half_tool + offset_in_height)

    output = output + "(wall right bottom)\n"
    output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool, wall.start_y - half_tool + offset_in_height)

    if wall.wooden_joints.has_key('bottom'):
      steps = wall.width / tit_size

      for step_index in range(0, steps):
        if step_index % 2 == 0:
          output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool - step_index * tit_size, wall.start_y - half_tool)
          output = output + "G1 x%f y%f\n" % (wall.start_x_width - half_tool - (step_index +1) * tit_size, wall.start_y - half_tool)
        else:
          output = output + "G1 x%f y%f\n" % (wall.start_x_width - half_tool - step_index * tit_size, wall.start_y - half_tool + offset_in_height)
          output = output + "G1 x%f y%f\n" % (wall.start_x_width + half_tool - (step_index +1) * tit_size, wall.start_y - half_tool + offset_in_height)

    output = output + "(wall left bottom)\n"
    output = output + "G1 x%f y%f\n" % (wall.start_x - half_tool, wall.start_y - half_tool + offset_in_height)

    return output

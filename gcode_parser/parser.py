class GcodeParser(object):
  gcode = None
  _gcode_objects = {}
  _gcode_pointer = 0

  def get_lines_number(self):
    return len(self.gcode)

  def _prepare_gcode_command(self, command_raw):
    if command_raw[0] == '(':
      return GcodeCommentCommand()

    code = command_raw.split(" ")

    if code[0].upper() == 'G1':
      return GcodeG1Command(gcode_command = command_raw)

    return GcodeCommand(command_raw)

  def next_code(self, ignore_comments = True):
    command = None

    while self._gcode_pointer < len(self.gcode) and command == None:
      if not self._gcode_objects.has_key(self._gcode_pointer):
         command_raw = self.gcode[self._gcode_pointer]
         command = self._prepare_gcode_command(command_raw)
         self._gcode_objects[self._gcode_pointer] = command
      else:
         command = self._gcode_objects[self._gcode_pointer]

      self._gcode_pointer = self._gcode_pointer + 1

      if command.code == 'COMMENT' and ignore_comments:
        command = None
        continue

    return command

  def _get_code_on_position(self, position, ignore_comments = True):
    command = None

    saved_gcode_pointer = self._gcode_pointer
    self._gcode_pointer = position

    command = self.next_code(ignore_comments = ignore_comments)

    self._gcode_pointer = saved_gcode_pointer

    return command

  def get_first_code(self, ignore_comments = True):
    position = 0
    return self._get_code_on_position(position)

  def get_last_code(self, ignore_comments = True):
    position = len(self.gcode) - 1
    return self._get_code_on_position(position)

  def find(self, searched_command):
    for index in range(0, len(self.gcode)):
      entry = self._prepare_gcode_command(self.gcode[index])
      if entry == searched_command:
        self._gcode_pointer = index + 1
        return entry

    return None
    
  def __init__(self, gcode):
    self.gcode = []
    self._gcode_objects = {}
    self._gcode_pointer = 0

    for line in gcode.split("\n"):
       if line.strip() != "":
         self.gcode.append(line.strip()) 

class GcodeCommand(object):
  code = None

  def get_code(self):
    return self.code

  def __init__(self, gcode_command = None, code = None):
    if code != None:
      self.code = code

    if gcode_command != None:
      parts = gcode_command.split(" ")
      self.code = parts[0]

  def __eq__(self, other):
    if not isinstance(other, GcodeCommand):
      return False

    return self.code == other.code


class GcodeCommentCommand(GcodeCommand):
  def __init__(self):
    self.code = 'COMMENT'

class GcodeG1Command(GcodeCommand):
  x = None
  y = None
  z = None

  def get_x(self):
    return self.x

  def get_y(self):
    return self.y

  def get_z(self):
    return self.z

  def __init__(self, gcode_command = None, gcode = None, x = None, y = None, z = None):
    if gcode_command != None:
      super(GcodeG1Command, self).__init__(gcode_command)
      parts = gcode_command.split(" ")

      for param in parts:
        if param[0].lower() == 'x':
          self.x = float(param[1:])

        if param[0].lower() == 'y':
          self.y = float(param[1:])

        if param[0].lower() == 'z':
          self.z = float(param[1:])
    else:
      self.code = "G1"
      self.x = x
      self.y = y
      self.z = z

  def __eq__(self, other):
    if not isinstance(other, GcodeG1Command):
      return False

    return super(GcodeG1Command, self).__eq__(other) and self.x == other.x and self.y == other.y and self.z == other.z

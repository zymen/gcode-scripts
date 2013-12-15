class GcodeParser(object):
  gcode = None
  _gcode_objects = {}
  _gcode_pointer = 0

  def get_lines_number(self):
    return len(self.gcode)

  def _prepare_gcode_command(self, command_raw):
    code = command_raw.split(" ")
    if code[0].upper() == 'G1':
      return GcodeG1Command(command_raw)

    return GcodeCommand(command_raw)

  def next_code(self):
    command = None

    if not self._gcode_objects.has_key(self._gcode_pointer):
       command_raw = self.gcode[self._gcode_pointer]
       command = self._prepare_gcode_command(command_raw)
       self._gcode_objects[self._gcode_pointer] = command
    else:
       command = self._gcode_objects[self._gcode_pointer]

    self._gcode_pointer = self._gcode_pointer + 1

    return command
    
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

  def __init__(self, gcode_command):
    parts = gcode_command.split(" ")
    self.code = parts[0]

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

  def __init__(self, gcode_command):
    super(GcodeG1Command, self).__init__(gcode_command)
    parts = gcode_command.split(" ")

    for param in parts:
      if param[0].lower() == 'x':
        self.x = float(param[1:])

      if param[0].lower() == 'y':
        self.y = float(param[1:])

      if param[0].lower() == 'z':
        self.z = float(param[1:])

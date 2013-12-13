
class Configuration(object):
  tit_size = 3

class Tool(object):
  cutter_diameter = 0 

  def __init__(self, cutter_diameter = 0):
    self.cutter_diameter = cutter_diameter

class Context(object):
  config = None
  tool = None

  def __init__(self, tool = Tool()):
    self.tool = tool

class Element(object):
  def get_gcode_generator(self):
    pass

class ElementGcodeGenerator(object):
   def generate_gcode(self):
    pass

class Project(object):
  elements = []
  context = None

  def __init__(self):
    self.elements = []
    self.context = Context()

  def add_element(self, element):
    self.elements.append(element)

  def set_configuration(self, configuration):
    self.context.configuration = configuration

  def set_tool(self, tool):
    self.context.tool = tool

  def generate_gcode(self):
    output = ""

    for element in self.elements:
      gcode_generator = element.get_gcode_generator()
      output = output + gcode_generator.generate_gcode()

    return output
    

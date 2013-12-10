
class Configuration(object):
	tit_size = 3

class Element(object):
  def get_gcode_generator(self):
    pass

class ElementGcodeGenerator(object):
   def generate_gcode(self):
    pass

class Project(object):
  elements = []
  configuration = None

  def __init__(self):
    self.elements = []

  def add_element(self, element):
    self.elements.append(element)

  def set_configuration(self, configuration):
    self.configuration = configuration

  def generate_gcode(self):
    output = ""

    for element in self.elements:
      gcode_generator = element.get_gcode_generator()
      output = output + gcode_generator.generate_gcode()

    return output
    

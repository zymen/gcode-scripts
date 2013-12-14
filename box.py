from core import Project, Element, Configuration, ElementGcodeGenerator, Tool
from parts.box.box import BoxBuilder

def main():
  project = Project()
  project.set_configuration(Configuration())
  project.set_tool(Tool(cutter_diameter = 2))

  box = BoxBuilder \
          .new_box(project) \
          .start_at(0, 0) \
          .with_size(40, 60, 80) \
          .with_wooden_joints() \
          .build()

  project.add_element(box);

  print project.generate_gcode()

if __name__ == '__main__':
  main()

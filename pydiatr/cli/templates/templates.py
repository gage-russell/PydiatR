import os

from jinja2 import Environment, FileSystemLoader

# current directory of file (this module is inside of the templates directory)
template_dir = os.path.dirname(__file__)
template_loader = FileSystemLoader(template_dir)
template_env = Environment(loader=template_loader)

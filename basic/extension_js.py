from os.path import dirname, join
from jinja2 import Template

class ExtensionGenerator():

    def __init__(self, configuration):
        self.configuration = configuration

    def generate_extension_js(self):
        this_folder = dirname(__file__)
        with open(join(this_folder, 'templates', 'extension.js.template'), 'r') as file:
            data = file.read()
        template = Template(data)
        extension = self.get_data()
        result = template.render(extension)
        result_file = open(join(self.configuration.project_path, 'out', 'src', 'extension.js'), 'w')
        result_file.write(result)

    def get_data(self):
        extension = {
            'name': self.configuration.language_name
        }
        return extension



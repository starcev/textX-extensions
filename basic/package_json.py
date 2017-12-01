from os.path import dirname, join
from jinja2 import Template

class PackageJsonGenerator(object):

    def __init__(self, configuration):
        self.configuration = configuration

    def generate_package_json(self):
        this_folder = dirname(__file__)
        with open(join(this_folder, 'templates', 'package.json.template'), 'r') as file:
            data = file.read()
        template = Template(data)
        package = self.get_data()
        result = template.render(package)
        result_file = open(join(self.configuration.project_path, 'package.json'), 'w')
        result_file.write(result)

    def get_data(self):
        has_publisher = False
        has_author = False
        has_url = False

        name = self.configuration.language_name
        version = self.configuration.version
        publisher = self.configuration.publisher
        author = self.configuration.author
        url = self.configuration.url
        extensions = self.configuration.language_extensions_string
        grammar_path = './coloring/' + name + '.tmLanguage.json'

        if version == None:
            version = "1.0.0"
        if publisher != None:
            has_publisher = True
        if author != None:
            has_author = True
        if url != None:
            has_url = True

        package = {
            'name': name,
            'version': version,
            'publisher': publisher,
            'author': author,
            'url': url,
            'extensions': extensions,
            'grammar_path': grammar_path,
            'has_publisher': has_publisher,
            'has_author': has_author,
            'has_url': has_url
        }
        return package
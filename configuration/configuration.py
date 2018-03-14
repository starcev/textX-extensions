from os.path import join, dirname
from textx.metamodel import metamodel_from_file

class Configuration(object):

    def __init__(self):
        this_folder = dirname(__file__)

        grammar = metamodel_from_file(join(this_folder, 'grammar.tx'), debug=False)
        self.grammar_model = grammar.model_from_file(join(this_folder, '.txconfig'))

    @property
    def language_name(self):
        return self.grammar_model.name

    @property
    def language_extensions(self):
        extensions = []
        for extension in self.grammar_model.extensions:
            extensions.append('.'+extension)
        return extensions

    @property
    def language_extensions_string(self):
        extensions = self.language_extensions
        extensions_string = ""
        extensions_string += "["
        for i, extension in enumerate(extensions):
            extensions_string += "\"" + extension + "\""
            if i < len(extensions)-1:
                extensions_string += ", "
        extensions_string += "]"
        return extensions_string

    @property
    def publisher(self):
        return self.grammar_model.general_section.publisher

    @property
    def url(self):
        return self.grammar_model.general_section.url

    @property
    def author(self):
        return self.grammar_model.general_section.author

    @property
    def version(self):
        return self.grammar_model.general_section.version

    @property
    def grammar_path(self):
        return self.grammar_model.paths_section.grammar_path

    @property
    def coloring_path(self):
        return self.grammar_model.paths_section.coloring_path

    @property
    def outline_path(self):
        return self.grammar_model.paths_section.outline_path

    @property
    def genereting_path(self):
        return self.grammar_model.paths_section.generation_path

    @property
    def project_path(self):
        return join(self.genereting_path, self.language_name)

    @property
    def python_interpreter(self):
        return self.grammar_model.pythonPath.interpreter

    def getValue(self, rule, option):
        for rule_item in self.grammar_model.rules:
            if rule_item.name == rule:
                for option_item in rule_item.options:
                    if option_item.name == option:
                        return option_item.value
        return None
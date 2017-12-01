from os.path import join, dirname, basename
from textx.metamodel import metamodel_from_file
from textx.export import metamodel_export, model_export
from shutil import copyfile

class OutlineVSCode(object):

    def __init__(self, configuration):
        self.configuration = configuration
        self.outline_path = join(self.configuration.project_path, 'out', 'src', 'outline')
        self.this_folder = dirname(__file__)

    def do_outline_for_vscode(self):
        if self.configuration.outline_path == None:
            return
        self.generate_python_interpreter_path()
        self.copy_script()
        self.copy_outline_tx()
        self.copy_outline_program()
        self.copy_language_grammar()
        self.copy_code_outline()
        model = self.get_outline_model()
        self.copy_icons(model)

    def get_outline_model(self):
        this_folder = dirname(__file__)
        language = metamodel_from_file(join(dirname(__file__), 'resources', 'outline.tx'))
        metamodel_export(language, join(dirname(__file__), 'outline.dot'))
        grammar_model = language.model_from_file(self.configuration.outline_path)
        model_export(grammar_model, join(this_folder, 'outline.dot'))
        return grammar_model

    def generate_python_interpreter_path(self):
        with open(join(self.outline_path, 'python_interpreter.txt'), 'w') as file:
            file.write(self.configuration.python_interpreter)

    def copy_script(self):
        copyfile(join(self.this_folder, 'resources', 'script.py'),join(self.outline_path, 'script.py'))

    def copy_outline_tx(self):
        copyfile(join(self.this_folder, 'resources', 'outline.tx'),
                 join(self.outline_path, 'outline.tx'))

    def copy_outline_program(self):
        copyfile(join(self.configuration.outline_path), join(self.outline_path, 'outline.ol'))

    def copy_language_grammar(self):
        with open(self.configuration.grammar_path, 'r') as grammar_file, \
                open(join(self.outline_path, 'language.tx'), 'w') as language_file:
            language_file.write(grammar_file.read())

    def copy_code_outline(self):
        copyfile(join(self.this_folder, 'resources', 'codeOutline.js'),
                 join(self.configuration.project_path, 'out', 'src', 'outline', 'codeOutline.js'))

    def copy_icons(self, model):
        for rule in model.rules:
            name = basename(rule.choices.icon[0].path)
            copyfile(rule.choices.icon[0].path, join(self.configuration.project_path, 'resources', 'icons', name))

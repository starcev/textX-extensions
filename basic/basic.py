from os import makedirs
from os.path import exists, dirname, join
from shutil import copyfile

class BasicGenerator(object):

    def __init__(self,configuration):
        self.configuration = configuration
        self.vscode_path = join(self.configuration.project_path, '.vscode')
        self.this_folder = dirname(__file__)

    def make_folder_structure(self):
        if exists(self.configuration.project_path) == False:
            makedirs(self.configuration.project_path)
            makedirs(join(self.configuration.project_path, '.vscode'))
            makedirs(join(self.configuration.project_path, 'resources'))
            makedirs(join(self.configuration.project_path, 'resources', 'icons'))
            makedirs(join(self.configuration.project_path, 'out'))
            makedirs(join(self.configuration.project_path, 'out', 'src'))
            makedirs(join(self.configuration.project_path, 'out', 'src', 'outline'))
            makedirs(join(self.configuration.project_path, 'coloring'))

    def do_basic_copies(self):
        self.copy_launch_json()
        #self.copy_extension_js()

    def copy_launch_json(self):
        copyfile(join(self.this_folder, 'resources', '.vscode', 'launch.json'),
                 join(self.vscode_path, 'launch.json'))

    #def copy_extension_js(self):
    #    copyfile(join(self.this_folder, 'resources', 'out', 'extension.js.template'),
    #             join(self.configuration.project_path, 'out', 'src', 'extension.js.template'))
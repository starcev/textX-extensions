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
            makedirs(join(self.configuration.project_path, 'resources'))
            makedirs(join(self.configuration.project_path, 'resources', 'icons'))
            makedirs(join(self.configuration.project_path, 'out'))
            makedirs(join(self.configuration.project_path, 'out', 'src'))
            makedirs(join(self.configuration.project_path, 'out', 'src', 'outline'))
            makedirs(join(self.configuration.project_path, 'coloring'))
from coloring.coloring import ColoringVSCode
from configuration.configuration import Configuration
from basic.folder import FolderGenerator
from basic.package_json import PackageJsonGenerator
from basic.extension_js import ExtensionGenerator
from outline.outline import OutlineVSCode

def main(debug=False):

    configuration = Configuration()

    folder = FolderGenerator(configuration)
    folder.make_folder_structure()

    package_json = PackageJsonGenerator(configuration)
    package_json.generate_package_json()

    extension = ExtensionGenerator(configuration)
    extension.generate_extension_js()

    coloring = ColoringVSCode(configuration)
    coloring.do_coloring_for_vscode()

    outline = OutlineVSCode(configuration)
    outline.do_outline_for_vscode()

if __name__ == "__main__":
    main()
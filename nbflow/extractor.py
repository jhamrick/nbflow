import os
import glob
import json
import sys

from nbformat.v4 import reads
from traitlets.config import Application, Unicode

from ._version import __version__


class DependencyExtractor(Application):

    name = Unicode(u'nbflow')
    description = Unicode(u'Extract the hierarchy of dependencies from notebooks in the specified folder.')
    version = __version__

    def extract_parameters(self, nb):
        # find the first code cell
        defs_cell = None
        for cell in nb.cells:
            if cell.cell_type == 'code':
                defs_cell = cell
                break

        if defs_cell is None:
            return {}

        defs_code = defs_cell.source
        globals_dict = {}
        locals_dict = {}
        exec(defs_code, globals_dict, locals_dict)
        return locals_dict

    def resolve_path(self, source, path):
        dirname = os.path.dirname(source)
        return os.path.abspath(os.path.join(dirname, path))

    def get_dependencies(self, dirnames):
        dependencies = {}

        for dirname in dirnames:
            files = glob.glob("{}/*.ipynb".format(dirname))

            for filename in files:
                modname = os.path.splitext(os.path.basename(filename))[0]
                with open(filename, "r") as fh:
                    nb = reads(fh.read())

                params = self.extract_parameters(nb)
                if '__depends__' not in params:
                    continue
                if '__dest__' not in params:
                    raise ValueError("__dest__ is not defined in {}".format(filename))

                # get sources that are specified in the file
                sources = [self.resolve_path(filename, x) for x in params['__depends__']]

                # always depend on util
                sources.append(os.path.abspath("{}/util.py".format(dirname)))

                targets = params['__dest__']
                if not hasattr(targets, '__iter__'):
                    targets = [targets]
                targets = [self.resolve_path(filename, x) for x in targets]

                dependencies['{}/{}.ipynb'.format(dirname, modname)] = {
                    'targets': targets,
                    'sources': sources
                }

        return json.dumps(dependencies, indent=2)

    def start(self):
        if len(self.extra_args) == 0:
            self.log.error("No directory names specified.")
            sys.exit(1)

        print(self.get_dependencies(self.extra_args))


def main():
    DependencyExtractor.launch_instance()

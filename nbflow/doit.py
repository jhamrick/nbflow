from __future__ import print_function

import json
import subprocess as sp
import sys

from .extractor import DependencyExtractor
from ._version import __version__


def build_notebook_cmd(notebook):
    cmd = [
        "jupyter", "nbconvert",
        "--log-level=ERROR",
        "--ExecutePreprocessor.timeout=120",
        "--execute",
        "--inplace",
        "--to", "notebook",
        #"--output", notebook,
        notebook
    ]
    return ' '.join(cmd)


def touch_cmds(target):
    for t in target:
        yield 'touch {0}'.format(str(t))


def get_cmds(notebook, target):
    yield build_notebook_cmd(notebook)
    for cmd in touch_cmds(target):
        yield cmd


def setup(directories):
    parsed = sp.check_output([sys.executable, "-m", "nbflow"] + directories,
                 universal_newlines=True)
    DEPENDENCIES = json.loads(parsed)
    for script in DEPENDENCIES:
        deps = DEPENDENCIES[script]
        sources = deps['sources']
        if len(deps['targets']) == 0:
            #targets = ['.phony_{}'.format(script)]
            targets = []
        else:
            targets = deps['targets']
        
        name = 'build-notebook:{0}'.format(script)
        file_dep = [script] + sources
        actions = list(get_cmds(script, targets))
        
        yield {'name': name,
               'actions': actions,
               'targets': targets,
               'file_dep': file_dep,
               'clean': True}


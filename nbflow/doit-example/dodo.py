import os
from nbflow.doit import create_build_tasks

def task_nbflow():
    yield from create_build_tasks(['analyses'])

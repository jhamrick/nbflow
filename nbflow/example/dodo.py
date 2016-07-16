import os
from nbflow import doit

def task_nbflow():
    for task in doit.setup(['analyses']):
        yield task

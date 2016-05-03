import json
import sys
import subprocess as sp


def build_notebook(target, source, env):
    notebook = str(source[0])
    cmd = [
        "jupyter", "nbconvert",
        "--log-level=ERROR",
        "--ExecutePreprocessor.timeout=120",
        "--execute",
        "--inplace",
        "--to", "notebook",
        "--out", notebook,
        notebook
    ]
    code = sp.call(cmd)
    if code != 0:
        raise RuntimeError("Error executing notebook")

    # we need to touch each of the targets so that they have a later
    # modification time than the source -- otherwise scons will think that the
    # targets always are out of date and need to be rebuilt
    for t in target:
        sp.call(["touch", str(t)])

    return None


def print_cmd_line(s, targets, sources, env):
    """s       is the original command line string
       targets is the list of target nodes
       sources is the list of source nodes
       env     is the environment"""
    if len(targets) == 0:
        sys.stdout.write("%s --> None\n"% str(sources[0]))
    else:
        for target in targets:
            if str(target).startswith('.phony'):
                target = 'None'
            sys.stdout.write("%s --> %s\n"% (str(sources[0]), str(target)))


def setup(env, directories):
    env['PRINT_CMD_LINE_FUNC'] = print_cmd_line
    env.Decider('timestamp-newer')
    DEPENDENCIES = json.loads(sp.check_output([sys.executable, "-m", "nbflow"] + directories))
    for script in DEPENDENCIES:
        deps = DEPENDENCIES[script]
        if len(deps['targets']) == 0:
            targets = ['.phony_{}'.format(script)]
        else:
            targets = deps['targets']
        env.Command(targets, [script] + deps['sources'], build_notebook)

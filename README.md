# NBFlow

[![Build Status](https://travis-ci.org/jhamrick/nbflow.svg?branch=master)](https://travis-ci.org/jhamrick/nbflow)  [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/jhamrick/nbflow/master)

A tool that supports one-button reproducible workflows with the Jupyter Notebook and Scons. **Note: this currently  only supports Python kernels.**

> **UPDATE: Scons >= 3.0.0 now supports Python 3 so Python 2 isn't needed anymore!** Now Nbflow and Scons are both Python 2 and 3 compatible so you can choose whichever you want.

> The actual version of Scons (3.0.1) currently supports Python >= 3.5, which is the default in Ubuntu 16.04

## Installation

To install, run:

Linux:
```
pip3 install git+git://github.com/jhamrick/nbflow.git
```

Windows:
```
pip install git+git://github.com/jhamrick/nbflow.git
```

## Usage

For a complete example of how to use nbflow, check out [the example](nbflow/example)
in this repository.

You can now you Binder to check the example online:

1. Entre in Binder [here](https://mybinder.org/v2/gh/jhamrick/nbflow/master) or through the badge above
2. Open a terminal
3. Run `cd nbflow/example`
4. Run `scons`
5. Check the results in the `results` directory

Optionally you can modify the notebook in this online environment and check how the results change.

### Analysis notebooks

For each notebook that you want executed, you MUST include two special variables
in the first code cell:

* `__depends__` -- a list of relative paths to files that the notebook depends
  on
* `__dest__` -- either a relative path, or list of relative paths, to files that
  the notebook produces

For example, the first cell in [one of the example notebooks](nbflow/example/analyses/analyze_data.ipynb)
is:

```python
__depends__ = ["../results/data.json"]
__dest__ = "../results/stats.json"
```

### SConstruct file

You need a `SConstruct` file in the root of you analysis directory. In this
`SConstruct` file you will need to import nbflow and use it to setup your scons
environment, e.g.:

```python
import os
from nbflow.scons import setup

env = Environment(ENV=os.environ)
setup(env, ["analyses"])
```

The second argument of the `setup` command takes a list of folder names that
contain analysis notebooks.

### Running nbflow

Once you have setup your analysis notebooks and your `SConstruct` file, you can
run your notebooks by just running the `scons` command from the root of your
analysis directory.

import sys
import os

from textwrap import dedent
from .util import run_command


def test_nbflow_command(temp_cwd):
    run_command([sys.executable, "-m", "nbflow"], retcode=1)
    output = run_command([sys.executable, "-m", "nbflow", "analyses"])
    expected = dedent(
        """
        {
          "analyses/analyze_data.ipynb": {
            "sources": [
              "%(path)s/results/data.json"
            ], 
            "targets": [
              "%(path)s/results/stats.json"
            ]
          }, 
          "analyses/gen_data.ipynb": {
            "sources": [], 
            "targets": [
              "%(path)s/results/data.json"
            ]
          }
        }
        """ % dict(path=os.path.abspath(os.path.realpath(temp_cwd)))
    ).lstrip()
    assert output == expected


def test_scons(temp_cwd):
    output = run_command(["scons"]).replace("\x1b[?1034h", "")
    expected = dedent(
        """
        scons: Reading SConscript files ...
        scons: done reading SConscript files.
        scons: Building targets ...
        analyses/gen_data.ipynb --> results/data.json
        analyses/analyze_data.ipynb --> results/stats.json
        scons: done building targets.
        """
    ).lstrip()

    assert output == expected

    output = run_command(["scons", "-n"]).replace("\x1b[?1034h", "")
    expected = dedent(
        """
        scons: Reading SConscript files ...
        scons: done reading SConscript files.
        scons: Building targets ...
        scons: `.' is up to date.
        scons: done building targets.
        """
    ).lstrip()

    assert output == expected

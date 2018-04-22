import pytest
import os
import tempfile
import shutil
from textwrap import dedent


@pytest.fixture
def temp_cwd(request):
    orig_dir = os.getcwd()
    path = tempfile.mkdtemp()
    os.chdir(path)

    def fin():
        os.chdir(orig_dir)
        shutil.rmtree(path)
    request.addfinalizer(fin)

    return path


@pytest.fixture
def sconstruct(temp_cwd):
    with open("SConstruct", "w") as fh:
        fh.write(dedent(
            """
            import os
            from nbflow.scons import setup

            env = Environment(ENV=os.environ)
            setup(env, ["."], ARGUMENTS)
            """
        ))

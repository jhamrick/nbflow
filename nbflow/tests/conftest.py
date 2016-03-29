import pytest
import os
import tempfile
import shutil
from .util import clear_notebooks


@pytest.fixture
def temp_cwd(request):
    orig_dir = os.getcwd()
    path = tempfile.mkdtemp()
    os.chdir(path)

    # copy example files
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "example"))
    shutil.copytree(os.path.join(root, "analyses"), "analyses")
    shutil.copy(os.path.join(root, "SConstruct"), "SConstruct")
    clear_notebooks("analyses")

    def fin():
        os.chdir(orig_dir)
        shutil.rmtree(path)
    request.addfinalizer(fin)

    return path

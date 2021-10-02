import os
import subprocess

def test_script():
    os.system(r"tests\test_script.py")

    assert os.path.isfile("course.json")


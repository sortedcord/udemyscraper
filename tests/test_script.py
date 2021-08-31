import os

def test_script():
    os.exec("tests/test_script.bat")

    assert os.path.isfile("course.json")
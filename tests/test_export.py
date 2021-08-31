from udemyscraper import UdemyCourse
from udemyscraper.export import export_course

global formats
formats = ['xml', 'json', 'csv']

import os, shutil


def main():
    course = UdemyCourse({'cache':True, 'cache_dir':'.udscraper_cache_test'})
    course.fetch_course("learn python")
    return course


def test_export_default():
    course = main() #Get course

    for format in formats:
        if format == "csv":
            course = [course]

        export_course(course, formats)
        assert os.path.isfile(f'course.{format}')
        shutil.rmtree(f'course.{format}')


def test_export_custom():
    course = main() #Get course

    for format in formats:
        if format == "csv":
            course = [course]

        export_course(course, formats, f"mycustomexport.{format}")
        assert os.path.isfile(f'course.{format}')
        shutil.rmtree(f'course.{format}')




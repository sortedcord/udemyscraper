from udemyscraper import UdemyCourse
from udemyscraper.export import export_course
from udemyscraper.utils import random_search_query

global formats
formats = ['xml', 'json', 'csv']

import os, shutil



def main():
    course = UdemyCourse({'cache':True, 'cache_dir':'.udscraper_cache_test'})
    course.fetch_course(random_search_query())
    return course


def test_export_default():
    for format in formats:
        course = main() #Get course
        if format == "csv":
            course = [course]

        export_course(course, format)
        assert os.path.isfile(f'course.{format}')
        os.remove(f'course.{format}')


def test_export_custom():
    for format in formats:
        course = main() #Get course
        if format == "csv":
            course = [course]

        export_course(course, format, f"mycustomexport.{format}")
        assert os.path.isfile(f'mycustomexport.{format}')
        os.remove(f'mycustomexport.{format}')




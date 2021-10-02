import os
import shutil

import time

from udemyscraper import UdemyCourse
from udemyscraper.utils import random_search_query

fixed_course_name = random_search_query()

def test_udemyscraper_no_params():
    course = UdemyCourse()
    course.fetch_course(fixed_course_name)
    assert course.title != ""


def test_udemyscraper_cache():
    if os.path.isdir('.udscraper_cache/'):
        # Clears out existing cache
        shutil.rmtree('.udscraper_cache/')

    start_time = time.time()
    course = UdemyCourse({'cache':True})
    course.fetch_course(fixed_course_name)
    exec_time1 = time.time() - start_time

    #Check for cache files
    assert os.path.isdir('.udscraper_cache/')
    assert os.path.isfile('.udscraper_cache/query.txt')
    assert os.path.isfile('.udscraper_cache/course.html')
    assert os.path.isfile('.udscraper_cache/search.html')

    # Check 2 (If cache files are being used after generation)
    start_time = time.time()
    course = UdemyCourse({'cache':True})
    course.fetch_course(fixed_course_name)
    exec_time2 = time.time() - start_time

    assert exec_time2 <= exec_time1
    # If less time is taken the second time then that means cache files are being used


    mycourse = UdemyCourse({'cache': True})
    mycourse.fetch_course(fixed_course_name)
    assert mycourse.title != ""

    # Check if cache files have been updated.
    with open('.udscraper_cache/query.txt') as file:
        query = file.read()
    assert fixed_course_name in query


    #clear cache
    shutil.rmtree('.udscraper_cache/')
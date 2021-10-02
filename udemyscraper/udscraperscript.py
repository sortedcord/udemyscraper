import time

import os

from alive_progress import alive_bar
from logging import *
import getopt
import sys


from udemyscraper import UdemyCourse
from udemyscraper.metadata import __version__
from udemyscraper.utils import display_help, loginfo, print_logo
from udemyscraper.export import export_course

def main():
    __starttime__ = time.time()
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "q:hvnb:l:d:o:e:tc:"

    # Long options
    long_options = [
        "query=", "help", "version", "no-warn", "browser=", "headless=", "dump=", 
        "output=", "debug=", "quiet", "time=", "progress=", "cache=", "cache_dir=",
    ]

    # Tool Defaults
    Preferences = {
        'warn': True,
        'browser': "chrome",
        'headless': True,
        'dump_format': None,
        'output_file': "",
        'debug': False,
        'quiet': False,
        'time': True,
        'progress': True,
        'cache': False,
        'cache_dir': '.udscraper_cache',
    }

    search_query = "" # What udscraper will search for in the serarch bar

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument

        for currentArgument, currentValue in arguments:

            # Help argument
            if currentArgument in ("-h", "--help"):
                display_help()
                exit()

            # Version argument
            elif currentArgument in ("-v", "--version"):
                print(f"udemyscraper {__version__} (cli)", "\n")
                exit()

            # Disable warning
            elif currentArgument in ("-n", "--no-warn"):
                Preferences['warn'] = False

            # Search query
            elif currentArgument in ("-q", "--query"):
                search_query = currentValue

            # Select Browser
            elif currentArgument in ("-b", "--browser"):
                Preferences["browser"] = currentValue.lower()

            # Disable/Enable headless
            elif currentArgument in ("-l", "--headless"):
                if currentValue.lower() == "true":
                    Preferences['headless'] = True
                elif currentValue.lower() == "false":
                    Preferences['headless'] = False
                else:
                    print(
                        "\n", "headless takes either of the two values: True or False.")

            # Select dump format
            elif currentArgument in ("-d", "--dump"):
                Preferences['dump_format'] = currentValue


            # Specify output file
            elif currentArgument in ("-o", "--output"):
                Preferences['output_file'] = currentValue

            # Enable Debug Logging
            elif currentArgument in ("-e", "--debug"):
                if currentValue.lower == "true":
                    Preferences['debug'] = True
                elif currentValue.lower == "false":
                    Preferences['debug'] = False
                elif currentValue.lower == "info":
                    Preferences['debug'] = "info"
                elif currentValue.lower == "debug":
                    Preferences['debug'] = True

            # Enable quiet mode
            elif currentArgument in ("--quiet"):
                Preferences['quiet'] = True
                Preferences['progress'] = False

            # Disable time taken
            elif currentArgument in ("-t", "--time"):
                Preferences['time'] = False

            # Toggle Progressbar
            elif currentArgument in ("--progress"):
                if currentValue == "true":
                    Preferences['progress'] = True
                if currentValue == "false":
                    Preferences['progress'] = False

            # Enable cache
            elif currentArgument in ("-c", "--cache"):
                if currentValue == 'true':
                    Preferences['cache'] = True
                elif currentValue == "clear":
                    Preferences['cache'] = 'clear'
                elif currentValue == '':
                    Preferences['cache'] = True
                elif currentValue == "false":
                    Preferences['cache'] = False
            
            #Change Cache directory
            elif currentArgument in ("--cache_dir"):
                Preferences['cache_dir'] = currentValue

    except getopt.error as err:
        # output error, and return with an error code
        # if there is some error with system args
        print(str(err))

    # Logo and others will be printed as long as quiet mode is turned off
    if Preferences['quiet'] == False:
        print_logo()

        print(f"Version: {__version__}")
        loginfo(f"Using Preferences: {Preferences}")

    if search_query == "":
        search_query = input("Enter the search query: ")
    else:
        if Preferences['quiet'] == False:
            print(f"Search with query: {search_query}")
    
    # Check if the given search query is a valid file or not
    if '.txt' in search_query and os.path.isfile(search_query):
        with open(search_query) as query_file:
            search_query = [] # Convert search query to a list
            # Read the query file
            for query in query_file.readlines():
                query = query.replace("\n", "")
                search_query.append(query)
            
    else:
        search_query = [search_query]
    courses = []

    for query in search_query:
        
        course = UdemyCourse(Preferences)

        if Preferences['quiet'] == False or Preferences['progress'] == True:
            with alive_bar(title="Scraping Course", bar="smooth") as abar:
                course.fetch_course(query, abar)
        else:
            course.fetch_course(query,)
        courses.append(course)
    

    time.sleep(5)

    if Preferences['dump_format'] == "csv":
        course = courses
        export_course(course, Preferences['dump_format'], Preferences['output_file'])

    elif Preferences['dump_format'] == 'json' or Preferences['dump_format'] == 'xml' and 'list' in str(type(course)):
        os.mkdir('UdemyBulkExport')
        for course, query in courses, search_query:
            export_course(course, Preferences['dump_format'], f"UdemyBulkExport/ {query}")
    else:
        export_course(course, Preferences['dump_format'], Preferences['output_file'])

    if Preferences['quiet'] == False or Preferences['time'] == True:
        print('It took', time.time()-__starttime__, 'seconds.')

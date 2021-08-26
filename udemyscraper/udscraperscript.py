import time

from alive_progress import alive_bar
from logging import *
import getopt
import sys
from colorama import Fore, Style
from udemyscraper.output import *

from udemyscraper import *
from udemyscraper.metadata import __version__
from udemyscraper.utils import display_help

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
        "output=", "debug=", "quiet", "time=", "progress=", "cache="
    ]

    # Tool Defaults
    Preferences = {
        'warn': True,
        'browser_preference': "CHROME",
        'headless': True,
        'dump_format': None,
        'output_file': "",
        'debug': False,
        'quiet': False,
        'time': True,
        'progress': True,
        'cache': False
    }

    search_query = ""

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        print(arguments, values)
        print(arguments, values)
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
                if currentValue.lower() == "chrome" or currentValue.lower() == "chromium":
                    Preferences['browser_preference'] = "CHROME"
                elif currentValue.lower() == "firefox":
                    Preferences['browser_preference'] = "FIREFOX"

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
                if currentValue.lower() == 'json':
                    Preferences['dump_format'] = "json"
                    Preferences['output_file'] = 'course.json'
                elif currentValue.lower() == 'xml':
                    Preferences['dump_format'] = "xml"
                    Preferences['output_file'] = 'course.xml'
                elif currentValue.lower() == 'csv':
                    Preferences['dump_format'] = "csv"
                    Preferences['output_file'] = 'course.csv'
                else:
                    print(currentValue, " is not a valid dump format.")

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
                if currentValue.lower() == "true":
                    Preferences['progress'] = True
                if currentValue.lower() == "false":
                    Preferences['progress'] = False

            # Enable cache
            elif currentArgument in ("-c", "--cache"):
                print(currentValue, currentValue, currentValue)
                if str(currentValue) == "":
                    Preferences['cache'] = True
                elif str(currentValue) == "clear":
                    Preferences['cache'] = 'clear'

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    if Preferences['quiet'] == False:
        print(Fore.MAGENTA + """
    ██╗   ██╗██████╗ ███████╗███╗   ███╗██╗   ██╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗
    ██║   ██║██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██║   ██║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝     ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║   ██║       ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
    ╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝""")
        print(Style.RESET_ALL)

        print(f"Version: {__version__}")
        print(f"Using Preferences: {Preferences}")

    if search_query == "":
        search_query = input("Enter the search query: ")
    else:
        if Preferences['quiet'] == False:
            print(f"Search with query: {search_query}")
    print(Preferences)
    course = UdemyCourse(Preferences)

    if Preferences['quiet'] == False or Preferences['progress'] == True:
        with alive_bar(title="Scraping Course", bar="smooth") as abar:
            course.fetch_course(search_query, abar)
    else:

        course.fetch_course(search_query,)

    if Preferences['dump_format'] != None:
        if Preferences['dump_format'] == 'json':
            course_to_json(course, Preferences['output_file'])
        elif Preferences['dump_format'] == 'csv':
            print("\n", "WARN: 'CSV' dump format is currently not supported.")
        elif Preferences['dump_format'] == 'xml':
            print("\n", "WARN: 'XML' dump format is currently not supported.")
    else:
        quick_display(course)

    if Preferences['quiet'] == False or Preferences['time'] == True:
        print('It took', time.time()-__starttime__, 'seconds.')

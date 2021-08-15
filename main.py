from udemyscraper import *
import getopt
import sys


# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hvnq:b:l:d:o:"

# Long options
long_options = ["help", "version", "no-warn",
                "query", "browser", "headless", "dump", "output"]

# Tool Defaults
warn = True
search_query = ""
browser_preference = "CHROME"
headless = True
dump = ""
output = "course.json"


try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--help"):
            with open('texts/help.txt') as file:
                lines = file.readlines()
                for line in lines:
                    print(line.replace("\n", ""))
                    time.sleep(0.1)

        elif currentArgument in ("-v", "--version"):
            print("Udemyscraper version 0.0.4", "\n")

        elif currentArgument in ("-n", "--no-warn"):
            warn = False

        elif currentArgument in ("-q", "--query"):
            search_query = currentValue

        elif currentArgument in ("-b", "--browser"):
            if currentValue.lower() == "chrome" or currentValue.lower() == "chromium":
                browser_preference = "CHROME"
            elif currentValue.lower() == "firefox":
                browser_preference = "FIREFOX"

        elif currentArgument in ("-l", "--headless"):
            if currentValue.lower() == "true":
                headless = True
            elif currentValue.lower() == "false":
                headless = False
            else:
                print("\n", "headless takes either of the two values: True or False.")
        elif currentArgument in ("-d", "--dump"):
            if currentValue.lower() == 'json':
                dump = "json"
            elif currentValue.lower() == 'xml':
                dump = "xml"
            elif currentValue.lower() == 'csv':
                dump = "csv"
            else:
                print(currentValue, " is not a valid dump format.")
        elif currentArgument in ("-o", "--output"):
            output = currentValue


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if search_query == "":
    search_query = input("Enter the search query: ")
course = UdemyCourse(search_query, warn, browser_preference, headless)
course.fetch_course()

if dump != "":
    if dump == "json":
        course_to_json(course, output)
    elif dump == "csv":
        print("I'm working on it :P")
    elif dump == "xml":
        course_to_xml(course,)

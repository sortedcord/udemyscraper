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
Options = {
    'warn': True,
    'browser_preference': "CHROME",
    'headless': True,
    'dump_format': "",
    'output_file': ""

}

search_query = ""

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
                exit()

        elif currentArgument in ("-v", "--version"):
            print("Udemyscraper version 0.0.4", "\n")
            exit()

        elif currentArgument in ("-n", "--no-warn"):
            Options['warn'] = False

        elif currentArgument in ("-q", "--query"):
            search_query = currentValue

        elif currentArgument in ("-b", "--browser"):
            if currentValue.lower() == "chrome" or currentValue.lower() == "chromium":
                Options['browser_preference'] = "CHROME"
            elif currentValue.lower() == "firefox":
                Options['browser_preference'] = "FIREFOX"

        elif currentArgument in ("-l", "--headless"):
            if currentValue.lower() == "true":
                Options['headless'] = True
            elif currentValue.lower() == "false":
                Options['headless'] = False
            else:
                print("\n", "headless takes either of the two values: True or False.")
        elif currentArgument in ("-d", "--dump"):
            if currentValue.lower() == 'json':
                Options['dump_format'] = "json"
                Options['output_file'] = 'course.json'
            elif currentValue.lower() == 'xml':
                Options['dump_format'] = "xml"
                Options['output_file'] = 'course.xml'
            elif currentValue.lower() == 'csv':
                Options['dump_format'] = "csv"
                Options['output_file'] = 'course.csv'
            else:
                print(currentValue, " is not a valid dump format.")
        elif currentArgument in ("-o", "--output"):
            Options['output_file'] = currentValue


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if search_query == "":
    search_query = input("Enter the search query: ")
course = UdemyCourse(search_query, Options)
course.fetch_course()


if Options['dump_format'] != "":
    if Options['dump_format'] == 'json':
        course_to_json(course, Options['output_file'])
    elif Options['dump_format'] == 'csv':
        print("\n", "WARN: 'CSV' dump format is currently not supported.")
    elif Options['dump_format'] == 'xml':
        print("\n", "WARN: 'XML' dump format is currently not supported.")

from udemyscraper import *
import getopt
import sys


# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hvnq:"

# Long options
long_options = ["help", "version", "no-warn", "query"]

# Tool Defaults
warn = True
search_query = ""

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)

    # checking each argument
    for currentArgument, currentValue in arguments:

        if currentArgument in ("-h", "--help"):
            with open('help.txt') as file:
                lines = file.readlines()
                for line in lines:
                    print(line.replace("\n", ""))
                    time.sleep(0.1)

        elif currentArgument in ("-v", "--version"):
            print("Udemyscraper version 0.0.3", "\n")

        elif currentArgument in ("-n", "--no-warn"):
            warn = False

        elif currentArgument in ("-q", "--query"):
            search_query = currentValue


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if search_query == "":
    search_query = input("Enter the search query: ")
course = UdemyCourse(search_query, warn)
course.fetch_course()

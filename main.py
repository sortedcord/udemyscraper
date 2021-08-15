from udemyscraper import *
import getopt
import sys


# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hvnq:b:l:"

# Long options
long_options = ["help", "version", "no-warn", "query", "browser", "headless"]

# Tool Defaults
warn = True
search_query = ""
browser_preference = "CHROME"
headless = True


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


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))

if search_query == "":
    search_query = input("Enter the search query: ")
course = UdemyCourse(search_query, warn, browser_preference, headless)
course.fetch_course()

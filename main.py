from udemyscraper import *
import getopt
import sys

warn = True

# Remove 1st argument from the
# list of command line arguments
argumentList = sys.argv[1:]

# Options
options = "hvn"

# Long options
long_options = ["help", "version", "no-warn"]

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


except getopt.error as err:
    # output error, and return with an error code
    print(str(err))


course = UdemyCourse(input("Enter search query: "), warn)
course.fetch_course()

import logging
import time

from udemyscraper.metadata import __version__


def loginfo(message):
    # Logs the message along with the time taken from the start
    logging.info(str(time.time()) + '  ' + message)


def display_warn():
    loginfo("Displaying warning")
    print("""
Thank You for using udemyscraper

Before fetching the course information be sure that 
you have google chrome >= 92.x.x installed on your machine. 
Support for other chromium based browsers such as brave, edge, 
opera, vivaldi, etc has not been implemented yet.

This tool is only meant to be used for educational purposes. 
Please do not abuse it as rate limits might still apply.

Happy Scraping!
~ Sortedcord
""")


def display_help():
    loginfo("Displaying help")
    print(f"""
udemyscraper {__version__} (cli)
Usage: udemyscraper [options] command

udemyscraper is a free and open source tool, 
that fetches udemy course information. Get udemy course 
information and convert it to json, csv or xml file, 
without authentication.

Most Used Commands:

    -h  --help          Displays information about udemyscraper and its usage
    -v  --version       Displays the version of the tool
    -n  --no-warn       Disables the warning when initializing the udemyscourse class
    -q  --query         You can pass the search query directly. If the search query
                        is of multiple words then be sure to enclose the entire string
                        in quotes.
    -b  --browser       Allows you to select the browser you would like to use for Scraping
                        Values: "chrome" or "firefox". Defaults to chrome if no argument is passed.
    -l  --headless      Can be used to disable/enable suppressing of the browser. Can be set to `true`
                        or `false`. Defaults to `true` if no argument is passed.
    -d  --dump          Dump the course object to the specified format. Available formats current 
                        include `json`
    -o  --output        Output the course object to the specified format. Deafults to 'output.json` for 
                        json.
    -e  --debug         Enable Debug Logging. Takes value as 'False', 'True', 'info' and 'debug'.
                        Check this page for more info - https://do.co/2WpLh8T
        --quiet         Disables the logo and the intro when running the `main.py` file.
    -t  --time          Displays the time taken for the entire script to run. Is enabled by default when
                        quiet mode is disabled. 
        --progress      Toggle the progressbar. It is enabled by default when run as a script and disabled
                        when quite mode is enabled.
    -c  --cache         Can have the value of true, false and clear.  
""")

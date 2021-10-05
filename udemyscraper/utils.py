import logging
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium import webdriver  # for webdriver

from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge

from udemyscraper.metadata import __version__

import platform

from colorama import Fore, Style

from random import randint

__illegal_dir__ = ["CON", "PRN", "AUX", 'NUL', 'COM1', 'COM2', 
                    'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 
                    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 
                    'LPT8', 'LPT9']

def loginfo(message):
    # Logs the message along with the time taken from the start
    logging.info(str(time.time()) + '  ' + message)


def display_warn():
    loginfo("Displaying warning")
    print("""
Thank You for using udemyscraper

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

def print_logo():
    print(Fore.MAGENTA + """
██╗   ██╗██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗
██║   ██║██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║   ██║██║  ██║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║   ██║██║  ██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╔╝██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝ ╚═════╝  ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝""")
    print(Style.RESET_ALL)


def set_browser(Preferences):
    if 'chrom' in Preferences['browser']:
        # Preferences['browser'] Options
        option = Options()
        if Preferences['headless'] == True:
            option.add_argument('headless')
            loginfo("Headless enabled")
        option.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        try:
            browser = webdriver.Chrome(options=option)
        except ValueError:
            print(
                f"{Preferences['browser']} could not be found. Make sure you have it installed in your machine.")
            exit()
        
    elif Preferences['browser'] == "edge":
        option = EdgeOptions()
        option.use_chromium = True
        if Preferences['headless'] == True:
            option.add_argument('headless')
            option.add_argument('disable-gpu')
            loginfo("Headless enabled")

        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        try:
            browser = Edge(options=option)
        except ValueError:
            print(
                f"{Preferences['browser']} could not be found. Make sure you have it installed in your machine.")
        
    
    elif Preferences['browser'] == "brave":
        if platform.system() == "Windows":
            brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        elif platform.system() == "Linux":
            brave_path = '/usr/bin/brave-browser'
        option = webdriver.ChromeOptions()
        option.binary_location = brave_path
        if Preferences['headless'] == True:
            option.add_argument('headless')
        browser = webdriver.Chrome(chrome_options=option)

    elif Preferences['browser'] == "firefox":
        fireFoxOptions = webdriver.FirefoxOptions()
        if Preferences['headless'] == True:
            loginfo("Headless enabled")
            fireFoxOptions.set_headless()
        try:
            browser = webdriver.Firefox(firefox_options=fireFoxOptions)
        except WebDriverException:
            print("Geko driver not found. Make sure it is in your path")
            exit()
    else:
        print(f"""{Preferences['browser']} is not a valid browser or is not
implemented yet. Please read the documentation and use the browsers
mentioned there. Exiting""")
        exit()

    return browser

def random_search_query():
    query_list = [
        'Learn how to invest in stocks',
        'Good artist drawings',
        'How to learn blender',
        "How to meake money easily",
        "Chemistry research",
        "Oauth 2.0",
        "Python for data science",
        "How to use unreal engine",
        "Unity Level Management"
    ]
    return query_list[randint(0,len(query_list)-1)]

import time
__starttime__ = time.time()

from alive_progress import alive_bar

# Selenium Libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # to wait until page loads
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium import webdriver  # for webdriver

from bs4 import BeautifulSoup
import json
import logging
from logging import *
import getopt
import sys, os
from colorama import Fore, Style
from pathlib import Path
import shutil

__version__ = "0.7.4"


def loginfo(message):
    # Logs the message along with the time taken from the start
    logging.info(str(time.time()-__starttime__) + '  ' + message)


def quick_display(course):
    print("===================== Fetched Course =====================", "\n")
    print(course.title)
    print(course.headline)
    print(f"URL: {course.link}")
    print(f"Instructed by {course.instructors}")
    print(f"{course.rating} out of 5 ({course.no_of_ratings})")
    print(f"Duration: {course.duration}")
    print(f"{course.no_of_lectures} Lessons and {course.no_of_sections} Sections")


def display_warn():
    loginfo("Displaying warning")
    print("""
Thank You for using udemyscraper

Before fetching the course information be sure that 
you have google chrome >= 92.x.x installed on your machine. 
Other chromium based browsers such as brave, edge, 
opera, vivaldi, etc will not work.

This tool is only meant to be used for educational purposes. 
Please do not abuse it as rate limits might still apply.

Happy Scraping!
~ Sortedcord
""")


def display_help():
    loginfo("Displaying help")
    print(f"""
udemyscraper {__version__} (cli)
Usage: udemyscraper.py [options] command

udemyscraper is a free and open source tool beautiful soup, 
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
""")

# Section class will contain an array with lesson classes


class Lesson():
    def __init__(self, lesson_html):
        # Since the structure of previewable
        # lessons is different from that of the
        # ones that are not:

        if "Preview" in lesson_html.select_one("div").text:
            self.demo = True
            self.title = lesson_html.select_one(
                "button").text
        else:
            self.demo = False
            self.title = lesson_html.select_one(
                "span[class*='section--item-title--']").text

        # Fetches the type of the lesson
        if "play" in str(lesson_html.select_one("use").attrs['xlink:href']):
            self.type = "Video"
            self.duration = lesson_html.select_one(
                "span[class*='section--hidden-on-mobile--171Q9 section--item-content-summary--']").text
        elif "quiz" in str(lesson_html.select_one("use").attrs['xlink:href']):
            self.type = "quiz"
            self.duration = None
        elif "article" in str(lesson_html.select_one("use").attrs['xlink:href']) == "#icon-article":
            self.type = "article"
            self.duration = lesson_html.select_one(
                "span[class*='section--hidden-on-mobile--171Q9 section--item-content-summary--']").text


# Course class will contain an array with section classes
class Section():
    def __init__(self, section_html):
        self.name = section_html.select_one(
            "span[class*='section--section-title--']").text
        loginfo("Scraped name")

        self.duration = section_html.select_one(
            "span[data-purpose='section-content']").text.split(' • ')[1].replace(' ', '')
        loginfo('Scraped Section duration')

        self.Lessons = []

        for lesson in section_html.select("ul > li > div"):
            self.Lessons.append(Lesson(lesson))
            loginfo(
                f"Lesson {len(self.Lessons)} scraped successfully")


        self.no_of_lessons = len(self.Lessons)
        self.duration = section_html.select_one(
            "span[data-purpose='section-content']").text.split(" • ")[1].replace(" ", "")


class UdemyCourse():
    def __init__(self, Preferences={
        'warn': True,
        'browser_preference': "CHROME",
        'headless': True,
        'debug': False,
        'quiet': False,
        'time': True,
        'cache' : False
    }):  # Set default preferences when none provided
        self.Preferences = Preferences

        if self.Preferences['warn'] == True:
            display_warn()

        if Preferences['debug'] == True:
            logging.basicConfig(level=logging.DEBUG)
        elif Preferences['debug'] == "info":
            logging.basicConfig(level=logging.INFO)

    def fetch_course(self, query):
        loginfo("Setting Dummy Functions for Bar")
        loginfo("")
        def br(message=None):
            if message is None:
                abar()
            else:
                abar.text(message)

        try:
            abar()
        except NameError:
            loginfo("Alive bar is not being used")
            def br(message=None):
                pass
        
        loginfo("Searching for cache file")
        cache_file = os.path.isfile('.udscraper_cache/query.txt')
        br('Checking if Cache files exists')
        if Preferences['cache'] == True and cache_file:
            loginfo("Cache files exists")
            with open('.udscraper_cache/query.txt') as query_file:
                br('Reading Cache files')
                loginfo("Reading cache files")
                old_query = query_file.read()
            if query != str(old_query):
                br('Flushing cache files as query is different')
                loginfo("Deleting cache folder")
                shutil.rmtree('.udscraper_cache/')
                Preferences['cache'] == True
                cache_file = os.path.isfile('.udscraper_cache/query.txt')

        #Check if cache exists
        if Preferences['cache'] == 'clear' or Preferences['cache'] == False or (Preferences['cache'] == True and cache_file == False):
            if Preferences['cache'] == 'clear':
                br('Flushing cache files')
                shutil.rmtree('.udscraper_cache/')
                loginfo("Cache folder deleted")
                Preferences['cache'] == True
                br()


            if Preferences['cache'] == True:
                br('Created cache files')
                os.mkdir('.udscraper_cache')
                loginfo("Created cache folder")
                br()

            # Get the url of the search query
            url = "https://www.udemy.com/courses/search/?src=ukw&q=" + query
            if Preferences['cache'] == True:
                br('Dumping query text')
                with open('.udscraper_cache/query.txt', 'w', encoding="utf-8") as file:
                    loginfo("Writing query text file")
                    file.write(query)
                br()

            br('Launching Browser')
            loginfo("Setting Up browser headers and preferences")
            if self.Preferences['browser_preference'] == "CHROME":
                # Browser Options
                option = Options()
                if self.Preferences['headless'] == True:
                    option.add_argument('headless')
                    loginfo("Headless enabled")
                option.add_experimental_option(
                    'excludeSwitches', ['enable-logging'])
                try:
                    browser = webdriver.Chrome(options=option)
                except ValueError:
                    print(
                        f"{self.Preferences['browser_preference']} could not be found. Make sure you have google chrome installed in your machine.")
                br()

            elif self.Preferences['browser_preference'] == "FIREFOX":
                fireFoxOptions = webdriver.FirefoxOptions()
                if self.Preferences['headless'] == True:
                    loginfo("Headless enabled")
                    fireFoxOptions.set_headless()
                try:
                    browser = webdriver.Firefox(firefox_options=fireFoxOptions)
                except WebDriverException:
                    print("Geko driver not found. Make sure it is in your path")
                    exit()
                br()

            br('Loading Udemy Search page')
            loginfo(
                "Redirecting to the searchpage")
            browser.get(url)
            br()

            br('Waiting for search results')
            # Wait until the search box loads
            try:
                loginfo(
                    "Waiting for the browser to load the search results. This depends on your network responsiveness")
                element_present = EC.presence_of_element_located(
                    (By.XPATH, "//div[starts-with(@class, 'course-directory--container--')]"))
                WebDriverWait(browser, 25).until(element_present)
            except TimeoutException:
                print(
                    "Timed out waiting for page to load or could not find a matching course")
                exit()
            loginfo("Search results found")
            br()

            br('Extracting Page Source')
            # Get page source
            content = browser.page_source
            if self.Preferences['cache'] == True:
                with open('.udscraper_cache/search.html', 'w', encoding="utf-8") as file:
                        file.write(content)
            loginfo("Fetched page source")

            #Parse HTML
            search_page = BeautifulSoup(content, "lxml")
            loginfo("Page source parsed")
            br()

            br('Getting Course Link')
            # Get course link
            self.link = 'https://udemy.com' + search_page.select_one(
                'div[class="course-list--container--3zXPS"] > div > a[tabindex="0"]')['href']
            loginfo("Found course link")

            # Scrape Information on course_page
            loginfo("Redirecting to Course Page")
            browser.get(self.link)
            loginfo("Redirection successful")
            br()

            br('Waiting for course page to load')
            # Wait till the price div loads
            try:
                loginfo("Waiting for the entire page to load")
                element_present = EC.presence_of_element_located(
                    (By.XPATH, "//div[starts-with(@class, 'price-text--container--')]"))
                loginfo("Page loading complete")
                WebDriverWait(browser, 25).until(element_present)
            except TimeoutException:
                print("Timed out waiting for page to load")
                exit()
            br()

            br('Updating page source')
            # Get the html
            content = browser.page_source
            loginfo("Fetched page url")

            # Parse HTML
            course_page = BeautifulSoup(content, "lxml")
            loginfo("Parsing complete")
            br()

            br('Extracting Course Information')
            # Get content information
            content_info = course_page.select(
                'span[class*="curriculum--content-length-"]')[0].text.replace("\xa0", " ").split(" • ")
            self.duration = content_info[2].replace(" total length", "")
            loginfo("Course duration scraped")

            self.no_of_lectures = int(content_info[1].replace(" lectures", ""))
            loginfo("No of Lecutres scraped")

            self.no_of_sections = int(content_info[0].replace(
                " sections", "").replace(" section", ""))
            loginfo("Number Of Sections scraped")
            br()

            br('Expanded Sections')
            # check if the show more button for sections exists or not.
            if self.no_of_sections > 10:
                browser.execute_script(
                    """var element = document.querySelector('[data-purpose="show-more"]'); element.click();""")
                loginfo(
                    "Clicked show more button to reveal all the sections")
            br()

            br('Updating page source')
            # Get the html
            content = browser.page_source
            if self.Preferences['cache'] == True:
                with open('.udscraper_cache/course.html', 'w', encoding="utf-8") as file:
                    file.write(content)

            loginfo("Updated page source with revealed sections")
            browser.close()
            loginfo("Browser Closed")

            # Parse HTML
            course_page = BeautifulSoup(content, "lxml")
            loginfo("Page source parsed")
            br()
        
        elif self.Preferences['cache'] == True and os.path.isfile('.udscraper_cache/query.txt'):
            br('Reading cached search page html')
            with open('.udscraper_cache/search.html', encoding="utf-8") as f:
                content = f.read()
            br()

            #Parse HTML
            br('Parsing HTML')
            search_page = BeautifulSoup(content, "lxml")
            loginfo("Page source parsed")
            br()

            br('Getting Course Link')
            # Get course link
            self.link = 'https://udemy.com' + search_page.select_one(
                'div[class="course-list--container--3zXPS"] > div > a[tabindex="0"]')['href']
            loginfo("Found course link")
            br()

            br('Reading cached course page html')
            # Get the html
            with open('.udscraper_cache/course.html', encoding="utf-8") as f:
                content = f.read()
            loginfo("Fetched page url")
            br()

            # Parse HTML
            course_page = BeautifulSoup(content, "lxml")
            loginfo("Parsing complete")
            br()

            br('Extracting Course Information')
            # Get content information
            content_info = course_page.select(
                'span[class*="curriculum--content-length-"]')[0].text.replace("\xa0", " ").split(" • ")
            self.duration = content_info[2].replace(" total length", "")
            loginfo("Course duration scraped")

            self.no_of_lectures = int(content_info[1].replace(" lectures", ""))
            loginfo("No of Lecutres scraped")

            self.no_of_sections = int(content_info[0].replace(
                " sections", "").replace(" section", ""))
            loginfo("Number Of Sections scraped")
            br()
            

        br('Extracting course information')
        # Get the title
        self.title = course_page.select_one(
            'h1[class*="udlite-heading-xl clp-lead__title clp-lead__title--small"]').text.replace("\n", "")
        loginfo("Title Scraped")
        br()

        # Get the headline text. (Kind of like the subtitle which is usually displayed under the tite on the course page)
        self.headline = course_page.select_one(
            "div[data-purpose='lead-headline']").text.replace("\n", "")
        loginfo("Headline Scraped")
        br()

        clpblock_elements = course_page.select_one(
            "div[class='clp-lead__badge-ratings-enrollment']")

        # Get the rating
        self.rating = float(clpblock_elements.select_one(
            'span[data-purpose="rating-number"]').text)
        loginfo("Course rating scraped")
        br()
        # Get number of ratings
        self.no_of_ratings = int(clpblock_elements.select(
            "span")[-1].text.replace("(", "").replace(" ratings)", "").replace(",", ""))
        br()
        # Get the number of students
        self.student_enrolls = int(course_page.select_one(
            'div[data-purpose="enrollment"]').text.replace(",", "").replace(" students", ""))
        loginfo("Enrollments scraped")
        br()
        # Get the instructors name
        self.instructors = []
        instructors = course_page.select(
            "a[class='udlite-btn udlite-btn-large udlite-btn-link udlite-heading-md udlite-text-sm udlite-instructor-links'] > span ")
        if len(instructors) > 1:
            for x in instructors:
                self.instructors.append(x.text)
        else:
            self.instructors = instructors[0].text
        loginfo("Instructor name scraped")
        br()
        # Get breadcrumb tags
        self.tags = []
        for tag in course_page.select("div[class='topic-menu udlite-breadcrumb'] > a"):
            self.tags.append(tag.text)
        loginfo("Tags Scraped")
        br()
        # Get course price
        self.price = float(course_page.select(
            'div[class*="price-text--price-part--"] > span')[1].text.replace("\u20b9", ""))
        loginfo("Price scraped")
        br()
        # Get course Language
        self.language = course_page.select_one(
            "div[class='clp-lead__element-item clp-lead__locale']").text.replace("\n", "")
        loginfo("Language scraped")
        br()
        # Get the pointers present in "What you'll learn part"
        self.objectives = []
        for objective in course_page.select("span[class*='what-you-will-learn--objective-item--']"):
            self.objectives.append(objective.text)
        loginfo("Objectives scraped")
        br()
        # Get the requirements section
        self.requirements = []
        for requirement in course_page.select("div[class='ud-component--course-landing-page-udlite--requirements'] > div > ul > li > div > div"):
            self.requirements.append(requirement.text)
        loginfo("Requirements scraped")
        br()
        # Get the long description section. Each paragraph is concatenated to the description string separated by a "\n" or a new line.
        self.description = course_page.select_one(
            "div[data-purpose='course-description']").text
        # loginfo("Description scraped")
        br()
        # Get the information in the target section section
        self.target_audience = []
        for a in course_page.select("div[data-purpose='target-audience'] > ul > li"):
            self.target_audience.append(a.text)
        loginfo("Target Audience text scraped")
        br()
        # Get the banner url of the course
        # self.banner = str(course_page.select_one(
        # ["div[class*='intro-asset--img-'] > img"]).attrs['src'].replace("240x135", "480x270"))
        loginfo("Banner URL scraped")
        br()

        # This is the sections array which will contain Section classes
        self.Sections = []
        br('Scraping Sections and Lessons')
        for section in course_page.select("div[class*='section--panel--']"):
            br(f'Scraping Section {len(self.Sections)+1}')
            self.Sections.append(Section(section))
            br()
        br()


def course_to_dict(course):
    # Initialize a new Sections array which will contain coverted dictionaries instead of objects for json serialization
    new_section_list = []

    for section in course.Sections:
        # Initialize a new lessons array which will contain coverted dictionaries instead of objects for every section
        new_lesson_list = []

        for lesson in section.Lessons:

            dict = lesson.__dict__         # Convert the lesson object to a dictionary
            new_lesson_list.append(dict)   # Add the dictionary to the new list

        # Update the lessons object array with the new lessons dictionary array for this section
        section.Lessons = new_lesson_list
        section_dict = section.__dict__  # Convert the section into a dictionary

        # Add the dictionary to the new list
        new_section_list.append(section_dict)

    # Update the sections object array with the new sections dictionary array
    course.Sections = new_section_list
    loginfo("Successfully parsed to a dicitonary")
    # return the dictionary
    return course.__dict__


def course_to_json(course, output_file='output.json'):
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a json in 'object.json' file. You can change this to whatever you want
    with open(output_file, 'w') as file:
        # Convert the course to dictionary and dump.
        file.write(json.dumps(course))
        loginfo(f"File course dumped as {output_file}")


"""
   SSSSSSSSSSSSSSS                                          iiii                              tttt
 SS:::::::::::::::S                                        i::::i                          ttt:::t
S:::::SSSSSS::::::S                                         iiii                           t:::::t
S:::::S     SSSSSSS                                                                        t:::::t
S:::::S                ccccccccccccccccrrrrr   rrrrrrrrr  iiiiiiippppp   ppppppppp   ttttttt:::::ttttttt
S:::::S              cc:::::::::::::::cr::::rrr:::::::::r i:::::ip::::ppp:::::::::p  t:::::::::::::::::t
 S::::SSSS          c:::::::::::::::::cr:::::::::::::::::r i::::ip:::::::::::::::::p t:::::::::::::::::t
  SS::::::SSSSS    c:::::::cccccc:::::crr::::::rrrrr::::::ri::::ipp::::::ppppp::::::ptttttt:::::::tttttt
    SSS::::::::SS  c::::::c     ccccccc r:::::r     r:::::ri::::i p:::::p     p:::::p      t:::::t
       SSSSSS::::S c:::::c              r:::::r     rrrrrrri::::i p:::::p     p:::::p      t:::::t
            S:::::Sc:::::c              r:::::r            i::::i p:::::p     p:::::p      t:::::t
            S:::::Sc::::::c     ccccccc r:::::r            i::::i p:::::p    p::::::p      t:::::t    tttttt
SSSSSSS     S:::::Sc:::::::cccccc:::::c r:::::r           i::::::ip:::::ppppp:::::::p      t::::::tttt:::::t
S::::::SSSSSS:::::S c:::::::::::::::::c r:::::r           i::::::ip::::::::::::::::p       tt::::::::::::::t
S:::::::::::::::SS   cc:::::::::::::::c r:::::r           i::::::ip::::::::::::::pp          tt:::::::::::tt
 SSSSSSSSSSSSSSS       cccccccccccccccc rrrrrrr           iiiiiiiip::::::pppppppp              ttttttttttt
                                                                  p:::::p
                                                                  p:::::p
                                                                 p:::::::p
                                                                 p:::::::p
                                                                 p:::::::p
                                                                 ppppppppp
"""


# When evoked directly
if __name__ == "__main__":
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hvnq:b:l:d:o:e:tc:"

    # Long options
    long_options = ["help", "version", "no-warn",
                    "query", "browser", "headless", "dump", "output", "debug", "quiet", "time", "progress", "cache"]

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
        'cache' : False
    }

    search_query = ""

    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # checking each argument
        # print(arguments, values)
        # exit()
        for currentArgument, currentValue in arguments:

            # Help argument
            if currentArgument in ("-h", "--help"):
                display_help()

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
                if currentValue == True:
                    Preferences['debug'] = True
                elif currentValue == False:
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
    course = UdemyCourse(Preferences)

    if Preferences['quiet'] == False or Preferences['progress'] == True:
        with alive_bar(title="Scraping Course", bar="smooth") as abar:
            course.fetch_course(search_query,)
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

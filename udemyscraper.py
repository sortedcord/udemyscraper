# Selenium Libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # to wait until page loads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium import webdriver  # for webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import platform
import time
import json
import logging
import getopt
import sys
from colorama import Fore, Style

__version__ = "0.0.5"

def display_warn():
    with open('texts/warning.txt') as file:
        lines = file.readlines()
        for line in lines:
            print(line.replace("\n", ""))
            time.sleep(0.4)


class UdemyCourse():
    def __init__(self, query, Options):
        self.query = query
        self.Options = Options
        
        if self.Options['warn'] == True:
            display_warn()

        if Options['debug'] == True:
            logging.basicConfig(level=logging.DEBUG)

    def fetch_course(self):
        # Course class will contain an array with section classes
        class Section():
            def __init__(self, html):
                # Section class will contain an array with lesson classes
                class Lesson():
                    def __init__(self, lesson_html):
                        self.lesson_html = lesson_html
                        self.name = lesson_html.find("span").text
                        logging.debug("Scraped Lesson HTML")

                self.html = BeautifulSoup(html, "lxml")
                logging.debug("Parsed Section HTML")

                self.name = self.html.select(
                    "span[class*='section--section-title--']")[0].text
                logging.debug("Scraped name")

                self.duration = self.html.find(
                    'span', attrs={'data-purpose': 'section-content'}).text.split(' • ')[1].replace(' ', '')
                logging.debug('Scraped Section duration')

                self.lesson_blocks = self.html.find_all(
                    "div", class_="udlite-block-list-item-content")
                self.lessons = []
                for lesson in self.lesson_blocks:
                    self.lessons.append(Lesson(lesson))
                    logging.debug(
                        f"Lesson {len(self.lessons)} scraped successfully")

                self.no_of_lessons = len(self.lessons)

        # Get the url of the search query
        url = "https://www.udemy.com/courses/search/?src=ukw&q=" + self.query

        logging.debug("Setting Up browser headers and preferences")
        if self.Options['browser_preference'] == "CHROME":
            # Browser Options
            option = Options()
            if self.Options['headless'] == True:
                option.add_argument('headless')
                logging.debug("Headless enabled")
            option.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

            if platform.system() == "Windows":
                browser = webdriver.Chrome(
                    executable_path='drivers/chromedriver.exe', chrome_options=option)
            else:
                browser = webdriver.Chrome(chrome_options=option)
        elif self.Options['browser_preference'] == "FIREFOX":
            fireFoxOptions = webdriver.FirefoxOptions()
            if self.Options['headless'] == True:
                logging.debug("Headless enabled")
                fireFoxOptions.set_headless()
            browser = webdriver.Firefox(
                firefox_options=fireFoxOptions)
        else:
            print("Don't know how this happened ¯\_(ツ)_/¯")

        logging.debug(
            "Starting up headless browser and redirecting to the searchpage")
        browser.get(url)

        # Wait until the search box loads
        try:
            logging.debug(
                "Waiting for the browser to load the search results. This depends on your network responsiveness")
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//div[starts-with(@class, 'course-directory--container--')]"))
            WebDriverWait(browser, 5).until(element_present)
        except TimeoutException:
            print(
                "Timed out waiting for page to load or could not find a matching course")
            exit()
        logging.debug("Search results found")

        # Get page source
        content = browser.page_source
        logging.debug("Fetched page source")
        search_page = BeautifulSoup(content, "lxml")
        logging.debug("Page source parsed")

        # Get course basic metadata
        link_block = str(search_page.select(
            'a[class*="browse-course-card--link--"]')[0])
        logging.debug("Scraped first result's URL")
        self.link = 'https://udemy.com' + \
            str(BeautifulSoup(link_block, 'lxml').find('a')['href'])

        # Scrape Information on course_page
        url = self.link
        logging.debug("Redirecting to Course Page")
        browser.get(url)
        logging.debug("Redirection successful")

        # Wait till the price div loads
        try:
            logging.debug("Waiting for the entire page to load")
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//div[starts-with(@class, 'price-text--container--')]"))
            logging.debug("Page loading complete")
            WebDriverWait(browser, 10).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")

        # Get the html
        content = browser.page_source
        logging.debug("Fetched page url")

        # Parse HTML
        course_page = BeautifulSoup(content, "lxml")
        logging.debug("Parsing complete")

        logging.debug("Searching for 'show more' button")
        no_of_buttons = len(course_page.find_all(
            "button", attrs={'data-purpose': 'show-more'}))
        # check if the show more button for sections exists or not.
        if no_of_buttons > 0:
            browser.execute_script(
                """var element = document.querySelector('[data-purpose="show-more"]'); element.click();""")
            logging.debug(
                "Clicked show more button to reveal all the sections")

        # Get the html
        content = browser.page_source
        logging.debug("Updated page source with revealed sections")
        browser.close()
        logging.debug("Browser Closed")

        # Parse HTML
        course_page = BeautifulSoup(content, "lxml")
        logging.debug("Page source parsed")

        # Get the title
        logging.debug("Searching for title")
        self.title = course_page.find(
            "h1", class_="udlite-heading-xl clp-lead__title clp-lead__title--small").text
        logging.debug("Title Scraped")

        # Get the headline text. (Kind of like the subtitle which is usually displayed under the tite on the course page)
        logging.debug("Searching for headline")
        self.headline = course_page.find(
            "div", attrs={'data-purpose': 'lead-headline'}).text
        logging.debug("Headline Scraped")

        # Get the rating
        logging.debug("Searching for course rating")
        self.rating = course_page.find(
            "span", attrs={'data-purpose': 'rating-number'}).text
        logging.debug("Course rating scraped")

        # Get number of ratings
        logging.debug("Searching for number of ratings")
        self.no_of_ratings = course_page.find("div", class_="clp-lead__element-item clp-lead__element-item--row").find_all(
            "span")[3].text.replace("(", "").replace(" ratings)", "")
        logging.debug("Number of ratings scraped")

        # Get the number of students
        logging.debug(
            "Searching for number of students enrolled in the course")
        self.student_enrolls = course_page.find(
            "div", attrs={'data-purpose': 'enrollment'}).text.replace(" students", "")
        logging.debug("Value scraped")

        # Get the instructors name
        self.instructor = course_page.find(
            "a", class_="udlite-btn udlite-btn-large udlite-btn-link udlite-heading-md udlite-text-sm udlite-instructor-links").find("span").text.replace("\n", "")
        logging.debug("Instructor name scraped")

        # Get content information
        content_info = course_page.select(
            'span[class*="curriculum--content-length-"]')[0].text.replace("\xa0", " ").split(" • ")
        self.duration = content_info[2].replace(" total length", "")
        logging.debug("Course duration scraped")

        self.no_of_lectures = content_info[1].replace(" lectures", "")
        logging.debug("No of Lecutres scraped")

        self.no_of_sections = content_info[0].replace(" sections", "")
        logging.debug("Number Of Lectures scraped")
        # Get breadcrumb tags
        self.tags = []
        for tag in course_page.find("div", class_="topic-menu udlite-breadcrumb").find_all("a", class_="udlite-heading-sm"):
            self.tags.append(tag.text)
        logging.debug("Tags Scraped")

        # Get course price
        self.price = course_page.select(
            'div[class*="price-text--price-part--"] > span')[1].text
        logging.debug("Price scraped")

        # Get course Language
        logging.debug("Language scraped")
        self.course_language = course_page.find(
            "div", class_="clp-lead__element-item clp-lead__locale").text.replace("\n", "")

        # Get the pointers present in "What you'll learn part"
        self.objectives = []
        for objective in course_page.find_all("span", class_="what-you-will-learn--objective-item--ECarc"):
            self.objectives.append(objective.text)
        logging.debug("Objectives scraped")

        # This is the sections array which will contain Section classes
        self.Sections = []

        string_section = []
        for s in course_page.select("div[class*='section--panel--1tqxC panel--panel--']"):
            string_section.append(str(s))
            _x = 1
        for section_block in string_section:
            logging.debug(f"Scraping section {str(_x)}")
            self.Sections.append(Section(section_block))
            logging.debug(f"Section {str(_x)} scraped successfully")
            _x += 1

        # Get the requirements section
        self.requirements = []
        for requirement in course_page.find("div", class_="ud-component--course-landing-page-udlite--requirements").find_all("div", class_="udlite-block-list-item udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral udlite-text-sm"):
            self.requirements.append(requirement.text)
        logging.debug("Requirements scraped")

        # Get the long description section. Each paragraph is concatenated to the description string separated by a "\n" or a new line.
        self.description = ""
        for parahraph in course_page.find("div", attrs={'data-purpose': 'safely-set-inner-html:description:description'}).find_all("p"):
            self.description += parahraph.text + "\n"
        logging.debug("Description scraped")

        # Get the information in the target section section
        self.target_audience = []
        for a in course_page.find("div", attrs={'data-purpose': 'target-audience'}).find_all("li"):
            self.target_audience.append(a.text)
        logging.debug("Target Audience text scraped")

        # Get the banner url of the course
        self.banner = str(course_page.find(
            "div", class_="intro-asset--asset--1eSsi").find("img").attrs['src']).replace("240x135", "480x270")
        logging.debug("Banner URL scraped")


def course_to_dict(course):
    # Initialize a new Sections array which will contain coverted dictionaries instead of objects for json serialization
    new_section_list = []

    for section in course.Sections:
        # Initialize a new lessons array which will contain coverted dictionaries instead of objects for every section
        new_lesson_list = []

        for lesson in section.lessons:

            dict = lesson.__dict__         # Convert the lesson object to a dictionary
            # Remove the html code from the dictionary
            del dict['lesson_html']
            new_lesson_list.append(dict)   # Add the dictionary to the new list

        # Update the lessons object array with the new lessons dictionary array for this section
        section.lessons = new_lesson_list
        section_dict = section.__dict__  # Convert the section into a dictionary

        # Remove the html code from the dictionary
        del section_dict['html']
        del section_dict['lesson_blocks']

        # Add the dictionary to the new list
        new_section_list.append(section_dict)

    # Update the sections object array with the new sections dictionary array
    course.Sections = new_section_list
    logging.debug("Successfully parsed to a dicitonary")
    # return the dictionary
    return course.__dict__


def course_to_json(course, output_file='output.json'):
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a json in 'object.json' file. You can change this to whatever you want
    with open(output_file, 'w') as file:
        # Convert the course to dictionary and dump.
        file.write(json.dumps(course))
        logging.debug(f"File course dumped as {output_file}")

if __name__ == "__main__":

    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]

    # Options
    options = "hvnq:b:l:d:o:e"

    # Long options
    long_options = ["help", "version", "no-warn",
                    "query", "browser", "headless", "dump", "output", "debug", "quiet"]

    # Tool Defaults
    Options = {
        'warn': True,
        'browser_preference': "CHROME",
        'headless': True,
        'dump_format': "",
        'output_file': "",
        'debug': False,
        'quiet': False,
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
            elif currentArgument in ("-e", "--debug"):
                Options['debug'] = True

            elif currentArgument in ("--quiet"):
                Options['quiet'] = True


    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    if Options['quiet'] == False:
        print(Fore.MAGENTA + """
██╗   ██╗██████╗ ███████╗███╗   ███╗██╗   ██╗    ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
██║   ██║██╔══██╗██╔════╝████╗ ████║╚██╗ ██╔╝    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║   ██║██║  ██║█████╗  ██╔████╔██║ ╚████╔╝     ███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
██║   ██║██║  ██║██╔══╝  ██║╚██╔╝██║  ╚██╔╝      ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
╚██████╔╝██████╔╝███████╗██║ ╚═╝ ██║   ██║       ███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
╚═════╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝   ╚═╝       ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝""")
        print(Style.RESET_ALL)

        print(f"Version: {__version__}")
        print(f"Using Preferences: {Options}")


    if search_query == "":
        search_query = input("Enter the search query: ")
    else:
        if Options['quiet'] == False:
            print(f"Search with query: {search_query}")
    course = UdemyCourse(search_query, Options)
    course.fetch_course()


    if Options['dump_format'] != "":
        if Options['dump_format'] == 'json':
            course_to_json(course, Options['output_file'])
        elif Options['dump_format'] == 'csv':
            print("\n", "WARN: 'CSV' dump format is currently not supported.")
        elif Options['dump_format'] == 'xml':
            print("\n", "WARN: 'XML' dump format is currently not supported.")

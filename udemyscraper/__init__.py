import time
__starttime__ = time.time()

# Selenium Libraries
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # to wait until page loads
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from udemyscraper.utils import display_warn, set_browser
import os
from bs4 import BeautifulSoup
import logging
from logging import *
from colorama import Fore, Style
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
        'browser': "chrome",
        'headless': True,
        'debug': False,
        'quiet': False,
        'time': True,
        'cache': False
    }):  # Set default preferences when none provided
        
        default_values = [True, "chrome", True, False, False, True, False]
        default_keys = ['warn', 'browser', 'headless', 'debug', 'quiet', 'time', 'cache']
        for key in default_keys:
            if key not in Preferences.keys():
                Preferences[key] = default_values[default_keys.index(key)]      
    
        self.Preferences = Preferences
        if self.Preferences['warn'] == True:
            display_warn()

        if self.Preferences['debug'] == True:
            logging.basicConfig(level=logging.DEBUG)
        elif self.Preferences['debug'] == "info":
            logging.basicConfig(level=logging.INFO)

    def fetch_course(self, query, abar=None):
        loginfo("Setting Dummy Functions for Bar")
        loginfo("")

        def br(message=""):
            try:
                if message=="":
                    abar()
                else:
                    abar.text(message)
            except:
                loginfo("Alive bar is not being used")

        loginfo("Searching for cache file")
        cache_file = os.path.isfile('.udscraper_cache/query.txt')
        br('Checking if Cache files exists')
        if self.Preferences['cache'] == True and cache_file:
            loginfo("Cache files exists")
            with open('.udscraper_cache/query.txt') as query_file:
                br('Reading Cache files')
                loginfo("Reading cache files")
                old_query = query_file.read()
            if query != str(old_query):
                br('Flushing cache files as query is different')
                loginfo("Deleting cache folder")
                shutil.rmtree('.udscraper_cache/')
                self.Preferences['cache'] == True
                cache_file = os.path.isfile('.udscraper_cache/query.txt')

        # Check if cache exists
        if self.Preferences['cache'] == 'clear' or self.Preferences['cache'] == False or (self.Preferences['cache'] == True and cache_file == False):
            if self.Preferences['cache'] == 'clear':
                br('Flushing cache files')
                shutil.rmtree('.udscraper_cache/')
                loginfo("Cache folder deleted")
                self.Preferences['cache'] == True
                br()

            if self.Preferences['cache'] == True:
                br('Created cache files')
                os.mkdir('.udscraper_cache')
                loginfo("Created cache folder")
                br()

            # Get the url of the search query
            url = "https://www.udemy.com/courses/search/?src=ukw&q=" + query
            if self.Preferences['cache'] == True:
                br('Dumping query text')
                with open('.udscraper_cache/query.txt', 'w', encoding="utf-8") as file:
                    loginfo("Writing query text file")
                    file.write(query)
                br()

            br('Launching Browser')
            loginfo("Setting Up browser headers and preferences")
            browser = set_browser(self.Preferences)

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

            # Parse HTML
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

            # Parse HTML
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
        self.banner = str(course_page.select_one(
        "span[class*='intro-asset--img-aspect--'] > img").attrs['src'].replace("240x135", "480x270"))
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

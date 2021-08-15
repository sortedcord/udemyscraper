import platform
import time

from dict2xml import *
import json

from bs4 import BeautifulSoup

# Selenium Libraries
from selenium import webdriver  # for webdriver

# for suppressing the browser
from selenium.webdriver.chrome.options import Options

# to wait until page loads
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def display_warn():
    with open('texts/warning.txt') as file:
        lines = file.readlines()
        for line in lines:
            print(line.replace("\n", ""))
            time.sleep(0.4)


class UdemyCourse():
    def __init__(self, query, warn=True, browser_preference="CHROME", headless=True):
        self.query = query
        self.browser_preference = browser_preference
        self.headless = headless
        if warn == True:
            display_warn()

    def fetch_course(self):
        # Course class will contain an array with section classes
        class Section():
            def __init__(self, html):
                # Section class will contain an array with lesson classes
                class Lesson():
                    def __init__(self, lesson_html):
                        self.lesson_html = lesson_html
                        self.name = lesson_html.find("span").text

                self.html = BeautifulSoup(html, "lxml")
                self.name = self.html.select(
                    "span[class*='section--section-title--']")[0].text
                self.lesson_blocks = self.html.find_all(
                    "div", class_="udlite-block-list-item-content")

                self.lessons = []
                for lesson in self.lesson_blocks:
                    self.lessons.append(Lesson(lesson))

                self.no_of_lessons = len(self.lessons)

                self.duration = self.html.find(
                    'span', attrs={'data-purpose': 'section-content'}).text.split(' • ')[1].replace(' ', '')

        # Get the url of the search query
        url = "https://www.udemy.com/courses/search/?src=ukw&q=" + self.query

        if self.browser_preference == "CHROME":
            # Browser Options
            option = Options()
            if self.headless == True:
                option.add_argument('headless')
            option.add_experimental_option(
                'excludeSwitches', ['enable-logging'])

            if platform.system() == "Windows":
                browser = webdriver.Chrome(
                    executable_path='drivers/chromedriver.exe', chrome_options=option)
            else:
                browser = webdriver.Chrome(chrome_options=option)
        elif self.browser_preference == "FIREFOX":
            fireFoxOptions = webdriver.FirefoxOptions()
            if self.headless == True:
                fireFoxOptions.set_headless()
            browser = webdriver.Firefox(
                executable_path="drivers/gekodriver.exe", firefox_options=fireFoxOptions)
        else:
            print("Don't know how this happened ¯\_(ツ)_/¯")

        browser.get(url)

        # Wait until the search box loads
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//div[starts-with(@class, 'course-directory--container--')]"))
            WebDriverWait(browser, 3).until(element_present)
        except TimeoutException:
            print(
                "Timed out waiting for page to load or could not find a matching course")
            exit()

        # Get page source
        content = browser.page_source
        search_page = BeautifulSoup(content, "lxml")

        # Get course basic metadata
        link_block = str(search_page.select(
            'a[class*="browse-course-card--link--"]')[0])
        self.link = 'https://udemy.com' + \
            str(BeautifulSoup(link_block, 'lxml').find('a')['href'])

        # Scrape Information on course_page
        url = self.link
        browser.get(url)

        # Wait till the price div loads
        try:
            element_present = EC.presence_of_element_located(
                (By.XPATH, "//div[starts-with(@class, 'price-text--container--')]"))
            WebDriverWait(browser, 4).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
            exit()

        # Get the html
        content = browser.page_source

        # Parse HTML
        course_page = BeautifulSoup(content, "lxml")

        no_of_buttons = len(course_page.find_all(
            "button", attrs={'data-purpose': 'show-more'}))
        time.sleep(3)
        # check if the show more button for sections exists or not.
        if no_of_buttons > 0:
            browser.execute_script(
                """var element = document.querySelector('[data-purpose="show-more"]'); element.click();""")

        # Get the html
        content = browser.page_source
        browser.close()
        # Parse HTML
        course_page = BeautifulSoup(content, "lxml")

        # Get the title
        self.title = course_page.find(
            "h1", class_="udlite-heading-xl clp-lead__title clp-lead__title--small").text

        # Get the headline text. (Kind of like the subtitle which is usually displayed under the tite on the course page)
        self.headline = course_page.find(
            "div", attrs={'data-purpose': 'lead-headline'}).text

        # Get the rating
        self.rating = course_page.find(
            "span", attrs={'data-purpose': 'rating-number'}).text

        # Get number of ratings
        self.no_of_ratings = course_page.find("div", class_="clp-lead__element-item clp-lead__element-item--row").find_all(
            "span")[3].text.replace("(", "").replace(" ratings)", "")

        # Get the number of students
        self.student_enrolls = course_page.find(
            "div", attrs={'data-purpose': 'enrollment'}).text.replace(" students", "")

        # Get the instructors name
        self.instructor = course_page.find(
            "a", class_="udlite-btn udlite-btn-large udlite-btn-link udlite-heading-md udlite-text-sm udlite-instructor-links").find("span").text.replace("\n", "")

        # Get content information
        content_info = course_page.select(
            'span[class*="curriculum--content-length-"]')[0].text.replace("\xa0", " ").split(" • ")
        self.duration = content_info[2].replace(" total length", "")

        self.no_of_lectures = content_info[1].replace(" lectures", "")

        self.no_of_sections = content_info[0].replace(" sections", "")
        # Get breadcrumb tags
        self.tags = []
        for tag in course_page.find("div", class_="topic-menu udlite-breadcrumb").find_all("a", class_="udlite-heading-sm"):
            self.tags.append(tag.text)

        # Get course price
        self.price = course_page.select(
            'div[class*="price-text--price-part--"] > span')[1].text

        # This is come noob code. I didn't know of any other way, so please, if you have a better alternative, create a PR :pray:
        self.no_of_rating = course_page.find("span", class_="", string=lambda x: x and x.startswith(
            '(')).text.replace("(", "").replace(" ratings)", "")
        self.no_of_students = course_page.find("div", attrs={
                                               "data-purpose": "enrollment"}).text.replace("\n", "").replace(" students", "")
        self.course_language = course_page.find(
            "div", class_="clp-lead__element-item clp-lead__locale").text.replace("\n", "")

        # Get the pointers present in "What you'll learn part"
        self.objectives = []
        for objective in course_page.find_all("span", class_="what-you-will-learn--objective-item--ECarc"):
            self.objectives.append(objective.text)

        # This is the sections array which will contain Section classes
        self.Sections = []

        string_section = []
        for s in course_page.select("div[class*='section--panel--1tqxC panel--panel--']"):
            string_section.append(str(s))
        for section_block in string_section:
            self.Sections.append(Section(section_block))

        # Get the requirements section
        self.requirements = []
        for requirement in course_page.find("div", class_="ud-component--course-landing-page-udlite--requirements").find_all("div", class_="udlite-block-list-item udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral udlite-text-sm"):
            self.requirements.append(requirement.text)

        # Get the long description section. Each paragraph is concatenated to the description string separated by a "\n" or a new line.
        self.description = ""
        for parahraph in course_page.find("div", attrs={'data-purpose': 'safely-set-inner-html:description:description'}).find_all("p"):
            self.description += parahraph.text + "\n"

        # Get the information in the target section section
        self.target_audience = []
        for a in course_page.find("div", attrs={'data-purpose': 'target-audience'}).find_all("li"):
            self.target_audience.append(a.text)

        # Get the url of the course
        self.banner = str(course_page.find(
            "div", class_="intro-asset--asset--1eSsi").find("img").attrs['src']).replace("240x135", "480x270")


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

    # return the dictionary
    return course.__dict__


def course_to_json(course, output_file='output.json'):
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a json file.
    with open(output_file, 'w', encoding="utf-8") as file:
        # Convert the course to dictionary and dump.
        file.write(json.dumps(course))


def course_to_xml(course, output_file='output.xml',):
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a xml file.
    with open(output_file, 'w', encoding="utf-8") as file:
        # Convert the course to dictionary and dump.
        xml = dict2xml(course, wrap='course')
        file.write(xml)

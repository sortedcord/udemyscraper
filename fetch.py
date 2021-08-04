from bs4 import BeautifulSoup
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import requests
from selenium.common.exceptions import WebDriverException
import json


class Course():
    
    def __init__(self, query):
        self.query = query    


    def fetchCourse(self):
        url = "https://www.udemy.com/courses/search/?src=ukw&q=" + self.query
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        
        browser = webdriver.Chrome('chromedriver.exe', options= option)

        browser.get(url)
        time.sleep(4)
        content = browser.page_source
        searchpage = BeautifulSoup(content, "html.parser")

        links = []
        for a in searchpage.find_all('a', class_='udlite-custom-focus-visible browse-course-card--link--3KIkQ', href=True): 
            if a.text: 
                links.append(a['href'])
        self.link = 'https://udemy.com' + (links[0])

        self.title = searchpage.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE").text
        self.description = searchpage.find('p', class_="udlite-text-sm course-card--course-headline--yIrRk").text
        self.instructor = searchpage.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f").text
        self.rating = searchpage.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8").text

        other_info = searchpage.find_all('span', class_="course-card--row--1OMjg")
        truncated_info = other_info[0:3]

        self.duration = truncated_info[0].text
        self.no_of_lectures = truncated_info[1].text

        class Section():
            def __init__(self, html):
                class Lesson():
                    def __init__(self, lesson_html):
                        self.lesson_html = lesson_html
                        self.name = lesson_html.find("span").text
                        
                self.html = BeautifulSoup(html, "html.parser")
                self.name = self.html.find("span", class_="section--section-title--8blTh").text
                self.lesson_blocks = self.html.find_all("div", class_="udlite-block-list-item-content")

                self.lessons = []

                for lesson in self.lesson_blocks:
                    self.lessons.append(Lesson(lesson))
                self.no_of_lessons = len(self.lessons)
                

                other_info_block = self.html.find_all("span", class_="udlite-text-sm section--hidden-on-mobile--171Q9 section--section-content--9kwnY")

        '''
                SCRAPE COURSE PAGE
        '''

        url = self.link
        browser.get(url)
        try:
            action = ActionChains(browser) # initialize ActionChain object
            classname = "udlite-btn udlite-btn-medium udlite-btn-secondary udlite-heading-sm curriculum--show-more--2tshH"
            browser.execute_script(f"javascript:document.getElementsByClassName('{classname}')[0].scrollIntoView();")
            button = browser.find_element_by_xpath("//*[@data-purpose='show-more']")
            action.click(on_element = button)
            action.perform()
        except (ValueError, WebDriverException) as e:
            print("looks like there aren't that many sections")


        content = browser.page_source
        browser.close()
        coursepage = BeautifulSoup(content, "html.parser")
        
        coursepage = BeautifulSoup(content, "html.parser")

        breadcrumbs = coursepage.find("div", class_="topic-menu udlite-breadcrumb")
        raw_tags = breadcrumbs.find_all("a", class_="udlite-heading-sm")
        tags = []
        for tag in raw_tags:
            tags.append(tag.text)
        self.tags = tags

        # This is come noob code. I didn't know of any other way, so please, if you have a better alternative, create a PR :pray:
        self.no_of_rating = coursepage.find("span", class_="", string=lambda x: x and x.startswith('(')).text.replace("(", "").replace(" ratings)", "")
        self.no_of_students = coursepage.find("div", attrs={"data-purpose": "enrollment"}).text.replace("\n","").replace(" students", "")
        self.course_language = coursepage.find("div", class_="clp-lead__element-item clp-lead__locale").text

        objectives = []
        raw_obj = coursepage.find_all("span", class_="what-you-will-learn--objective-item--ECarc")
        for objective in raw_obj:
            objectives.append(objective.text)
        self.objectives = objectives

        self.Sections = []

        string_section = []
        sections = coursepage.find_all("div", class_="section--panel--1tqxC panel--panel--3NYBX")
        for s in sections:
            string_section.append(str(s))
        for section_block in string_section:
            self.Sections.append(Section(section_block))

        requirements_block = coursepage.find("div", class_="ud-component--course-landing-page-udlite--requirements")


def convertToJson(course):
    new_section_list = []
    for section in course.Sections:
        new_lesson_list = []
        for lesson in section.lessons:
            dict = lesson.__dict__
            del dict['lesson_html']
            new_lesson_list.append(dict)
        section.lessons = new_lesson_list
        section_dict = section.__dict__
        del section_dict['html']
        del section_dict['lesson_blocks']
        new_section_list.append(section_dict)
    course.Sections = new_section_list

    with open('object.json', 'w') as file:
        file.write(json.dumps(course.__dict__))





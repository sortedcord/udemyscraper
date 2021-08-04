from bs4 import BeautifulSoup
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.action_chains import ActionChains
import time
import requests

class Course():
    
    def __init__(self, query):
        self.query = query    


    def fetchCourse(self):
        url = "https://www.udemy.com/courses/search/?src=ukw&q=" + self.query
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome('chromedriver.exe',options=option)

        browser.get(url)
        time.sleep(4)
        content = browser.page_source
        soup = BeautifulSoup(content, "html.parser")
        browser.close()

        links = []
        for a in soup.find_all('a', class_='udlite-custom-focus-visible browse-course-card--link--3KIkQ', href=True): 
            if a.text: 
                links.append(a['href'])
        self.link = 'https://udemy.com' + links[0]

        self.title = soup.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE")
        self.description = soup.find('p', class_="udlite-text-sm course-card--course-headline--yIrRk")
        self.instructor = soup.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f")
        self.rating = soup.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8")

        other_info = soup.find_all('span', class_="course-card--row--1OMjg")
        truncated_info = other_info[0:3]

        self.duration = truncated_info[0]
        self.no_of_lectures = truncated_info[1]


    def getCourseInfo(self):
        class Section():
            def __init__(self, html):
                class Lesson():
                    def __init__(self, lesson_html):
                        self.lesson_html = lesson_html

                        self.name = lesson_html.find("span").text

                self.html = html

                self.name = html.find("span", class_="section--section-title--8blTh").text
                self.lesson_blocks = html.find_all("div", class_="udlite-block-list-item-content")

                self.lessons = []

                for lesson in self.lesson_blocks:
                    self.lessons.append(Lesson(lesson))



        url = self.link

        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        browser = webdriver.Chrome('chromedriver.exe', options=option)
        browser.set_window_size(1280,720)
        browser.get(url)
        action = ActionChains(browser) # initialize ActionChain object
        browser.execute_script("javascript:window.scrollBy(0,1500)")
        button = browser.find_element_by_xpath("//*[@data-purpose='show-more']")
        action.click(on_element = button)
        action.perform()
        content = browser.page_source
        browser.close()
        soup = BeautifulSoup(content, "html.parser")
        
        soup = BeautifulSoup(content, "html.parser")

        breadcrumbs = soup.find("div", class_="topic-menu udlite-breadcrumb")
        raw_tags = breadcrumbs.find_all("a", class_="udlite-heading-sm")
        tags = []
        for tag in raw_tags:
            tags.append(tag.text)
        self.tags = tags

        # This is come noob code. I didn't know of any other way, so please, if you have a better alternative, create a PR :pray:
        self.no_of_rating = soup.find("span", class_="", string=lambda x: x and x.startswith('(')).text.replace("(", "").replace(" ratings)", "")
        self.no_of_students = soup.find("div", attrs={"data-purpose": "enrollment"}).text.replace("\n","").replace(" students", "")
        self.course_language = soup.find("div", class_="clp-lead__element-item clp-lead__locale").text

        objectives = []
        raw_obj = soup.find_all("span", class_="what-you-will-learn--objective-item--ECarc")
        for objective in raw_obj:
            objectives.append(objective.text)
        self.objectives = objectives

        self.Sections = []

        sections = soup.find_all("div", class_="section--panel--1tqxC panel--panel--3NYBX")
        
        for section in sections:
            self.Sections.append(Section(section))
            


        









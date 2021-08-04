from bs4 import BeautifulSoup
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
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
        self.author = soup.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f")
        self.rating = soup.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8")

        other_info = soup.find_all('span', class_="course-card--row--1OMjg")
        truncated_info = other_info[0:3]

        self.duration = truncated_info[0]
        self.no_of_lectures = truncated_info[1]


    def getCourseInfo(self):
        url = self.link

        page = requests.get(url)
        content = page.content
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


        '''
                                                                     WARNING
                                                    If you value your life more than the udemy courses
                                                    then please do not read the code below. Within 2 to
                                                    3 minutes of reading the code below, you may develop
                                                    the badCode syndrome. In order to protect your brain 
                                                    from this condition, please do not read the code below.

        '''        
        class Section():
            def __init__(self, name, no_of_lectures, duration):
                self.name = name
                self.no_of_lectures = no_of_lectures
                self.duration = duration
            
            class Lessons():
                def __init__(self, name, duration, lesson_type):
                    self.name = name
                    self.duration = duration
                    self.lesson_type = lesson_type
        
        sections = []
        sections_raw = soup.find_all("span", class_="section--section-title--8blTh")
        section_names = []
        for section in sections_raw:
            section_names.append(section.text)

        section_info = soup.find_all("span", class_="udlite-text-sm section--hidden-on-mobile--171Q9 section--section-content--9kwnY")
        section_lectures = []
        section_duration = []
        for section in section_info:
            formatted_section_info = section.text.replace("•", "").replace(" lectures  ", " ").replace("hr ", "hr")
            formatted_section_info = formatted_section_info.split(" ")
            section_lectures.append(formatted_section_info[0])
            section_duration.append(formatted_section_info[1])
        
        for section in range(len(sections_raw)):
            sections.append(Section(section_names[section], section_lectures[section], section_duration[section]))
        
        self.sections = sections









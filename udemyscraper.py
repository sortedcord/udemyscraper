import time
import json
from bs4 import BeautifulSoup

#Selenium Libraries
from selenium import webdriver   # for webdriver
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.common.exceptions import WebDriverException



class UdemyCourse():
    def __init__(self, query):
        self.query = query


    def fetch_course(self):
            # Course class will contain an array with section classes
        class Section():
            def __init__(self, html):
                #Section class will contain an array with lesson classes
                class Lesson():
                    def __init__(self, lesson_html):
                        self.lesson_html = lesson_html
                        self.name = lesson_html.find("span").text
                        
                self.html = BeautifulSoup(html, "lxml")
                self.name = self.html.find("span", class_="section--section-title--8blTh").text
                self.lesson_blocks = self.html.find_all("div", class_="udlite-block-list-item-content")

                self.lessons = []
                for lesson in self.lesson_blocks:
                    self.lessons.append(Lesson(lesson))
                
                self.no_of_lessons = len(self.lessons)
                
                other_info_block = self.html.find_all("span", class_="udlite-text-sm section--hidden-on-mobile--171Q9 section--section-content--9kwnY")

        #Get the url of the search query
        url = "https://www.udemy.com/courses/search/?src=ukw&q=" + self.query

        # Browser Options
        option = Options()
        option.add_argument('headless')
        option.add_experimental_option('excludeSwitches', ['enable-logging'])
        browser = webdriver.Chrome(executable_path='chromedriver.exe',chrome_options=option)
        browser.get(url)
        time.sleep(3)

        #Get page source
        content = browser.page_source
        search_page = BeautifulSoup(content, "lxml")

        # Get course_page Link
        links = []
        for a in search_page.find_all('a', class_='udlite-custom-focus-visible browse-course-card--link--3KIkQ', href=True): 
            if a.text: 
                links.append(a['href'])
    
        other_info = search_page.find_all('span', class_="course-card--row--1OMjg")
        truncated_info = other_info[0:3]

        # Get course basic metadata
        self.link = 'https://udemy.com' + (links[0])
        self.title = search_page.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE").text
        self.headline = search_page.find('p', class_="udlite-text-sm course-card--course-headline--yIrRk").text
        self.instructor = search_page.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f").text
        self.rating = search_page.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8").text
        self.duration = truncated_info[0].text
        self.number_of_lectures = truncated_info[1].text

        
        # Scrape Information on course_page
        url = self.link
        browser.get(url)

        time.sleep(3) #Wait for the browser to completely load the page. You can change this depending on your internet speed.

        #Try to click on show more sections button
        try:
            browser.execute_script("""var zabutton = document.getElementsByClassName('udlite-btn udlite-btn-medium 
                                                                                    udlite-btn-secondary udlite-heading-sm 
                                                                                    curriculum--show-more--2tshH' 
                                                                                    )[0]; zabutton.click();""")
        # If there are less than 10 sections
        except WebDriverException:
            print("More sections button could not be found. This course has less than 10 sections then.")

        # Get the html
        content = browser.page_source
        browser.close()

        #Parse HTML
        course_page = BeautifulSoup(content, "lxml")

        # Get breadcrumb tags
        self.tags = []
        for tag in course_page.find("div", class_="topic-menu udlite-breadcrumb").find_all("a", class_="udlite-heading-sm"):
            self.tags.append(tag.text)

        # This is come noob code. I didn't know of any other way, so please, if you have a better alternative, create a PR :pray:
        self.no_of_rating = course_page.find("span", class_="", string=lambda x: x and x.startswith('(')).text.replace("(", "").replace(" ratings)", "")
        self.no_of_students = course_page.find("div", attrs={"data-purpose": "enrollment"}).text.replace("\n","").replace(" students", "")
        self.course_language = course_page.find("div", class_="clp-lead__element-item clp-lead__locale").text.replace("\n","")

        #Get the pointers present in "What you'll learn part"
        self.objectives = []
        for objective in course_page.find_all("span", class_="what-you-will-learn--objective-item--ECarc"):
            self.objectives.append(objective.text)

        # This is the sections array which will contain Section classes
        self.Sections = []

        string_section = []
        for s in course_page.find_all("div", class_="section--panel--1tqxC panel--panel--3NYBX"):
            string_section.append(str(s))
        for section_block in string_section:
            self.Sections.append(Section(section_block))

        # Get the requirements section
        self.requirements = []
        for requirement in course_page.find("div", class_="ud-component--course-landing-page-udlite--requirements").find_all("div", class_="udlite-block-list-item udlite-block-list-item-small udlite-block-list-item-tight udlite-block-list-item-neutral udlite-text-sm"):
            self.requirements.append(requirement.text)

        # Get the long description section. Each paragraph is concatenated to the description string separated by a "\n" or a new line.
        self.description = ""
        for parahraph in course_page.find("div", attrs={'data-purpose':'safely-set-inner-html:description:description'}).find_all("p"):
            self.description += parahraph.text + "\n"

        # Get the information in the target section section
        self.target_audience = []
        for a in course_page.find("div", attrs={'data-purpose': 'target-audience'}).find_all("li"):
            self.target_audience.append(a.text)

        # Get the url of the course
        self.banner = str(course_page.find("div", class_="intro-asset--asset--1eSsi").find("img").attrs['src']).replace("240x135","480x270")


def course_to_json(course):
    #Initialize a new Sections array which will contain coverted dictionaries instead of objects for json serialization
    new_section_list = []


    for section in course.Sections:
        # Initialize a new lessons array which will contain coverted dictionaries instead of objects for every section
        new_lesson_list = []

        for lesson in section.lessons:
            
            dict = lesson.__dict__         # Convert the lesson object to a dictionary
            del dict['lesson_html']        # Remove the html code from the dictionary
            new_lesson_list.append(dict)   # Add the dictionary to the new list

        
        section.lessons = new_lesson_list   #Update the lessons object array with the new lessons dictionary array for this section
        section_dict = section.__dict__     #Convert the section into a dictionary

        # Remove the html code from the dictionary
        del section_dict['html']            
        del section_dict['lesson_blocks']

        # Add the dictionary to the new list
        new_section_list.append(section_dict)

    #Update the sections object array with the new sections dictionary array 
    course.Sections = new_section_list

    # Dump the python object as a json in 'object.json' file. You can change this to whatever you want
    with open('object.json', 'w') as file:
        file.write(json.dumps(course.__dict__)) #Convert the course to dictionary and dump.
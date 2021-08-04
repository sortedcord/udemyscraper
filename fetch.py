from bs4 import BeautifulSoup
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
import time

class Course():
    
    def __init__(self, query):
        self.query = query    

    
    def fetchCourse(self):
        url = f"https://www.udemy.com/courses/search/?src=ukw&q={self.query}"
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
        link = links[0]

        title = soup.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE")
        description = soup.find('p', class_="udlite-text-sm course-card--course-headline--yIrRk")
        author = soup.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f")
        rating = soup.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8")

        other_info = soup.find_all('span', class_="course-card--row--1OMjg")
        truncated_info = other_info[0:3]
        duration = truncated_info[0]
        no_of_lectures = truncated_info[1]

        self.link = 'https://udemy.com'+link
        self.title = title.text
        self.description = description.text
        self.author = author.text
        self.rating = rating.text
        self.duration = duration.text
        self.no_of_lectures = no_of_lectures.text

from bs4 import BeautifulSoup
import requests
import os
from selenium import webdriver   # for webdriver
from selenium.webdriver.support.ui import WebDriverWait  # for implicit and explict waits
from selenium.webdriver.chrome.options import Options  # for suppressing the browser
from selenium.webdriver.common.action_chains import ActionChains
import time



url = 'https://www.udemy.com/course/the-complete-javascript-course/'

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

# with open('demo.html','w', encoding='utf-8') as file:
#     file.write(str(soup.prettify()))

# breadcrumbs = soup.find("div", class_="topic-menu udlite-breadcrumb")
# raw_tags = breadcrumbs.find_all("a", class_="udlite-heading-sm")
# tags = []
# for tag in raw_tags:
#     tags.append(tag.text)

# This is come noob code. I didn't know of any other way, so please, if you have a better alternative, create a PR :pray:
# no_of_ratings = soup.find("span", class_="", string=lambda x: x and x.startswith('(')).text.replace("(", "").replace(" ratings)", "")

# no_of_students = soup.find("div", attrs={"data-purpose": "enrollment"}).text.replace("\n","").replace(" students", "")

# course_language = soup.find("div", class_="clp-lead__element-item clp-lead__locale").text
# print(course_language)


## This does not show all of the sections, so I will be using selenium after all, firstly, to move the mouse to the get more sections one and then click on it. Which will be done in a later commit..

sections = soup.find_all("div", class_="section--panel--1tqxC panel--panel--3NYBX")

for section in sections:
    name = section.find("span", class_="section--section-title--8blTh")
    lessons = section.find_all("div", class_="udlite-block-list-item-content")
    for lesson in lessons:
        name = lesson.find("span")
        print(name.text)
        


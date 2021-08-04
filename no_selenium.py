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


sections = soup.find_all("div", class_="section--panel--1tqxC panel--panel--3NYBX")

for section in sections:
    name = section.find("span", class_="section--section-title--8blTh")
    lessons = section.find_all("div", class_="udlite-block-list-item-content")
    for lesson in lessons:
        name = lesson.find("span")
        print(name.text)
        


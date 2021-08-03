from bs4 import BeautifulSoup
from selenium import webdriver
import time

def fetchCourse(query):
    url = f"https://www.udemy.com/courses/search/?src=ukw&q={query}"
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(4)
    content = browser.page_source
    soup = BeautifulSoup(content, "html.parser")
    browser.close()
    title = soup.find('div', class_="udlite-focus-visible-target udlite-heading-md course-card--course-title--2f7tE")
    return title.text
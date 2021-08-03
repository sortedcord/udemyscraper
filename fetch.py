from os import truncate
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
    description = soup.find('p', class_="udlite-text-sm course-card--course-headline--yIrRk")
    author = soup.find('div', class_="udlite-text-xs course-card--instructor-list--lIA4f")
    rating = soup.find('span', class_="udlite-heading-sm star-rating--rating-number--3lVe8")

    other_info = soup.find_all('span', class_="course-card--row--1OMjg")
    truncated_info = other_info[0:3]
    duration = truncated_info[0]
    no_of_lectures = truncated_info[1]
    return title.text, description.text, author.text, rating.text, duration.text, no_of_lectures.text
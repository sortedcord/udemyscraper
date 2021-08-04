from bs4 import BeautifulSoup
import requests
import os


url = 'https://www.udemy.com/course/the-complete-javascript-course/'


page = requests.get(url)
content = page.content
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
        


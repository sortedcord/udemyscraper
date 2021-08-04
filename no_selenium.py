from bs4 import BeautifulSoup
import requests
import os


url = 'https://www.udemy.com/course/the-complete-javascript-course/'


page = requests.get(url)
content = page.content
soup = BeautifulSoup(content, "html.parser")

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

objectives = []
raw_obj = soup.find_all("span", class_="what-you-will-learn--objective-item--ECarc")
for objective in raw_obj:
    objectives.append(objective.text)


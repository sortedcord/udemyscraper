![scraper](docs/logo.png)

# Udemy Scraper

![License](https://img.shields.io/badge/LICENSE-GPL--3.0-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.9.6-blue?style=for-the-badge&logo=python&logoColor=white)
![Chromium](https://img.shields.io/badge/CHROMIUM-92.0.3-GREEN?style=for-the-badge&logo=GoogleChrome&logoColor=white)


A Web Scraper built with beautiful soup, that fetches udemy course information.

## Basic Usage
This section shows the basic usage of this script. Before this be sure to [install](#installation) this first before importing it in your file.

Udemyscraper contains a `UdemyCourse` class which can be imported into your file it takes just one argument which is `query` which is the seach query. It has a method called `fetch_course` which you can call after creating a UdemyCourse object.

```py
from udemyscraper import UdemyCourse

course = UdemyCourse('learn javascript')
course.fetch_course()
```

The following datatable contains all of the properties that can be fetched.

|Name             |Type         |Description                                          |Usage               |
|-----------------|-------------|-----------------------------------------------------|--------------------|
|`query`          |String       |Search term which is searched in the website   |`course.query`      |
|`link`           |URL (String) |url of the course.                             |`course.link`       |
|`title`          |String       |Title of the course                            |`course.title`      |
|`headline`       |String       |The headline usually displayed under the title |`course.headline`   |
|`instructor`     |String       |Name of the instructor of the course           |`course.instructor` |
|`rating`         |Integer      |Rating of the course out of 5                  |`course.rating`     |
|`no_of_ratings`  |Integer      |Number of rating the course has got           |`course.no_of_ratings` |
|`duration`       |String       |Duration of the course in hours and minutes    |`course.duration`   |
|`no_of_lectures` |String |Gives the number of lectures in the course (lessons) |`course.no_of_lectures`|
|`no_of_sections` |String       |Gives the number of sections in the courses |`course.no_of_lectures` |
|`tags`           |List         |Is the list of tags of the course (Breadcrumbs) |`course.tags[1]`    |
|`student_enrolls` |Integer     |Gives the number of students enrolled | `course.student_enrolls` |
|`course_language` | String     |Gives the language of the course | `course.course_language` | 
|`objectives` |List     |List containing all the objectives for the course | `course.objectives[2]`  |
|`Sections`   |List      |List containing all the section objects for the course | `course.Sections[2]` |
|`requirements` |List    |List containing all the requirements for the course | `course.requirements` |
|`description` |String   |Gives the description paragraphs of the course |`course.description` |
|`target_audience` |List |List containing the points under Target Audience heading |`course.target_audience` |
|`banner` |String |URL for the course banner image |`course.banner`

#### Sections Class

|Name             |Type         |Description                                          |Usage               |
|-----------------|-------------|-----------------------------------------------------|--------------------|
|`name` |String  |Returns the name of the section of the course |`course.Sections[4].name` |
|`lessons` |List |List with all the lesson objects for the section | `course.Sections[4].lessons[2]` |

#### Lessons Class

|Name             |Type         |Description                                          |Usage               |
|-----------------|-------------|-----------------------------------------------------|--------------------|
|`name` |String |Gives the name of the lesson |`course.Sections[4].lessons[2].name` |

## Installation

### Virtual Environment

Firstly, it is recommended to install and run this inside of a virtual environment. You can do so by using the `virtualenv` library and then activating it.

```sh
pip install virtualenv

virtualenv somerandomname

```

Activating for \*nix

```sh
source somerandomname/bin/activate
```

Activating for Windows

```
somerandomname\Scripts\activate
```

### Package Installation

```sh
pip install -r requirements.txt
```

### Choosing Browser

A browser window may not pop-up as I have enabled the  `headless` option so the entire process takes minimal resources. As of [commit 633ec08](https://github.com/sortedcord/udemy-web-scraper/commit/633ec0875cd6e61fcc4f9309bc2a099c3e7cf6fb) the headless browser is a bit buggy when it comes to executing javascript commands, so it is possible that the browser process may not terminate properly so be sure to check for that either in Task Manager, HTOP, etc and end it.

This script works with firefox as well as chrome.

#### Running with Chrome (or chromium)

To run this script you need to have chrom(ium) installed on the machine as well as the chromedriver binary which can be downloaded from this [page](https://chromedriver.chromium.org/downloads). Make sure that the binary you have installed works on your platform/ architecture and the the driver version corresponds to the version of the browser you have downloaded.

I have already provided a windows binary of the driver in the repo itself which supports chrom(ium) 92. You can use that or you can get your specific driver from the link above.

#### Running with Firefox

In order to run this script this firefox, you need to have firefox installed as well as the `gekodriver` executable file in this directory or in your path.
You can download the gekodriver from [here](https://github.com/mozilla/geckodriver/releases).

Once you have finished setting up the driver, you need to make a few changes in the srcipt to use firefox instead of chrome.

This is what the file currently looks like. As you can see, it uses the chrome engine by default.
```py
# udemyscraper.py

option = Options()
option.add_argument('headless')
option.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(
    executable_path='chromedriver.exe', chrome_options=option) 
```

And these are the changes you would have to make to use firefox.
```py
fireFoxOptions = webdriver.FirefoxOptions()
brower = webdriver.Firefox(firefox_options=fireFoxOptions)
```

If you want to use Firefox `headless` then add the following line before initializing the browser variable
```py
fireFoxOptions.set_headless()
```

## Approach

It is fairly easy to webscrape sites, however, there are some sites that are not that scrape-friendly. Scraping sites, in itself is perfectly legal however there have been cases of lawsuits against web scraping, some companies \*cough Amazon \*cough consider web-scraping from its website illegal however, they themselves, web-scrape from other websites. And then there are some sites like udemy, that try to prevent people from scraping their site.

Using BS4 in itself, doesn't give the required results back, so I had to use a browser engine by using selenium to fetch the courses information. Initially, even that didn't work out, but then I realised the courses were being fetch asynchronously so I had to add a bit of delay. So fetching the data can be a bit slow initially.

## Functionality

As of this commit, the script can search udemy for the search term you input and get the courses link, and all the other overview details like description, instructor, duration, rating, etc.

Here is a json representation of the data it can fetch as of now:-

```json
{
  "query": "The Complete Angular Course: Beginner to Advanced",
  "link": "https://udemy.com/course/the-complete-angular-master-class/",
  "title": "The Complete Angular Course: Beginner to Advanced",
  "headline": "The most comprehensive Angular 4 (Angular 2+) course. Build a real e-commerce app with Angular, Firebase and Bootstrap 4",
  "instructor": "Mosh Hamedani",
  "rating": "4.5",
  "duration": "29.5 total hours",
  "no_of_lectures": "376 lectures",
  "tags": ["Development", "Web Development", "Angular"],
  "no_of_rating": "23,910",
  "no_of_students": "96,174",
  "course_language": "English",
  "objectives": [
    "Establish yourself as a skilled professional developer",
    "Build real-world Angular applications on your own",
    "Troubleshoot common Angular errors",
    "Master the best practices",
    "Write clean and elegant code like a professional developer"
  ],
  "Sections": [
    {
      "name": "Introduction",
      "lessons": [{ "name": "Introduction" }, { "name": "What is Angular" }],
      "no_of_lessons": 12
    },
    {
      "name": "TypeScript Fundamentals",
      "lessons": [
        { "name": "Introduction" },
        { "name": "What is TypeScript?" }
      ],
      "no_of_lessons": 18
    },
    {
      "name": "Angular Fundamentals",
      "lessons": [
        { "name": "Introduction" },
        { "name": "Building Blocks of Angular Apps" }
      ],
      "no_of_lessons": 10
    }
  ],
  "requirements": [
    "Basic familiarity with HTML, CSS and JavaScript",
    "NO knowledge of Angular 1 or Angular 2 is required"
  ],
  "description": "\nAngular is one of the most popular frameworks for building client apps with HTML, CSS and TypeScript. If you want to establish yourself as a front-end or a full-stack developer, you need to learn Angular.\n\nIf you've been confused or frustrated jumping from one Angular 4 tutoria...",
  "target_audience": [
    "Developers who want to upgrade their skills and get better job opportunities",
    "Front-end developers who want to stay up-to-date with the latest technology"
  ],
  "banner": "https://foo.com/somepicture.jpg"
}
```

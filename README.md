# udemy-web-scraper

A Web Scraper built with beautiful soup, that fetches udemy course information.

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

### Chrome setup

Be sure to have chrome installed and install the corresponding version of chromedriver. I have already provided a windows binary file. If you want, you can install the linux binary for the chromedriver from its page.

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

## Usage

In order to use the scraper, import it as a module and then create a new course class like so-

```py
from udemyscraper import UdemyCourse
```

This will import the `UdemyCourse` class and then you can create an instance of it and then pass the search query to it. Prefarably the exact course name.

```py
from udemyscraper import UdemyCourse

javascript_course = UdemyCourse("Javascript course for beginners")
```

This will create an empty instance of `UdemyCourse`. To fetch the data, you need to call the `fetch_course` function.

```py
javascript_course.fetch_course()
```

Now that you have the course, you can access all of the courses' data as shown [here](#Functionality).

```py
print(javascript_course.Sections[2].lessons[1].name) # This will print out the 3rd Sections' 2nd Lesson's name
```

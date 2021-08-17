![scraper](docs/logo.png)


![License](https://img.shields.io/badge/LICENSE-GPL--3.0-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/PYTHON-3.9.6-blue?style=for-the-badge&logo=python&logoColor=white)
![Chromium](https://img.shields.io/badge/CHROMIUM-92.0.3-GREEN?style=for-the-badge&logo=GoogleChrome&logoColor=white)


A Web Scraper built with beautiful soup, that fetches udemy course information.

## Table Of Contents

- [Table Of Contents](#table-of-contents)
- [Basic Usage](#basic-usage)
- [Installation](#installation)
  - [Virtual Environment](#virtual-environment)
  - [Package Installation](#package-installation)
- [Choosing Browser](#choosing-browser)
  - [Running with Chrome (or chromium)](#running-with-chrome-or-chromium)
  - [Running with Firefox](#running-with-firefox)
  - [Suppressing Browser](#suppressing-browser)
- [Approach](#approach)
  - [Why not just use the Udemy's API?](#why-not-just-use-the-udemys-api)
- [Standalone Usage](#standalone-usage)
  - [List of Commands](#list-of-commands)
- [Functionality](#functionality)
  - [Datatables](#datatables)
    - [Course Class](#course-class)
    - [Section Class](#section-class)
    - [Lesson Class](#lesson-class)
  - [Output/ Dumping data](#output-dumping-data)
    - [Converting to Dictionary](#converting-to-dictionary)
    - [Dumping as JSON](#dumping-as-json)
    - [Dumping as CSV](#dumping-as-csv)
    - [Dumping as XML](#dumping-as-xml)
      - [For Jellyfin users](#for-jellyfin-users)
- [Contributing](#contributing)

## Basic Usage
This section shows the basic usage of this script. Before this be sure to [install](#installation) this first before importing it in your file.

Udemyscraper contains a `UdemyCourse` class which can be imported into your file it takes just one argument which is `query` which is the seach query. It has a method called `fetch_course` which you can call after creating a UdemyCourse object.

```py
from udemyscraper import UdemyCourse

course = UdemyCourse('learn javascript')
course.fetch_course()
```

## Installation

### Virtual Environment

Firstly, it is recommended to install and run this inside of a virtual environment. You can do so by using the `virtualenv` library and then activating it.

```bash
pip install virtualenv

virtualenv somerandomname

```

Activating for \*nix

```bash
source somerandomname/bin/activate
```

Activating for Windows

```
somerandomname\Scripts\activate
```

### Package Installation

```bash
pip install -r requirements.txt
```

## Choosing Browser

A browser window may not pop-up as I have enabled the  `headless` option so the entire process takes minimal resources.

This script works with firefox as well as chrome.

### Running with Chrome (or chromium)

To run this script you need to have chrom(ium) installed on the machine as well as the chromedriver binary which can be downloaded from this [page](https://chromedriver.chromium.org/downloads). Make sure that the binary you have installed works on your platform/ architecture and the the driver version corresponds to the version of the browser you have downloaded.

I have already provided a windows binary of the driver in the repo itself which supports chrom(ium) 92. You can use that or you can get your specific driver from the link above.

To set chrome as default you can pass in an argument while initializing the class though it is set to chrome by default.

```py
mycourse = UdemyCourse(browser_preference="CHROME")
```
Or you can pass in a argument while using `main.py`
```bash
python3 main.py -b chrome
```

### Running with Firefox

In order to run this script this firefox, you need to have firefox installed as well as the `gekodriver` executable file in this directory or in your path.
You can download the gekodriver from [here](https://github.com/mozilla/geckodriver/releases). Or use the one provided with the source code.

To use firefox instead of chrome,  you can pass in an argument while initializing the class:

```py
mycourse = UdemyCourse(browser_preference="FIREFOX")
```
Or you can pass in a argument while using `main.py`
```bash
python3 main.py -b firefox
```
### Suppressing Browser
The `headless` option is enabled by default. But in case you want to disable it for debugging purposes, you may do so by passing the `headless` argument to `false`

```py
mycourse = UdemyCourse(headless=False)
```

Or specify the same for `main.py`
```bash
python3 main.py -h false
```

## Approach

It is fairly easy to webscrape sites, however, there are some sites that are not that scrape-friendly. Scraping sites, in itself is perfectly legal however there have been cases of lawsuits against web scraping, some companies \*cough Amazon \*cough consider web-scraping from its website illegal however, they themselves, web-scrape from other websites. And then there are some sites like udemy, that try to prevent people from scraping their site.

Using BS4 in itself, doesn't give the required results back, so I had to use a browser engine by using selenium to fetch the courses information. Initially, even that didn't work out, but then I realised the courses were being fetch asynchronously so I had to add a bit of delay. So fetching the data can be a bit slow initially.

### Why not just use the Udemy's API?

Even I thought of that after some digging around as I did not know that such an API existed. However, this requires you to have a udemy account already. I might add the use of this Api in the future, but right now, I would like to keep things simple. Moreover, this kind of front-end webscraping does not require authentication.

## Standalone Usage
In case you do not wish to use the module in your own python file but you just need to dump the data, you can do so by running the main.py file along with passing the required arguments.

``` bash
python3 main.py <command>    
```

### List of Commands

![Commands](docs/command.svg)

## Functionality

As of this commit, the script can search udemy for the search term you input and get the courses link, and all the other overview details like description, instructor, duration, rating, etc.
### Datatables

The following datatable contains all of the properties that can be fetched.

#### Course Class

| Name              | Type         | Description                                              | Usage                    |
|-------------------|--------------|----------------------------------------------------------|--------------------------|
| `query`           | String       | Search term which is searched in the website             | `course.query`           |
| `link`            | URL (String) | url of the course.                                       | `course.link`            |
| `title`           | String       | Title of the course                                      | `course.title`           |
| `headline`        | String       | The headline usually displayed under the title           | `course.headline`        |
| `instructor`      | String       | Name of the instructor of the course                     | `course.instructor`      |
| `rating`          | Integer      | Rating of the course out of 5                            | `course.rating`          |
| `no_of_ratings`   | Integer      | Number of rating the course has got                      | `course.no_of_ratings`   |
| `duration`        | String       | Duration of the course in hours and minutes              | `course.duration`        |
| `no_of_lectures`  | String       | Gives the number of lectures in the course (lessons)     | `course.no_of_lectures`  |
| `no_of_sections`  | String       | Gives the number of sections in the courses              | `course.no_of_lectures`  |
| `tags`            | List         | Is the list of tags of the course (Breadcrumbs)          | `course.tags[1]`         |
| `price`           | String       | Price of the course in local currency                    | `course.price`           |
| `student_enrolls` | Integer      | Gives the number of students enrolled                    | `course.student_enrolls` |
| `course_language` | String       | Gives the language of the course                         | `course.course_language` |
| `objectives`      | List         | List containing all the objectives for the course        | `course.objectives[2]`   |
| `Sections`        | List         | List containing all the section objects for the course   | `course.Sections[2]`     |
| `requirements`    | List         | List containing all the requirements for the course      | `course.requirements`    |
| `description`     | String       | Gives the description paragraphs of the course           | `course.description`     |
| `target_audience` | List         | List containing the points under Target Audience heading | `course.target_audience` |
| `banner`          | String       | URL for the course banner image                          | `course.banner`          |

#### Section Class

| Name       | Type   | Description                                      | Usage                           |
|------------|--------|--------------------------------------------------|---------------------------------|
| `name`     | String | Returns the name of the section of the course    | `course.Sections[4].name`       |
| `duration` | String | The duration of the specific course              | `course.Sections[4].duration`   |
| `lessons`  | List   | List with all the lesson objects for the section | `course.Sections[4].lessons[2]` |

#### Lesson Class

| Name   | Type   | Description                  | Usage                                |
|--------|--------|------------------------------|--------------------------------------|
| `name` | String | Gives the name of the lesson | `course.Sections[4].lessons[2].name` |


### Output/ Dumping data

#### Converting to Dictionary

The entire course object is converted into a dictionary by using nested object to dictionary conversion iterations.

```py
from udemyscraper import course_to_dict

# Assuming you have already created a course object and fetched the data
dictionary_course = course_to_dict(course)
```

#### Dumping as JSON

Currently, the script can convert the entire course into a dictionary, parse it into a json file and then dump it to a json file. You can do this by calling the `course_to_json()` function like so:

```py
from udemyscraper import course_to_json

# Assuming you have already created a course object and fetched the data
course_to_json(course)
```
This will dump the data to `object.json` file in the same directory. If you want to change the filename, then you can do so by editing [this code](udemyscraper.py#L206).

#### Dumping as CSV
Currently not implemented yet.

#### Dumping as XML
Currently not implemented yet.

##### For Jellyfin users
Jellyfin metadata uses XML structure for its `.nfo` files. For images, we only have one resource which is the poster of the file. It might be possible to write a custom XML structure for jellyfin. Currently in development.



## Contributing
Issues and PRs as well as discussions are always welcomes, but please make an issue of a feature/code that you would be modifying before starting a PR.

Currently there are lots of features I would like to add to this script. You can check [this page](https://github.com/sortedcord/udemy-web-scraper/projects/1) what the current progress is.

For further instructions, do read [contributing.md](CONTRIBUTING.md).
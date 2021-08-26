import json
from udemyscraper.utils import loginfo

def quick_display(course):
    print("===================== Fetched Course =====================", "\n")
    print(course.title)
    print(course.headline)
    print(f"URL: {course.link}")
    print(f"Instructed by {course.instructors}")
    print(f"{course.rating} out of 5 ({course.no_of_ratings})")
    print(f"Duration: {course.duration}")
    print(f"{course.no_of_lectures} Lessons and {course.no_of_sections} Sections")


def course_to_dict(course):
    # Initialize a new Sections array which will contain coverted dictionaries instead of objects for json serialization
    new_section_list = []

    for section in course.Sections:
        # Initialize a new lessons array which will contain coverted dictionaries instead of objects for every section
        new_lesson_list = []

        for lesson in section.Lessons:

            dict = lesson.__dict__         # Convert the lesson object to a dictionary
            new_lesson_list.append(dict)   # Add the dictionary to the new list

        # Update the lessons object array with the new lessons dictionary array for this section
        section.Lessons = new_lesson_list
        section_dict = section.__dict__  # Convert the section into a dictionary

        # Add the dictionary to the new list
        new_section_list.append(section_dict)

    # Update the sections object array with the new sections dictionary array
    course.Sections = new_section_list
    loginfo("Successfully parsed to a dicitonary")
    # return the dictionary
    return course.__dict__


def course_to_json(course, output_file='output.json'):
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a json in 'object.json' file. You can change this to whatever you want
    with open(output_file, 'w') as file:
        # Convert the course to dictionary and dump.
        file.write(json.dumps(course))
        loginfo(f"File course dumped as {output_file}")

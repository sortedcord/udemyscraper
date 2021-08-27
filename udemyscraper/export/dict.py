from udemyscraper.utils import loginfo

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
from udemyscraper.utils import loginfo
from udemyscraper.export.dict import course_to_dict

import csv

def course_to_csv(courses, output_file='output.csv'):
    if output_file == None:
        output_file = 'course.json'

    dict_courses_array = []

    for course in courses:
        inline_instructors = ""
        for instructor in course.instructors:
            if course.instructors.index(instructor) != len(course.instructors)+1:
                inline_instructors = inline_instructors + instructor + ", "
            else:
                inline_instructors = inline_instructors + instructor
        course.instructors = inline_instructors

        inline_tags = ""
        for tag in course.tags:
            if course.tags.index(tag) != len(course.tags)+1:
                inline_tags = inline_tags + tag + ", "
            else:
                inline_tags = inline_tags + tag
        course.tags = inline_tags

        inline_objectives = ""
        for objective in course.objectives:
            if course.objectives.index(objective) != len(course.objectives)+1:
                inline_objectives = inline_objectives + objective + ", "
            else:
                inline_objectives = inline_objectives + objective
        course.objectives = inline_objectives

        inline_requirements = ""
        for requirement in course.requirements:
            if course.requirements.index(requirement) != len(course.requirements)+1:
                inline_requirements = inline_requirements + requirement + ", "
            else:
                inline_requirements = inline_requirements + requirement
        course.requirements = inline_requirements

        inline_target_audiences = ""
        for target_audience in course.target_audience:
            if course.target_audience.index(target_audience) != len(course.target_audience)+1:
                inline_target_audiences = inline_target_audiences + target_audience + ", "
            else:
                inline_target_audiences = inline_target_audiences + target_audience
        course.target_audience = inline_target_audiences

        # Convert the course to dictionary
        course = course_to_dict(course)

        del course["Preferences"]
        del course["Sections"]

        dict_courses_array.append(course)
    
    with open(output_file, 'w', encoding='utf-8') as file:

        writer = csv.DictWriter(file, fieldnames = [*dict_courses_array[0]])
        writer.writeheader()
        writer.writerows(dict_courses_array)

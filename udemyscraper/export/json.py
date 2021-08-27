from udemyscraper.utils import loginfo
from udemyscraper.export.dict import course_to_dict

import json

def course_to_json(course, output_file='output.json'):
    if output_file == None:
        output_file = 'course.json'
    # Convert the course to dictionary
    course = course_to_dict(course)

    # Dump the python object as a json in 'object.json' file. You can change this to whatever you want
    with open(output_file, 'w') as file:
        # Convert the course to dictionary and dump.
        file.write(json.dumps(course))
        loginfo(f"File course dumped as {output_file}")
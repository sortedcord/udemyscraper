from dict2xml import dict2xml

from udemyscraper.export.dict import course_to_dict as dict

def course_to_xml(course, output_file=None):
    course = dict(course)
    del course['Preferences']
    output_file = 'course.xml'
    xml = dict2xml(course, wrap ='course', indent ="  ")
    print(course)
    # with open(output_file, 'w', encoding='utf-8') as file:
    #     file.write(course)

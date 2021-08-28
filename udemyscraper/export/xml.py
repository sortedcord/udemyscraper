from dicttoxml import dicttoxml

from udemyscraper.export.dict import course_to_dict as dict

def course_to_xml(course, output_file=None):
    course = dict(course)
    del course['Preferences']
    output_file = 'course.xml'

    xml = dicttoxml(course)
    xml_decode = xml.decode()
    xmlfile = open(output_file, "w", encoding='utf-8')
    xmlfile.write(xml_decode)
    xmlfile.close()

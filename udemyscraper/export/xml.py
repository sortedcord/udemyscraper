import dicttoxml

from udemyscraper.export.dict import course_to_dict as dict

def course_to_xml(course, output_file=None):
    course = dict(course)
    del course['Preferences']
    
    if output_file is None or output_file == '':
        output_file = 'course.xml'

    xml = dicttoxml.dicttoxml(course, custom_root="course" ,item_func = lambda x: x[:-1])
    xml_decode = xml.decode()
    xmlfile = open(output_file, "w", encoding='utf-8')
    xmlfile.write(xml_decode)
    xmlfile.close()

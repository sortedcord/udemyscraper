from udemyscraper.export.csv import course_to_csv as csv
from udemyscraper.export.json import course_to_json as json
from udemyscraper.export.dict import course_to_dict as dict
from udemyscraper.export.print import print_course as printc
from udemyscraper.export.xml import course_to_xml as xml


def export_course(course, mode, output=None):
    if mode != None:
        if mode == 'json':
            json(course, output)
        elif mode == 'csv':
            csv(course, output)
        elif mode == 'xml':
            xml(course, output)
        elif mode == "print":
            printc(course)
        elif 'dict' in mode:
            return dict(course)
        else:
            print(f"{mode} is not a valid export method")
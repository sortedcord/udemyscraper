from fetch import UdemyCourse
from fetch import convert_to_json

search_term = input("Enter Search Term: ")

udemy_course = UdemyCourse(search_term)
udemy_course.fetch_course()

convert_to_json(udemy_course)
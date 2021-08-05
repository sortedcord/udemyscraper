from fetch import Course
from fetch import convertToJson

search_term = input("Enter Search Term: ")

udemy_course = Course(search_term)
udemy_course.fetchCourse()

convertToJson(udemy_course)

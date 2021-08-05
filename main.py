from fetch import Course
from fetch import convertToJson

search_term = "The Complete Angular Course: Beginner to Advanced"

udemy_course = Course(search_term)
udemy_course.fetchCourse()

convertToJson(udemy_course)

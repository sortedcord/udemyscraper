from fetch import Course

search_term = input("Enter your search term here: ")

udemy_course = Course(search_term)
udemy_course.fetchCourse()
udemy_course.getCourseInfo()

print(udemy_course.sections[1].name)

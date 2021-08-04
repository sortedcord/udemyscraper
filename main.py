from fetch import Course

search_term = input("Enter your search term here: ")

udemy_course = Course(search_term)
udemy_course.fetchCourse()
udemy_course.getCourseInfo()

print(udemy_course.Sections[2].lessons[2].name)


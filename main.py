from fetch import Course

search_term = input("Enter your search term here: ")

udemy_course = Course(search_term)
udemy_course.fetchCourse()
print(udemy_course.description)
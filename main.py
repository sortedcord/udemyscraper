from fetch import fetchCourse

search_term = input("Enter the search term here: ")
course_title = fetchCourse(search_term)
print(course_title)

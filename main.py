from fetch import fetchCourse

# search_term = input("Enter the search term here: ")
search_term = input("Enter the search term: ")
url, title, description, author, rating, duration, no_of_lectures = fetchCourse(search_term)

print(url)
print(f"============ {title} ============")
print(f"\n", f"Description: {description}")
print(f"This course is instructed by {author}")
print(f"This course got {rating} stars out of 5")
print(no_of_lectures)


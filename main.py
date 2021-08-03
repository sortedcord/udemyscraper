from bs4 import BeautifulSoup

with open('html/dummy.index.html', 'r') as f:
    content = f.read()
    # print(content)

    soup = BeautifulSoup(content, 'lxml')
    # print(soup.prettify())

    titles = soup.find_all('h1')
    
    for title in titles:
        print(title.text)
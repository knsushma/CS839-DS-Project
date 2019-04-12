import urllib.request
from bs4 import BeautifulSoup

movie_list = []
for num in range(1,500):
    themoviedb = "https://www.themoviedb.org/movie?page=" + str(num)
    resp = urllib.request.urlopen(themoviedb)
    soup = BeautifulSoup(resp, 'html.parser',from_encoding=resp.info().get_param('charset'))
    for link in soup.find_all('a', {'class' : 'title result'}, href=True):
        href_link = link['href']
        if href_link.startswith("/movie/") and len(href_link) == 13:
            movie_list.append(link["href"])

file = open('themoviedb.txt', 'w+')
for item in movie_list:
    file.write("%s\n" % item)
file.close()
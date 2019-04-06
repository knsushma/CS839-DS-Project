from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import json


extractors = ["Rating", "Genre", "Directed By", "Runtime"]
text_file = open("./rottentomatoes_hyperlinks.txt")
links = [link.strip("\n") for link in text_file]
print(links)

for link in links[:10]:
    web_page = urlopen(Request(link))
    soup = BeautifulSoup(web_page, 'html.parser',from_encoding=web_page.info().get_param('charset'))

    name = soup.find("h1", {"class" : "mop-ratings-wrap__title mop-ratings-wrap__title--top"}).text
    print(name)
    contents = soup.find_all("li", {"class" : "meta-row clearfix"})
    for content in contents:
         content_soup = BeautifulSoup(str(content), 'html.parser')
         #print(content)
         #print(content_soup.find("div", {"class" : "meta-label subtle"}).text.replace(":", "").strip() in extractors)
         if content_soup.find("div", {"class" : "meta-label subtle"}).text.replace(":", "").strip() in extractors:
             value = content_soup.find("div", {"class" : "meta-value"}).text
             print(value.strip())
    print()

# for link in links[]:
#
#     web_page = urlopen(Request(link))
#     soup = BeautifulSoup(web_page, 'html.parser',from_encoding=web_page.info().get_param('charset'))
#

# web_page = urlopen(Request("https://www.rottentomatoes.com/browse/dvd-streaming-all/"))
# soup = BeautifulSoup(web_page, 'html.parser',from_encoding=web_page.info().get_param('charset'))
#
# links = []
# for link in soup.find_all("a", attrs={'href': re.compile("^https://")}):
#     url = link.get('href')
#     if ("www.rottentomatoes.com/tv/") in url and url not in links:
#         print(url)
#         links.append(url)
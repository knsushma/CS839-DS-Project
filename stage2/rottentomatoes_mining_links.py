from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import re
import json

links = []
for page_num in range(1, 101):
    web_response = urlopen(Request("https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page="+str(page_num)))
    json_response = json.load(web_response)

    for item in json_response["results"]:
        links.append("https://www.rottentomatoes.com" + item["url"])

with open("./rottentomatoes_hyperlinks.txt", "w") as output_file:
    for link in links:
        output_file.write("%s\n" % link)

# web_page = urlopen(Request("https://www.rottentomatoes.com/browse/dvd-streaming-all/"))
# soup = BeautifulSoup(web_page, 'html.parser',from_encoding=web_page.info().get_param('charset'))
#
# links = []
# for link in soup.find_all("a", attrs={'href': re.compile("^https://")}):
#     url = link.get('href')
#     if ("www.rottentomatoes.com/tv/") in url and url not in links:
#         print(url)
#         links.append(url)

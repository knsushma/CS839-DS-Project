from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv

# Read links for webpages from which we extract attributes/data
text_file = open("./rottentomatoes_hyperlinks.txt")
links = [link.strip("\n") for link in text_file]

# Final data table that contains multiple tuple with each tuple having attributes (Extractors mentioned below)
table = []
table.append(["Name", "Rating", "Genre", "Directed By", "Runtime"])
extractors = ["Rating", "Genre", "Directed By", "Runtime"]

for link in links:
    tuple = []
    web_page = ""
    # Read contents of the webpage, continue if webpage is Not Found/Unreachable/Operation Timed Out
    try:
        web_page = urlopen(Request(link))
    except HTTPError as e:
        print("Error Code: ", e)
        continue
    except URLError as e:
        print("Error Code ", e)
        continue

    #parse the HTML content of the webpage
    soup = BeautifulSoup(web_page, 'html.parser',from_encoding=web_page.info().get_param('charset'))
    #Extract the attributes by tag name
    name = soup.find("h1", {"class" : "mop-ratings-wrap__title mop-ratings-wrap__title--top"}).text
    tuple.append(name)
    contents = soup.find_all("li", {"class" : "meta-row clearfix"})
    attribute_map = {}
    for content in contents:
        content_soup = BeautifulSoup(str(content), 'html.parser')
        attribute_name = content_soup.find("div", {"class" : "meta-label subtle"}).text.replace(":", "").strip()
        if  attribute_name in extractors:
            value = content_soup.find("div", {"class" : "meta-value"}).text
            attribute_map[attribute_name] = ' '.join(value.split())
    for e in extractors:
        tuple.append(attribute_map.get(e, "NA"))
    table.append(tuple)

csv_file = csv.writer(open("./rottentomatoes_data.csv", "w"), dialect="excel")
csv_file.writerows(table)

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
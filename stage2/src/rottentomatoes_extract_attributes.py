from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import csv
import json

# Read links for webpages from which we extract attributes/data
text_file = open("./rottentomatoes_movie_hyperlinks.txt")
links = [link.strip("\n") for link in text_file]

# Final data table that contains multiple tuple with each tuple having attributes (Extractors mentioned below)
table = []
table.append(["Name", "Year", "Rating", "Genre", "Directed By", "Runtime"])
extractors = ["Rating", "Genre", "Directed By", "Runtime"]

year_count = 0
loop_num = 0
for link in links:
    print("Working on link: {0}".format(loop_num))

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
    year = soup.find("span", {"class" : "h3 year heroImageNoMovie-year"})
    if (year):
        year_count += 1
        tuple.append(year.text)
    else:
        #Extract from script
        try:
            year = json.loads((soup.find("script", {"id" : "mps-page-integration"}).text.strip().split(";")[0]).split("=")[1].strip())['cag[release]']
            tuple.append(year)
        except Exception as e:
            tuple.append("NA")
    contents = soup.find_all("li", {"class" : "meta-row clearfix"})
    attribute_map = {}
    for content in contents:
        content_soup = BeautifulSoup(str(content), 'html.parser')
        attribute_name = content_soup.find("div", {"class" : "meta-label subtle"}).text.replace(":", "").strip()
        if  attribute_name in extractors:
            value = content_soup.find("div", {"class" : "meta-value"}).text
            if attribute_name == "Rating":
                attribute_map[attribute_name] = ' '.join(value.split()).split("(")[0].strip()
            else:
                attribute_map[attribute_name] = ' '.join(value.split())

    for e in extractors:
        tuple.append(attribute_map.get(e, "NA"))
    table.append(tuple)

    loop_num += 1

# Write the contents of table (A list of lists with each list representing a tuple)
csv_file = csv.writer(open("../data/rottentomatoes_data.csv", "w"), dialect="excel")
csv_file.writerows(table)
#print(table)
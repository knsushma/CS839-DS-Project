import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

imdb_movie_links = []
base_string = "https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page="

# Each page has 100 movies, taking 52 pages to get 5000 movies with a buffer of 200 more.
for page_num in range(1, 53):
    print("In Page: " + str(page_num))
    url_link = base_string + str(page_num)

    try:
        resp = urllib.request.urlopen(url_link)
    except HTTPError as e:
        print("Error Code: ", e)
        continue
    except URLError as e:
        print("Error Code ", e)
        continue

    soup = BeautifulSoup(resp, 'html.parser', from_encoding=resp.info().get_param('charset'))
    temp_list = []

    for link in soup.find_all('a', href=True):
        if link['href'].startswith("/title/") and link['href'].endswith("ref_=ttls_li_tt"):
            if link["href"] not in temp_list:
                temp_list.append(link["href"])
    imdb_movie_links.extend(temp_list)

write_file = open('imdb_movie_hyperlinks.txt', 'w+')
for item in imdb_movie_links:
    write_file.write("https://www.imdb.com{0}\n".format(item))
write_file.close()
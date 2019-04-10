import urllib.request
from urllib.error import HTTPError, URLError
import csv
from bs4 import BeautifulSoup


text_file = open("./imdb_movie_hyperlinks.txt")
links = [link.strip("\n") for link in text_file]

table = [["Name", "Rating", "Genre", "Directed By", "Runtime", "Year"]]

count = 1

for link in links:

    try:
        resp = urllib.request.urlopen(link)
    except HTTPError as e:
        print("Error Code: ", e)
        continue
    except URLError as e:
        print("Error Code ", e)
        continue

    try:
        soup = BeautifulSoup(resp, 'html.parser', from_encoding=resp.info().get_param('charset'))
        movie_features = []

        # MOVIE NAME AND YEAR
        name = soup.find('h1', {"class": ["", "long"]})
        if name:
            name = name.text
            if name:
                title_array = name.split('\xa0')
                movie_name = title_array[0]
                if len(title_array) > 1:
                    s = title_array[1]
                    movie_year = s[s.find("(")+1:s.find(")")]
                else:
                    movie_year = "NA"
            else:
                movie_name = "NA"
                movie_year = "NA"
        else:
            movie_name = "NA"
            movie_year = "NA"

        # INFO: RATING, RUNTIME, GENRES
        name = soup.find('div', class_='subtext')
        name = name.text
        info_array = ''.join(name.split())
        info_array = info_array.split('|')
        movie_rating = info_array[0]
        movie_runtime = info_array[1]
        movie_genres = info_array[2]

        # DIRECTOR
        name = soup.find('div', class_='credit_summary_item')
        if name:
            name = name.text
            if name:
                directors = name.replace('\n', '').strip().split(":", 1)[1]
                movie_directors = directors if directors != "" else "NA"
            else:
                movie_directors = "NA"
        else:
            movie_directors = "NA"

        # UPDATE THE MOVIE FEATURES
        movie_features.append(movie_name)
        movie_features.append(movie_rating)
        movie_features.append(movie_genres)
        movie_features.append(movie_directors)
        movie_features.append(movie_runtime)
        movie_features.append(movie_year)

        print("Working on movie: " + str(count))
        count += 1
        table.append(movie_features)
    except:
        print("Generic Exception at link: {0}".format(link))

# WRITE THE MOVIE FEATURES TO THE CSV
csv_file = csv.writer(open("../DATA/imdb_data.csv", "w", newline=""), dialect="excel")
csv_file.writerows(table)

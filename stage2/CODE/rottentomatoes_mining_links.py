from urllib.request import Request, urlopen
import json

links = []
loop_num = 0
for page_num in range(1, 170):
    print("Working on Page: {0}".format(loop_num))

    #web_response = urlopen(Request("https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=release&type=dvd-streaming-all&page="+str(page_num)))
    web_response = urlopen(Request("https://www.rottentomatoes.com/api/private/v2.0/browse?maxTomato=100&maxPopcorn=100&services=amazon%3Bhbo_go%3Bitunes%3Bnetflix_iw%3Bvudu%3Bamazon_prime%3Bfandango_now&certified&sortBy=tomato&type=dvd-streaming-all&page=" + str(page_num)))
    json_response = json.load(web_response)

    for item in json_response["results"]:
        links.append("https://www.rottentomatoes.com" + item["url"])

    loop_num += 1

text_file = open("./rottentomatoes_movie_hyperlinks.txt", "w")
for link in links:
    text_file.write("%s\n" % link)
text_file.close()
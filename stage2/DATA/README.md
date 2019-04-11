## [Web Crawling](https://sites.google.com/view/data-science-ask/home/web-crawling?authuser=0)

We chose to extract movies information from two well known movie rating websites [IMDB](https://www.imdb.com/) and [RottenTomatoes](https://www.rottentomatoes.com/).
To have more most likely matching tuples we added couple of filters in both the websites before we could extract data. Filters like:

1. Selected movies under DVD streaming section and sorted the movies list by Tomatometer (RottenTomatoes).
2. Sorted the movies list from 1972-2016 (IMDB).

The link for the filtered result can be found below

### [IMDB](https://www.imdb.com/list/ls057823854/?sort=list_order,asc&st_dt=&mode=detail&page=1)
### [RottenTomatoes](https://www.rottentomatoes.com/browse/dvd-streaming-all?minTomato=0&maxTomato=100&services=amazon;hbo_go;itunes;netflix_iw;vudu;amazon_prime;fandango_now&genres=1;2;4;5;6;8;9;10;11;13;18;14&sortBy=tomato)


We have extracted around ****5000**** tuples from both the websites and below shows the schema of the extracted data.

| Attributes  |  Description |
|---|---|
|  Name | Name of the movie  |
|  year |  The year when the movie was released (Ex: 2005)  |
| Rating  |  Rating of the movie (like, R: Restricted, G: General Audiences, PG: Parental Guidance Suggested)  |
|  Genre |  The category of the movie (like: Drama, Comedy, Action, Horror, Romance etc) |
|  Directed By | Name(s) of director(s) who directed the movie   |
|  Runtime |  The duration of the movie |


#### We have 2 CSV files corresponding to data extracted from IMDB.com and rottentomatoes.com.
```
rottentomatoes_data.csv has 5397 tuples.
imdb_data.csv has 4886 tuples.
```

##### rottentomatoes_data.csv has the following attributes: <br />
**Name**: Name of the movie  <br />
**Year**: The year that the movie was released (Ex: 2005)   <br />
**Rating**: Rating of the movie (like, R: Restricted, G: General Audiences, PG: Parental Guidance Suggested)  <br />
**Genre**: The category of the movie (like: Drama, Comedy, Action, Horror, Romance etc)  <br />
**Directed By**: Name(s) of director(s) who directed the movie  <br /> 
**Runtime**: The duration of the movie. The format is in "Minutes" (Ex: 146 minutes)  <br />  <br /> 

##### imdb_data.csv has the following attributes:  <br />
**Name**: Name of the movie  <br />
**Year**: The year that the movie was released (Ex: 2005)   <br />
**Rating**: Rating of the movie (like, R: Restricted, G: General Audiences, PG: Parental Guidance Suggested)  <br />
**Genre**: The category of the movie (like: Drama, Comedy, Action, Horror, Romance etc)  <br />
**Directed By**: Name(s) of director(s) who directed the movie  <br />
**Runtime**: The duration of the movie. The format is in "xhymin" (Ex: 1h50min)   <br />

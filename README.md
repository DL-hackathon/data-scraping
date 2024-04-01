# Data scraping 
## Project description

We are going to collect, process, analyse and present data from [imdb.com](https://www.imdb.com/). 

Have you heard of [Six degrees of separation](https://en.wikipedia.org/wiki/Six_degrees_of_separation) theory? Have you heard of the game [Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon)? Well, our first goal in the project will be to implement a function, that will help us play this game.

The idea is simple. We introduce a special measure of distance between actors. How is it measured? If two actors played in the same movie, the distance between them is 1. If two actors never played in the same move, but there is some actor, who played in some movies with each of the actors, then the distance between the actors is 2. And so on. You can play around [here](https://oracleofbacon.org/help.php) to get a feel. Let's call it *movie distance*.

Firstly, we will be implementing a function, counting a distance between given actors. We will be using data from [IMDB](https://imdb.com) to obtain such an information. Then, we will try to visualize this data.



### Detailed description

This task is not so easy, so we will solve the problem step by step:
#### 1. Implement two auxiliary functions, that will be used for obtaining data

* to get a list of movies that a current actor played in
* to get a list of actors, that played in the current movie


`get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit)`

* This function takes a beautifulsoup soup object (`cast_page_soup`) of a page for the cast & crew for the current film.
* The function should return a list of all actors that played in the movie. An actor should be defined by such a pair: `(name_of_actor, url_to_actor_page)`. So, the output of the function is expected to be the list of such pairs.
* The function should be able to take an optional argument `num_of_actors`. This argument allows us to limit the output. If we set the argument equal to, say, 10, then the function should return first 10 actors listed on the cast page, and no more than that. If we set the argument equal to `None`, then the function should return all the actors. If there are fewer actors than the argument, the function should work and return all actors that are there.

`get_movies_by_actor_soup(actor_page_soup, num_of_movies_limit)`

* This functions takes a beautifulsoup soup object (`actor_page_soup`) of a page for the current actor.
* The function should return a list of all movies that the actor played in. A movie should be defined by such a pair: `(name_of_movie, url_to_movie_page)`. So, the output of the function is expected to be the list of such pairs.
* The function should be able to take an optional argument `num_of_movies_limit`. This argument allows us to limit the output. If we set the argument equal to, say, 10, then the function should return 10 latest movies that the actor played in, and no more than that. If we set the argument equal to None, then the function should return all the movies. If there are fewer movies than the argument, the function should work and return all movies that are there.
* The function should return only those movies, that have already been released.
* Sometimes actors could be producers, or even directors, or something else. The function should return only those movies, where the actor did an acting job. So, we should omit all the movies, where the actor has not actually played a role.
* The function should return only full feature movies. So, it should omit other types of videos, which are marked on imdb like that: TV Series, Short, Video Game, Video short, Video, TV Movie, TV Mini-Series, TV Series short and TV Special.

#### 2. Implement a function, that takes two actors as an input, and returns the *movie distance* between actors

#### Some pieces of advice:

* Don't forget about helper functions. A good way is to break bigger functions into smaller parts, and it is easier to test each part. Put your helper functions in `imdb_helper_functions.py`.
* You might want to add some additional arguments and functionality to your functions. For example, a simple logging could be done as an additional function argument, that (when set to `True`) will allow us to see, what is going on inside a function by printing intermediate variable values. Logging helps us a lot in testing functions.

#### 3. Obtain and Visualize a graph of *movie distance* between actors



### General summary for the review criteria.

You are required to submit three files

* `imdb_code.py`
* `imdb_helper_functions.py`
* `report.ipynb`

`imdb_code.py` should contain two functions implemented

* `get_actors_by_movie_soup`
* `get_movies_by_actor_soup`

`imdb_helper_functions.py` should contain all helper functions necessary for your code to work.

`report.ipynb` shoud contain the output for all function calls with the arguments below:
* for `get_movies_by_actor_soup`:
    * actor Dwayne Johnson https://www.imdb.com/name/nm0425005/
    * actor Dwayne Johnson https://www.imdb.com/name/nm0425005/, num_of_movies_limit=100
    * actor Dwayne Johnson https://www.imdb.com/name/nm0425005/, num_of_movies_limit=5
    * actress Scarlett Johansson https://www.imdb.com/name/nm0424060/
    * actress Scarlett Johansson https://www.imdb.com/name/nm0424060/, num_of_movies_limit=100
    * actress Scarlett Johansson https://www.imdb.com/name/nm0424060/, num_of_movies_limit=5
* for `get_actors_by_movie_soup`:
    * movie "Black Widow" https://www.imdb.com/title/tt3480822/fullcredits/
    * movie "Black Widow" https://www.imdb.com/title/tt3480822/fullcredits/, num_of_movies_limit=150
    * movie "Black Widow" https://www.imdb.com/title/tt3480822/fullcredits/, num_of_movies_limit=5 

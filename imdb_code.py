# define helper functions if needed
# and put them in `imdb_helper_functions` module.
# you can import them and use here like that:
from imdb_helper_functions import get_proper_url
from imdb_helper_functions import get_soup_txt
from imdb_helper_functions import get_soup
from imdb_helper_functions import get_proper_url
from imdb_helper_functions import read_json
from imdb_helper_functions import save_json
from imdb_helper_functions import get_graph_dict
# from imdb_helper_functions import collect_data
from imdb_helper_functions import check_local_file


import urllib
import re
import requests
from bs4 import BeautifulSoup
import time
from collections import defaultdict
import json
import matplotlib.pyplot as plt
# %matplotlib inline
from wordcloud import WordCloud, STOPWORDS
from tqdm import tqdm
from collections import defaultdict
import json
from itertools import permutations
from copy import deepcopy
from networkx import astar_path
import networkx as nx



def get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit=None):
    '''
    `get_actors_by_movie_soup(cast_page_soup, num_of_actors_limit)`

    * This function takes a beautifulsoup soup object (`cast_page_soup`)
    of a page for the cast & crew for the current film.
    * The function should return a list of all actors that played in the movie.
    * An actor should be defined by such a pair: `(name_of_actor, url_to_actor_page)`.
    So, the output of the function is expected to be the list of such pairs.
    * The function should be able to take an optional argument `num_of_actors`.
    This argument allows us to limit the output.

    '''
    cast_list = []

    url_of_soup_page = cast_page_soup.find('link')['href']
    url_of_soup_page = get_proper_url(url_of_soup_page)

    #     print(cast_page_soup)
    raw_cast_list = cast_page_soup.find('table', attrs={'class': 'cast_list'})
    #     print(raw_cast_list)
    actors = raw_cast_list.find_all('td', attrs={'class': None})
    if actors:
        for actor in actors:
            if actor:
                try:
                    actor_name = actor.find('a').text.strip()
                    actor_page = urllib.parse.urljoin(url_of_soup_page, actor.find('a')['href'])
                #         print(actor.find('a')['href'])
                    actor_page = actor_page.split('/?')[0]
                #         print(actor_page)
                    actor_page = get_proper_url(actor_page)
                    cast_list.append((actor_name, actor_page))
                except:
                    pass

    if not num_of_actors_limit:
        return cast_list
    else:
        return cast_list[:num_of_actors_limit]

def get_movies_by_actor_soup(actor_page_soup,
                             num_of_movies_limit=None):

    '''
    * This functions takes a beautifulsoup soup object (`actor_page_soup`)
    of a page for the current actor.
    * The function should return a list of all movies that the actor played in.
    A movie should be defined by such a pair: `(name_of_movie, url_to_movie_page)`.
    So, the output of the function is expected to be the list of such pairs.
    * The function should be able to take an optional argument `num_of_movies_limit`.
    This argument allows us to limit the output. If there are fewer movies than the argument,
    the function should work and return all movies that are there.
    * The function should return only those movies, that have already been released.
    * Sometimes actors could be producers, or even directors, or something else.
    The function should return only those movies, where the actor did an acting job.
    So, we should omit all the movies, where the actor has not actually played a role.
    * The function should return only full feature movies. So, it should omit other types
    of videos, which are marked on imdb like that: TV Series, Short, Video Game, Video short,
    Video, TV Movie, TV Mini-Series, TV Series short and TV Special.

    '''
    full_feature_movies = []

    url_of_soup_page = actor_page_soup.find('link')['href']

    movies = actor_page_soup.find_all("div", {"id": re.compile('actor-tt\d+|actress-tt\d+')})

    title_type = ['(TV Movie)', '(TV Series)',
                  '(TV Series short)',
                  '(TV Episode)', '(TV Special)',
                  '(TV Mini-Series)', '(Documentary)',
                  '(Video Game)', '(Short Film)',
                  '(Video)', '(TV Short)', '(Short)',
                  '(Podcast Series)', '(Podcast Episode)',
                  '(Music Video)', '(announced)', '(filming)',
                  '(pre-production)', '(TV Mini Series)',
                  '(post-production)', '(TV Mini Series short)',
                  '(completed)', '(Video short)', '(Music Video short)']

    for movie in movies:
        if not any(map(lambda x: x.lower() in movie.text.lower(),
                       title_type)):
            movie_name = movie.find('a').text
            movie_link = urllib.parse.urljoin(url_of_soup_page, movie.find('a')['href'])
            movie_link = movie_link.split('/?')[0]
            movie_link = get_proper_url(movie_link)
            full_feature_movies.append((movie_name, movie_link))

    if not num_of_movies_limit:
        return full_feature_movies
    else:
        return full_feature_movies[:num_of_movies_limit]


def get_movie_distance(actor_start_url: str,
                       actor_end_url: str,
                       num_of_actors_limit: int = None,
                       num_of_movies_limit: int = None):

    # trivial check
    if actor_start_url == actor_end_url:
        return 0

    # first check
    path_json_graph = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
                      f'W11_Project_Demo_02/data/json/graph.json'
    if check_local_file(path_json_graph):
        graph = read_json(path_json_graph)
        graph = nx.DiGraph(graph)
        try:
            distance = astar_path(graph, actor_start_url, actor_end_url)
            return len(distance) // 2
        except nx.exception.NodeNotFound:
            pass

    # prepare a dict to collect data about actors
    path_json_actors = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
                       f'W11_Project_Demo_02/data/json/actors_info.json'
    if not check_local_file(path_json_actors):
        actors_info = defaultdict(list)
    else:
        actors_info = read_json(path_json_actors)

    # prepare a dict to collect data about movies
    path_json_movies = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
                       f'W11_Project_Demo_02/data/json/movies_info.json'
    if not check_local_file(path_json_movies):
        movies_info = defaultdict(list)
    else:
        movies_info = read_json(path_json_movies)

    # first check
    if actors_info and movies_info:
        graph = get_graph_dict(actors_info, movies_info)
        save_json(path_json_graph, graph)
        graph = nx.DiGraph(graph)
        try:
            distance = astar_path(graph, actor_start_url, actor_end_url)
            return len(distance) // 2
        except nx.exception.NodeNotFound:
            pass

    actor_start_url = get_proper_url(actor_start_url)
    path_txt = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
               f'W11_Project_Demo_02/data/txt/{actor_start_url.split("/", maxsplit=5)[4]}.txt'
    if not check_local_file(path_txt):
        send_request(actor_start_url, path_txt)
    actor_soup = get_soup_txt(path_txt)
    movies = get_movies_by_actor_soup(actor_soup, num_of_movies_limit=num_of_movies_limit)
    movies = [movie for _, movie in movies]
    # save data about actors into actors_info dict
    if actor_start_url not in actors_info.keys():
        actors_info[actor_start_url] = movies
    layer = 0
    while layer < 5:
        # actors_info, movies_info = collect_data(actors_info,
        #                                         movies_info,
        #                                         path_json_actors,
        #                                         path_json_movies,
        #                                         num_of_actors_limit,
        #                                         num_of_movies_limit)
    # data collection start
        actor_info_copy = deepcopy(actors_info)
        for actor_1 in actor_info_copy.keys():
            movies_1 = actor_info_copy[actor_1]
            for movie_1 in movies_1:
                path_txt = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
                           f'W11_Project_Demo_02/data/txt/{movie_1.split("/", maxsplit=5)[4]}.txt'
                if not check_local_file(path_txt):
                    send_request(movie_1, path_txt)
                movie_soup = get_soup_txt(path_txt)
                actors = get_actors_by_movie_soup(movie_soup,
                                                  num_of_actors_limit=num_of_actors_limit)
                actors = [actor for _, actor in actors]
                # save data about movies
                if movie_1 not in movies_info.keys():
                    movies_info[movie_1] = actors
                for actor_2 in actors:
                    path_txt = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
                               f'W11_Project_Demo_02/data/txt/{actor_2.split("/", maxsplit=5)[4]}.txt'
                    if not check_local_file(path_txt):
                        send_request(actor_2, path_txt)
                    actor_soup = get_soup_txt(path_txt)
                    movies_2 = get_movies_by_actor_soup(actor_soup,
                                                        num_of_movies_limit=num_of_movies_limit)
                    movies_2 = [movie for _, movie in movies_2]
                    if actor_2 not in actors_info.keys():
                        actors_info[actor_2] = movies_2

            save_json(path_json_actors, actors_info)
            save_json(path_json_movies, movies_info)
    # data collection end

            if actors_info and movies_info:
                graph = get_graph_dict(actors_info, movies_info)
                save_json(path_json_graph, graph)
                graph = nx.DiGraph(graph)
                try:
                    distance = astar_path(graph, actor_start_url, actor_end_url)
                    return len(distance) // 2
                except nx.exception.NodeNotFound:
                    pass
        layer += 1
    # if no connection in the third layer
    distance = None
    return distance


def get_movie_descriptions_by_actor_soup(actor_page_soup):
    '''
    This function collect descriptions of actor's movies
    '''
    movies = get_movies_by_actor_soup(actor_page_soup)
    links = (movie for _, movie in movies)
    actor_name = actor_page_soup.\
                       title.text.split(' - ')[0]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'en',
               'X-FORWARDED-FOR': '2.22.181.0'}
    descriptions = [f'{actor_name}']
    for link in links:
        link = get_proper_url(link, suffix=False)
        response = requests.get(link, headers=headers)
        assert response.status_code == 200,\
                   f'Something went wrong. Actual response.status_code is {response.status_code}'
        soup = BeautifulSoup(response.text, features="lxml")
        description = soup.find('span', attrs={'data-testid': 'plot-xs_to_m'}).text
        descriptions.append(description)
    return descriptions


# url = 'https://www.imdb.com/name/nm0425005/'
# url = get_proper_url(url)
# actor_page_soup = get_soup(url)
# print(actor_page_soup)
# print(get_movie_descriptions_by_actor_soup(actor_page_soup))
# print(len(get_movies_by_actor_soup(actor_page_soup)))

# print(get_movie_distance('https://www.imdb.com/name/nm0425005/fullcredits/',
#                    'https://www.imdb.com/name/nm1165110/fullcredits/',
#                    num_of_actors_limit=6,
#                    num_of_movies_limit=6))

# r = get_movie_distance('https://www.imdb.com/name/nm0425005/fullcredits/',
#                        'https://www.imdb.com/name/nm0425005/fullcredits/',
#                        num_of_actors_limit=6,
#                        num_of_movies_limit=6)
# print('distance = ', r)
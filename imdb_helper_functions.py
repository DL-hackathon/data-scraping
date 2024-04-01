# from imdb_code import get_actors_by_movie_soup
# from imdb_code import get_movies_by_actor_soup


import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os
import re
import time
from collections import defaultdict
import json
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


def helper_function_example():
    return 'Hello, I am supposed to be a helper function'


def get_soup(url):
    '''
        This function send request to url
        Returns Beautiful soup object
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'en',
               'X-FORWARDED-FOR': '2.22.181.0'}
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, f'Something went wrong. Your soup is not ready to use.'
    soup = BeautifulSoup(response.text, features='lxml')
    return soup

def get_soup_txt(path:str):
    '''
            path : str - local html-file
            This function cook soup from local file (path)
            Returns Beautiful soup object
    '''
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    f.close()
    soup = BeautifulSoup(text, features="lxml")
    return soup

# get_soup_txt('a')

def check_local_file(path: str):
    '''
    This function checks local availability of the txt-file for the url provided

    '''
    if os.path.exists(path):
        return True
    return False

def get_proper_url(url: str, suffix=True):
    '''
    This function corrects url if needed
    '''
    suff = 'fullcredits/'
    if 'www' not in url:
        url = url.replace('imdb', 'www.imdb')

    if url[-1] != '/':
        url = url + '/'

    if suffix:
        if suff not in url:
            url = url + suff

    if not suffix:
        if suff in url:
            url = url.replace(suff, '')
    return url

def read_json(path: str):
    '''
    Reads json from local path
    '''
    with open(path, 'r', encoding="utf-8") as f1:
        file = json.load(f1)
        f1.close()
    return file

def save_json(path: str, file):
    '''
        Saves json from local path
    '''
    with open(path, 'w', encoding="utf-8") as f:
        json.dump(file, f)
        f.close()


# def collect_data(actors_info: dict,
#                  movies_info: dict,
#                  path_json_actors: str,
#                  path_json_movies: str,
#                  num_of_actors_limit: int = None,
#                  num_of_movies_limit: int = None):
#
#     actor_info_copy = deepcopy(actors_info)
#     for actor_1 in actor_info_copy.keys():
#         movies_1 = actor_info_copy[actor_1]
#         for movie_1 in movies_1:
#             path_txt = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
#                        f'W11_Project_Demo_02/data/txt/{movie_1.split("/", maxsplit=5)[4]}.txt'
#             if not check_local_file(path_txt):
#                 send_request(movie_1, path_txt)
#             movie_soup = get_soup_txt(path_txt)
#             actors = get_actors_by_movie_soup(movie_soup,
#                                               num_of_actors_limit=num_of_actors_limit)
#             actors = [actor for _, actor in actors]
#             # save data about movies
#             if movie_1 not in movie_info.keys():
#                 movies_info[movie_1] = actors
#             for actor_2 in actors:
#                 path_txt = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/' + \
#                            f'W11_Project_Demo_02/data/txt/{actor_2.split("/", maxsplit=5)[4]}.txt'
#                 if not check_local_file(path_txt):
#                     send_request(actor_2, path_txt)
#                 actor_soup = get_soup_txt(path_txt)
#                 movies_2 = get_movies_by_actor_soup(actor_soup,
#                                                     num_of_movies_limit=num_of_movies_limit)
#                 movies_2 = [movie for _, movie in movies_2]
#                 if actor_2 not in actor_info.keys():
#                     actor_info[actor_2] = movies_2
#
#         save_json(path_json_actors, actors_info)
#         save_json(path_json_movies, movies_info)
#
#     return actors_info, movies_info

def get_graph_dict(actors_info: dict, movies_info: dict):
    graph = deepcopy(actors_info)
    for i in movies_info:
        graph[i] = movies_info[i]
    return graph


def send_request(url: str, path: str):
    '''
    This function writes an html-page as a txt-file on a hard drive
    '''

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
               'Accept-Language': 'en',
               'X-FORWARDED-FOR': '2.23.180.0'}

    response = requests.get(url, headers=headers)
    time.sleep(5)
    assert response.status_code == 200, \
        f'Something went wrong. Actual response.status_code is {response.status_code}'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(response.text)
    f.close()


def write_to_csv(path: str,
                 actor_start_name: str,
                 actor_start_url: str,
                 actor_end_name: str,
                 actor_end_url: str,
                 distance: int):
    if not check_local_file(path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"actor_start_name;actor_start_url;actor_end_name;actor_end_url;distance\n")
        f.close()
    with open(path, 'a', encoding='utf-8') as f:
        f.write(f"{actor_start_name};{actor_start_url};{actor_end_name};{actor_end_url};{distance}\n")
    f.close()

def save_descriptions(descriptions: list):
    '''
    This function saves descriptions into a {actor_name}.txt file
    '''

    path = f"C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/W11_Project_Demo_02/data/descr/{descriptions[0]}.txt"
    if not os.path.exists(path):
        with open(path, 'a', encoding='utf-8') as f:
            for description in descriptions[1:]:
                f.write(description + '\n')
        f.close()

# path = 'C:/Users/DL/PycharmProjects/3rd_sem/Data_Scraping/W11_Project_Demo_02/data/descr/'

def print_wordclouds(path:str):
    '''
    This function print wordclouds for the descriptions located in the path
    :param path: string with a path to descriptions
    :return: None
    '''

    i = 0
    for file in list(os.walk(path))[0][2]:
        with open(path + file, 'r', encoding='utf-8') as f:
            description = f.read()
        f.close()
        i += 1
        wordCloud = WordCloud(width=1000, height=1000,
                              random_state=1, background_color='black',
                              colormap='Set2', collocations=False, stopwords=STOPWORDS.add('Read')).generate(description)
        plt.figure(figsize=(5,5))
        plt.title(f"{i}. {file.split('.')[0]}'s wordcloud")
        plt.imshow(wordCloud)
        plt.axis("off")
        plt.show()

# print_wordclouds(path)


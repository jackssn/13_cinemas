import requests
from bs4 import BeautifulSoup
import time
import argparse
import re


TIMEOUT = 11  # seconds
SHOWS_LIMIT = 200


def check_positive(value):
    ivalue = int(value)
    if ivalue <= 0:
         raise argparse.ArgumentTypeError("{} is an invalid positive int value".format(value))
    return ivalue


def get_film_list_from_afisha_page():
    response = requests.get('http://www.afisha.ru/msk/schedule_cinema/')
    films_soup = BeautifulSoup(response.text, 'html5lib')
    films_list = films_soup.find_all("div", {"class": "m-disp-table"})
    return [x.a.text.strip() for x in films_list]


def fetch_movie_info(movie_title):
    payload = {'first': 'yes', 'kp_query': movie_title}
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'UTF-8',
        'Accept-Language': 'en-US,en;q=0.8,ru;q=0.6',
        'Content-Type': 'text/html;charset=UTF-8',
        'User-Agent': 'Agent:Mozilla/5.0 (Windows NT 6.1; WOW64))'
    }
    response = requests.get('https://www.kinopoisk.ru/index.php', headers=headers, params=payload)
    if response.status_code != 200:
        return None
    film_soup = BeautifulSoup(response.text, 'html5lib')
    movie_info = {'title': movie_title}
    try:
        movie_info['rating'] = float(film_soup.find("span", {"class": "rating_ball"}).text)
    except AttributeError:
        movie_info['rating'] = 0
    try:
        shows_str = film_soup.find("div", {"class": "shows"}).a.text
        movie_info['shows'] = re.sub("[^0-9]", "", shows_str)
    except AttributeError:
        movie_info['shows'] = 0
    return movie_info


def output_movies_to_console(movies, quantity):
    for number, movie in enumerate(sort_movie_list_by_rating(movies), start=1,):
        print('{} "{}" has rating {} and {} shows'.format(number, movie['title'], movie['rating'], movie['shows']))
        if number == quantity:
            break


def sort_movie_list_by_rating(movies):
    sorted_by_rating_movie_list = sorted(movies, key=lambda k: k['rating'], reverse=True)
    return [x for x in sorted_by_rating_movie_list if int(x['shows']) > SHOWS_LIMIT]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Movies quantity')
    parser.add_argument('movies_quantity', type=check_positive, help='How many movies to show')
    args = parser.parse_args()

    movies_quantity = args.movies_quantity
    movies_info = []
    movies_titles_list = get_film_list_from_afisha_page()
    for number, movie_title in enumerate(movies_titles_list, start=1):
        if number == 5:
            break
        current_movie_dict = fetch_movie_info(movie_title)
        if current_movie_dict is None:
            print("Error parsing {}/{} movie".format(number, len(movies_titles_list)))
        else:
            movies_info.append(current_movie_dict)
            print("{}/{} movie parsed".format(number, len(movies_titles_list)))
        time.sleep(TIMEOUT)
    output_movies_to_console(movies_info, movies_quantity)

import requests
from bs4 import BeautifulSoup
import time


TIMEOUT = 11  # seconds


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
    r = requests.get('https://www.kinopoisk.ru/index.php', headers=headers, params=payload)
    if r.status_code != 200:
        return {}
    film_soup = BeautifulSoup(r.text, 'html5lib')
    movie_info = {}
    movie_info['title'] = movie_title
    try:
        movie_info['rating'] = float(film_soup.find("span", {"class": "rating_ball"}).text)
    except AttributeError:
        movie_info['rating'] = 0
    try:
        movie_info['shows'] = film_soup.find("div", {"class": "shows"}).a.text
    except AttributeError:
        movie_info['shows'] = 0
    return movie_info


def output_movies_to_console(movies, quantity):
    sorted_by_rating_movie_list = sorted(movies, key=lambda k: k['rating'], reverse=True)
    sorted_by_rating_movie_list_without_zero_shows = [x for x in sorted_by_rating_movie_list if x['shows'] != 0]
    for number, movie in enumerate(sorted_by_rating_movie_list_without_zero_shows, start=1,):
        print('%s) "%s" has rating %s and %s' % (number, movie['title'], movie['rating'], movie['shows']))
        if number == quantity:
            break


if __name__ == '__main__':
    movies_quantity = 10
    movies_info = []
    movies_titles_list = get_film_list_from_afisha_page()
    for number, movie_title in enumerate(movies_titles_list, start=1):
        current_movie_dict = fetch_movie_info(movie_title)
        if current_movie_dict:
            movies_info.append(current_movie_dict)
            print("%d/%d movie parsed" % (number, len(movies_titles_list)))
        else:
            print("Error parsing %d/%d movie" % (number, len(movies_titles_list)))
        time.sleep(TIMEOUT)
    output_movies_to_console(movies_info, movies_quantity)

import requests
from bs4 import BeautifulSoup
import time


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
    film_soup = BeautifulSoup(r.text, 'html5lib')
    movie_info = {}
    movie_info['title'] = movie_title
    movie_info['rating'] = float(film_soup.find("span", {"class": "rating_ball"}).text)
    movie_info['shows'] = film_soup.find("div", {"class": "shows"}).a.text
    return movie_info


def output_movies_to_console(movies):
    for movie in sorted(movies, key=movies.__getitem__):
        print(movie)
    pass


if __name__ == '__main__':
    movies_info = []
    N = 5  # test. connection error
    movies_titles_list = get_film_list_from_afisha_page()
    for number_movie in range(N):
        movie_title = movies_titles_list[number_movie]
        movies_info.append(fetch_movie_info(movie_title))
        time.sleep(11)
        print(movie_title, 'added to output list')
    output_movies_to_console(movies_info)

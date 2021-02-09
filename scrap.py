"""
web scraping tool for list of movies from IMDB based on rating

"""
import csv
import re
import requests
from bs4 import BeautifulSoup


# https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&start=1&ref_=adv_nxt

# makes a request based on GET pagination.
def imdbdataExtract():
    request_url = "https://www.imdb.com/search/title/"
    data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) '
                      'AppleWebKit/537.36 ( '
                      'KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36'}
    for i in range(1, 1000, 50):
        requestParams = {
            "groups": "top_1000",
            "sort": "user_rating,desc",
            "start": i,
            "ref_": "adv_nxt"
        }

        responsePerPage = requests.get(request_url, params=requestParams,
                                       headers=headers)
        soup = BeautifulSoup(responsePerPage.content, 'html.parser')

        containers = soup.find("div", attrs={'class': 'lister-list'})
        for container in containers.findAll('div',
                                            attrs={'class': 'lister-item'
                                                            '-content'}):
            try:
                # Movie name and the year released
                movieAndYear = container.h3.findAll('span')
                movieGenre = \
                    container.findAll('p', attrs={'class': 'text-muted'})[
                        0].findAll('span')

                cast = container.findAll('p', attrs={'class': ''})[0].findAll(
                    'a')
                # extracts data
                info = {
                    'id': re.sub("[^0-9]", "", movieAndYear[0].text),
                    'movie_name': container.h3.a.text + ' ' + movieAndYear[
                        1].text,
                    'genre': movieGenre[len(movieGenre) - 1].text.replace('\n','').strip(),
                    'director': cast[0].text,
                    # adding multiple actors for movie
                    'actors': ','.join(
                        [cast[actor].text for actor in range(2, len(cast))])
                }
                data.append(info)
            except Exception as e:
                print(e)
    return data


# saves data to file within current dir.
def saveToFile(data):
    keys = data[0].keys()
    with open('movies.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def main():
    saveToFile(imdbdataExtract())


if __name__ == "__main__":
    main()

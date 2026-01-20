import requests
from bs4 import BeautifulSoup

url = "https://www.imdb.com/fr/chart/top"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml"
}


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

next_link = soup.find("", class_="next")
if next_link:
    url_suivante = next_link.a["href"]

films = soup.find_all("h3", class_='ipc-title__text')
print(len(films))

for film in films:
    print(film.text.strip())
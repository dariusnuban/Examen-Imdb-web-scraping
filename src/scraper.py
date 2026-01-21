import requests
from bs4 import BeautifulSoup
import json
import time
from database import DatabaseManager  # Import de votre classe

BASE_URL = "https://www.senscritique.com"
LIST_URL = "https://www.senscritique.com/liste/les_250_films_a_voir_imdb_top_250/251213"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
}

def parse_duration(dur):
    if not dur: return None
    return dur.replace("PT", "").replace("H", "h ").replace("M", "min")

# Initialisation de la base de données
db = DatabaseManager("base_de_données.db")

for page in range(1, 7):
    print(f"Scraping page {page}...")
    url = LIST_URL if page == 1 else f"{LIST_URL}?page={page}"
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        continue
        
    soup = BeautifulSoup(response.text, "html.parser")

    # Recherche des liens vers les fiches films
    film_links = soup.find_all("a", class_="sc-f84047c3-0 sc-d9336e28-1 bZInWI gfTNTa sc-d947697b-1 deogiZ sc-b5c2c6dc-3 dikXUs")

    for f in film_links:
        try:
            link = BASE_URL + f["href"]
            soup_film = BeautifulSoup(requests.get(link, headers=headers).text, "html.parser")

            # Extraction via le JSON LD caché dans la page
            json_tag = soup_film.find("script", type="application/ld+json")
            if not json_tag: continue
            
            data = json.loads(json_tag.text)

            # Nettoyage et formatage
            title = data.get("name")
            year = int(data.get("datePublished", "0000")[:4])
            genre = ", ".join(data["genre"]) if isinstance(data.get("genre"), list) else data.get("genre")
            duration = parse_duration(data.get("duration"))

            director_data = data.get("director", [])
            if isinstance(director_data, dict):
                director = director_data.get("name")
            else:
                director = ", ".join([d.get("name", "") for d in director_data])

            rating_data = data.get("aggregateRating", {})
            imdb_rating = float(rating_data.get("ratingValue", 0))
            rating_count = int(rating_data.get("ratingCount", 0))

            # ENVOI À LA BASE DE DONNÉES
            db.insert_film(title, year, genre, duration, director, imdb_rating, rating_count, link)
            
            print(f"Ajouté : {title}")
            time.sleep(0.1) # Respect du serveur

        except Exception as e:
            print(f"Erreur sur un film : {e}")
            continue

# Fermeture propre
db.close()
print("Scraping terminé et base de données enregistrée.")
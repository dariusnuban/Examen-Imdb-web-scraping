import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

s = requests.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'})
start_page = 'https://www.imdb.com/chart/top'
start_page_text = s.get(start_page).text

link_list = []

template = 'https://www.imdb.com%s'

soup = BeautifulSoup(start_page_text, "html.parser")

for col in soup.find_all('td', {'class':'titleColumn'}):
    link_list.append(template % re.findall("/title/tt[0-9]+", col.find('a').get('href'))[0])


movies = pd.DataFrame(link_list, index=range(1, 251), columns=['IMDB link'])

movies.insert(column='Title', loc=0, value=["" for i in range(1,251)])
movies.insert(column='Year', loc=1, value=["" for i in range(1,251)])
movies.insert(column='Genre', loc=2, value=["" for i in range(1,251)])
movies.insert(column='Duration', loc=3, value=["" for i in range(1,251)])
movies.insert(column='Origin', loc=4, value=["" for i in range(1,251)])
movies.insert(column='Director', loc=5, value=["" for i in range(1,251)])
movies.insert(column='IMDB rating', loc=6, value=["" for i in range(1,251)])
movies.insert(column='Rating count', loc=7, value=["" for i in range(1,251)])


for n in range(1, 251):
    page_text = s.get(link_list[n - 1]).text
    soup = BeautifulSoup(page_text)
    
    # Searching for attributes with one valid value
    
    ## It's important to use try/except because English version of the page won't contain the div with class 'originalTitle'
    try:
        movies.at[n, 'Title'] = soup.find('div', {'class':'originalTitle'}).contents[0].strip()
    except AttributeError:
        movies.at[n, 'Title'] = (soup.find('div', {'class':'title_wrapper'}).contents[1]).find(text = re.compile('[a-zA-Z0-9]*'))
    
    movies.at[n, 'Year'] = (soup.find('span', {'id':'titleYear'}).contents[1].get_text().strip())
    movies.at[n, 'Duration'] = soup.find('time', {'datetime':re.compile('[a-zA-Z0-9]*')}).get_text().strip()
    movies.at[n, 'Director'] = soup.find('a', {'href':re.compile('.*/name/nm[0-9]+/\?ref_=tt_ov_dr.*')}).get_text().strip()
    movies.at[n, 'IMDB rating'] = soup.find('span', {'itemprop':'ratingValue'}).get_text().strip()
    movies.at[n, 'Rating count'] = int(soup.find('span', {'itemprop':'ratingCount'}).get_text().strip().replace(',', ''))
    
    # Searching for attributes with multiple (possible) valid values
    genres = soup.find_all('a', {'href':re.compile('.*/search/title\?genres=[a-z]*\&explore=title_type,genres\&ref_=tt_ov_inf.*')})
    movies.at[n, 'Genre'] = ' | '.join(set([x.get_text().strip() for x in genres]))
    
    countries = soup.find_all('a', {'href':re.compile('/search/title\?country_of_origin=[a-z]*&ref_=tt_dt_dt')})
    movies.at[n, 'Origin'] = ' | '.join(set([x.get_text().strip() for x in countries]))


movies

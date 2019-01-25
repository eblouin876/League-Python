from bs4 import BeautifulSoup
import urllib3
from Character import *
name = "kog'maw"
ahri = Character(name.title(), "Link")


def make_soup(link):
    http = urllib3.PoolManager()

    # Here we go to the webpage that has a list of all of the champions
    response = http.request('GET', link)
    page = response.data

    # Now we make soup out of it in order to read the html
    soup = BeautifulSoup(page, 'html.parser')

    # and return the soup
    return soup

stats = {}
sorted_stats = []
unsorted_stats = []
soup = make_soup('http://leagueoflegends.wikia.com/wiki/'+ahri.name)
table = soup.select("#champion_info-season7 > tr")
raw_stats = table[1].select("tr")

for row in raw_stats:
    values = row.select("td")
    try:
        h = values[1].select("span")
        a = values[0].select("span > a")
        stats[a[0].text] = h[0].text + h[1].text
    except IndexError as e:
        print(e)
        pass

    try:
        d = values[3].select("span")
        b = values[2].select("span > a")
        stats[b[0].text] = d[0].text + d[1].text
    except IndexError as e:
        print(e)
        pass

print(stats)

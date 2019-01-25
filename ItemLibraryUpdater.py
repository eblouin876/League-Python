from bs4 import BeautifulSoup
import urllib3
import certifi
import Item


class ItemLibraryUpdater(object):

    def __init__(self):
        self.items = {}
        self.update_item_name_number()

    def make_soup(self, link):
        http = urllib3.PoolManager()

        # Here we go to the webpage that has a list of all of the champions
        response = http.request('GET', link)
        page = response.data

        # Now we make soup out of it in order to read the html
        soup = BeautifulSoup(page, 'html.parser')

        # and return the soup
        return soup

    def update_item_name_number(self):
        item_update = {}

        soup = self.make_soup('http://leagueoflegends.wikia.com/wiki/Item')

        item_table = soup.select('.va-collapsible-content.mw-collapsible-content > div')
        raw_table = item_table[0].select('.centered-grid > div')

        print(raw_table)
        for item in raw_table:
            pass
items = ItemLibraryUpdater()
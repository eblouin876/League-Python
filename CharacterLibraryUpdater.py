from bs4 import BeautifulSoup
import urllib3
from Character import *


class CharacterLibraryUpdater(object):

    def __init__(self):
        self.characters = {}
        self.update_character_name_link()
        self.update_position_frequency()
        self.update_character_skills()
        self.update_character_matchups()
        self.update_runes()
        self.update_stats()
        print("Library Complete")

    def make_soup(self, link):
        http = urllib3.PoolManager()

        # Here we go to the webpage that has a list of all of the champions
        response = http.request('GET', link)
        page = response.data

        # Now we make soup out of it in order to read the html
        soup = BeautifulSoup(page, 'html.parser')

        # and return the soup
        return soup

    def update_character_name_link(self):
        # This gives an empty space for the new characters!
        update = {}

        soup = self.make_soup('http://na.op.gg/champion/statistics')

        # This brings up all of the information on all of the characters
        raw_characters = soup.select('.champion-index__champion-list > div')

        # Now we take the raw data and pull the positions, link in op.gg and name of each character
        for each in raw_characters:
            name = each.select('.champion-index__champion-item__name')
            link = each.select('a')

            # This is here because there are characters that are removed after the new update and don't have a link
            # but they still appear on the main website, so they have to be dealt with
            try:
                if isinstance(link[0]['href'], str):
                    update[name[0].text.lower()] = Character(name[0].text.lower(), 'http://na.op.gg' + link[0]['href'])
            except IndexError:
                print(name[0].text + " has no link. They must be deceased.")
                pass
        self.characters = update
        print('Names updated')

    def update_character_skills(self):
        # This happens for each character that exists. It will also have to happen for each position they might play
        for key, character in self.characters.items():
            # Make a placeholder for the skill build
            skill_update = {}
            for position in character.position:
                skill = []
                stew = self.make_soup(character.op_gg_link)

                # Doing this once on the page makes sure it goes to the correct one. This will also be used for matchups
                soup = self.make_soup(character.op_gg_link + "/" + position.lower())
                builds_table = soup.select('.champion-skill-build__table')
                try:
                    raw_build = builds_table[0].select('td')
                    for each in raw_build:
                        text = each.text.lower()
                        skill.append(text.strip())

                # One of the character sites (Fizz) was broken so put this in here to bypass it. What will it do to data
                except IndexError:
                    pass

                # Add that position to the skill update
                skill_update[position] = skill
            # Add the full update to the character
            character.skill_build = skill_update
        print("Skills updated")

    def update_character_matchups(self):
        for key, character in self.characters.items():
            match_update = {}
            stew = self.make_soup(character.op_gg_link)
            for position in character.position:
                match = {}
                # Doing this once on the page makes sure it goes to the correct one. This will also be used for matchups
                soup = self.make_soup(character.op_gg_link + "/" + position.lower())

                # Get link to matchup
                raw_link = soup.select('.champion-stats-menu__list__item.champion-stats-menu__list__item--red.tabHeader > a')
                link = 'http://na.op.gg' + raw_link[0]['href']

                # New soup with Link
                new_soup = self.make_soup(link)

                raw_table = new_soup.select('.champion-matchup-champion-list')
                match_table = raw_table[0].select('.champion-matchup-list__champion')

                for each in match_table:
                    # Get name and winrate
                    info = each.select('span')
                    name = info[0].text.lower()
                    win_rate = info[1].text.lower()
                    match[name.strip()] = win_rate.strip()

                # Save for this position
                match_update[position] = match

            character.matchup = match_update
        print("Matchups updated")

    def update_position_frequency(self):
        for key, character in self.characters.items():
            positions_update = {}
            soup = self.make_soup(character.op_gg_link)

            # Get positions boxes
            raw_positions = soup.select('.champion-stats-position')

            # Get frequency
            raw_frequency = raw_positions[0].select('a')

            for frequency in raw_frequency:
                position = frequency.select('span')
                pos = position[0].text.lower()
                if position[0].text.lower() == "bottom":
                    pos = 'bot'
                if position[0].text.lower() == 'middle':
                    pos = 'mid'
                positions_update[pos] = position[1].text

            character.position = positions_update
        print("Positions updated")

    def update_runes(self):
        for key, character in self.characters.items():
            runes_update = {}
            stew = self.make_soup(character.op_gg_link)
            for position in character.position:
                runes = []
                # Doing this once on the page makes sure it goes to the correct one.
                soup = self.make_soup(character.op_gg_link + "/" + position.lower())

                # Get link to runes
                raw_link = soup.select('a[href$="rune"]')
                link = 'http://na.op.gg' + raw_link[0]['href']

                # New soup with Link
                new_soup = self.make_soup(link)

                # Get to the raw table
                raw_table = new_soup.select(".champion-stats-summary.champion-stats-summary--rune > div")

                # Get the runes
                raw_runes = raw_table[0].select(".perk-page__item.perk-page__item--active")
                for rune in raw_runes:
                    r = rune.select("div")
                    raw_rune = r[0].select('img')
                    new_rune = raw_rune[0]['alt']
                    runes.append(new_rune)

                runes_update[position] = runes
            character.runes = runes_update
        print('Runes Updated')

    # Not working for Jarvan IV because IV has to be capitalized -_-
    def update_stats(self):
        for key, character in self.characters.items():
            stats = {}
            names = key.split(' ')
            name = names[0].title()
            for i in range(1, len(names)):
                name += '_' + names[i].title()
            soup = self.make_soup('http://leagueoflegends.wikia.com/wiki/' + name)
            table = soup.select("#champion_info-season7 > tr")
            try:
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
            except IndexError as e:
                print(e)
                print(key.title() + " Could not be found")


            character.stats = stats
        for key, character in self.characters.items():
            print(key + " " + str(character.stats))
        print("Stats update")

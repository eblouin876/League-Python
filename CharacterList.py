from Character import *
import mysql.connector
import ast


class CharacterList(object):

    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="league_database"
        )

        self.mycursor = self.mydb.cursor()

        self.characters = {}

        self.update_characters()

    def update_characters(self):
        update = {}
        sql = "SELECT * FROM characters"
        self.mycursor.execute(sql)
        raw_data = self.mycursor.fetchall()
        for each in raw_data:
            update[each[1]] = Character(each[1], each[2], ast.literal_eval(each[3]), ast.literal_eval(each[4]),
                                        ast.literal_eval(each[5]), ast.literal_eval(each[6]), ast.literal_eval(each[7]))
        self.characters = update

    def best_against(self, character):
        best_matches = []
        best_match = ''
        best_win = 0
        matchups = self.characters[character].matchup
        for position, matchup in matchups.items():
            match = matchup
            for key, value in match.items():
                win = float(value.rstrip('%'))
                if win > best_win:
                    best_match = key
                    best_win = float(value.rstrip('%'))
                else:
                    pass
            best_matches.append(character.capitalize() + " is best against " + best_match.capitalize() + " in " +
                                position + " and wins " + str(best_win) + "% of the time")
        for each in best_matches:
            print(each)

    def worst_against(self, character):
        worst_matches = {}
        for position, matchup in self.characters[character].matchup.items():
            worst_match = ''
            lowest = 100
            for key, value in matchup.items():
                win = float(value.rstrip('%'))
                if win < lowest:
                    worst_match = key
                    lowest = float(value.rstrip('%'))
                else:
                    pass
            worst_matches[position] = [worst_match, 100-lowest]
        return worst_matches

    def choose_character_to_play(self, opponent):
        play_characters = {}
        characters = self.worst_against(opponent)
        for position, character in characters.items():
            print("For " + str(character[1]) + "% win rate against " + opponent.capitalize() + " on " + position + " ("
                  + self.characters[opponent].position[position] + " chance for this position) play ")
            self.print_skills_runes(character[0], position)
            play_characters[position] = character[0]
        return play_characters

    def print_skills_runes(self, character, position):
        build = self.characters[character].skill_build[position]
        runes = self.characters[character].runes[position]
        stats = self.characters[character].stats
        print(character.capitalize() + "\nStats:" + str(stats) + "\nSkill Build: " + str(build) + "\nWith Runes: " + str(runes))
        return build


test = CharacterList()

test.choose_character_to_play('aatrox')

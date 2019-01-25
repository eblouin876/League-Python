import mysql.connector
import mysql.connector.errors as error
from CharacterLibraryUpdater import *


class LeagueDatabase(object):

    def __init__(self):
        mydb = mysql.connector.connect(
          host="localhost",
          user="root",
          passwd="root",
        )

        mycursor = mydb.cursor()

        try:
            mycursor.execute("CREATE DATABASE league_database")
        except error.DatabaseError:
            print("League database already exists")
            pass

        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database='league_database'
        )

        self.mycursor = self.mydb.cursor()
        self.update_database()

    def update_database(self):
        character_library = CharacterLibraryUpdater()

        try:
            self.mycursor.execute("CREATE TABLE characters (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), link "
                                  "VARCHAR(255), position VARCHAR(255), skills LONGTEXT, matchup LONGTEXT, runes "
                                  "LONGTEXT, stats LONGTEXT)")
        except error.ProgrammingError as e:
            print(e)
            self.mycursor.execute("DROP TABLE characters")
            self.mycursor.execute("CREATE TABLE characters (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), link "
                                  "VARCHAR(255), position VARCHAR(255), skills LONGTEXT, matchup LONGTEXT, runes "
                                  "LONGTEXT, stats LONGTEXT)")

        for key, value in character_library.characters.items():

            try:
                sql = ("INSERT INTO characters" "(name, link, position, skills, matchup, runes, stats)" "VALUES (%s, %s, %s, "
                       "%s, %s, %s, %s)")
                val = (str(value.name), str(value.op_gg_link), str(value.position), str(value.skill_build),
                       str(value.matchup), str(value.runes), str(value.stats))
                self.mycursor.execute(sql, val)

                self.mydb.commit()

            except error.DatabaseError as e:
                print(e)
                print('Could not add ' + key + ' to database')
        print('Database updated')


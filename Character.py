class Character(object):

    def __init__(self, name, link, position={}, skills={}, match={}, runes={}, stats={}):
        self.name = name
        self.op_gg_link = link
        self.skill_build = skills
        self.position = position
        self.matchup = match
        self.runes = runes
        self.stats = stats

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def print(self):
        print(self.name)
        print(self.op_gg_link)
        print(self.skill_build)
        print(self.position)
        print(self.matchup)
        print(self.runes)
        print(self.stats)

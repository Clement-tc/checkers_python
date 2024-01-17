class Player:
    def __init__(self,name):
        self.name=name
        self.score=0
    def gainpoint(self):
        self.score+=1
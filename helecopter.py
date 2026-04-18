import os

from utils import randcell

class helecopter:
    def __init__(self, w, h):
        rc = randcell(w,h)
        rx,ry = rc[0],rc[1]
        self.h,self.w = h,w
        self.x, self.y = rx,ry
        self.mxtank, self.tank = 1,0
        self.score = 0
        self.lives = 20

    def move(self,dx,dy):
        nx,ny = dx + self.x, dy + self.y
        if nx >= 0 and ny >= 0 and nx < self.h and ny < self.w:
            self.x, self.y = nx,ny
    
    def print_stats(self):
        print("🧺 ",self.tank,"/",self.mxtank, sep='', end='|')
        print("🏆 ",self.score, sep='', end='|')
        print("💓 ",self.lives, sep='')

    def game_over(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        print("X                                     X")
        print("X    GAME OVER, YOUR SCORE IS", self.score, "    X")
        print("X                                     X")
        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        exit(0)

    def export_data(self):
        return {"score": self.score,
                "lives": self.lives,
                "x": self.x, "y": self.y,
                "tank": self.tank,
                "mxtank": self.mxtank}
    
    def import_data(self,data):
        self.score = data["score"] or 0
        self.lives = data["lives"] or 20
        self.x = data["x"] or 0
        self.y = data["y"] or 0
        self.tank = data["tank"] or 0
        self.mxtank = data["mxtank"] or 1
from utils import randbool
from utils import randcell
from utils import randneibor

# 0 - поле
# 1 - дерево
# 2 - река
# 3 - госпиталь
# 4 - апгрейд-шоп
# 5 - огонь

CELL_TYPES = "🟩🎄🌊🏥🏪🔥"
TREE_BONUS = 100
UPDATE_COST = 5000
LIFE_COST = 10000

class map:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[0 for i in range(w)] for j in range(h)]
        self.generete_forest(8,10)
        self.generete_river(10)
        self.generete_river(20)
        self.generate_shop()
        self.generate_hospital()
        
    def check_bounds(self, x,y):
        if (x < 0 or y < 0 or x>= self.h or y >= self.w):
            return False
        return True

    def print_map(self, heleco, clouds):
        print("⬛" * (self.w + 2))
        for ri in range(self.h):
            print("⬛", end='')
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if clouds.cells[ri][ci] == 1:
                    print("⚪", end="")
                elif clouds.cells[ri][ci] == 2:
                    print("🌀", end="")
                elif heleco.x == ri and heleco.y == ci:
                    print("🚁", end="")
                elif cell >= 0 and cell < len(CELL_TYPES):
                    print(CELL_TYPES[cell], end="")
            print("⬛")
        print("⬛" * (self.w + 2))

    def generete_forest(self, r, mxr):
        for ri in range(self.h):
            for ci in range(self.w):
                if (randbool(r,mxr)):
                    self.cells[ri][ci] = 1

    def generete_river(self, l):
        rc = randcell(self.w,self.h)
        rx, ry = rc[0], rc[1]
        self.cells[rx][ry] = 2
        while l > 1:
            rc2 = randneibor(rx,ry)
            rx2, ry2 = rc2[0], rc2[1]
            if (self.check_bounds(rx2, ry2)):
                # if (self.cells[rx2][ry2] != 2):
                    self.cells[rx2][ry2] = 2
                    rx, ry = rx2, ry2
                    l-=1

    def generate_tree(self):
        c = randcell(self.w,self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == 0):
            self.cells[cx][cy] = 1

    def generate_shop(self):
        c = randcell(self.w,self.h)
        cx,cy = c[0],c[1]
        self.cells[cx][cy] = 4
    def generate_hospital(self):
        c = randcell(self.w,self.h)
        cx,cy = c[0],c[1]
        if self.cells[cx][cy] != 4:
            self.cells[cx][cy] = 3
        else:
            self.generate_hospital()

    def add_fire(self):
        c = randcell(self.w,self.h)
        cx, cy = c[0], c[1]
        if (self.cells[cx][cy] == 1):
            self.cells[cx][cy] = 5

    def update_fire(self):
        for ri in range(self.h):
            for ci in range(self.w):
                cell = self.cells[ri][ci]
                if cell == 5:
                    self.cells[ri][ci] = 0
        for i in range(10):
            self.add_fire()

    def process_helecopter(self, heleco, cloud):
        m = self.cells[heleco.x][heleco.y]
        c = cloud.cells[heleco.x][heleco.y]
        if  m == 2:
            heleco.tank = heleco.mxtank
        if m == 5 and heleco.tank >= 1:
            heleco.tank -= 1
            self.cells[heleco.x][heleco.y] = 1
            heleco.score += TREE_BONUS
        if m == 4 and heleco.score >= UPDATE_COST:
            heleco.mxtank += 1
            heleco.score -= UPDATE_COST
        if m == 3 and heleco.score >= LIFE_COST:
            heleco.lives += 10
            heleco.score -= LIFE_COST
        if  c == 2:
            heleco.lives -= 1
            if heleco.lives == 0:
                heleco.game_over()

    def export_data(self):
        return {"cells": self.cells}
    
    def import_data(self,data):
        self.cells = data["cells"] or [[0 for i in range(self.w)] for j in range(self.h)]
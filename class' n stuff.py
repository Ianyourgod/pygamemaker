import os, time, threading
from getkey import get, getnum, getchars
coldi = {"orange": "🟧 ","yellow": "🟨 ","brown": "🟫 ","blue": "🟦 ","red": "🟥 ","green": "🟩 ","purple": "🟪 ","black": "⬛ ","white": "⬜ "}
pxl=[]
pyl=[]
scl=[]
stl = []
obx, oby = [], []
obc = "black"
Pc = "black"
wnx = 0
wny = 0
def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
class player:
    def __init__(self, x1, y1, x2, y2, col = "black"):
        global pxl, pyl, Pc
        self.pxl, self.pyl = [], []
        for i in range(y2 - y1 + 1):
            for a in range(x2 - x1 + 1):
                pxl.append(x1 + a)
                pyl.append(y1 + i)
                self.pxl.append(x1 + a)
                self.pyl.append(y1 + i)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.dimx = x2 - x1
        self.dimy = y2 - y1
        Pc = col
    def left(self, am=1):
        global pxl, pyl
        if type(am) == float:
            return
        pxl = []
        self.pxl = []
        self.x1 -= am
        self.x2 -= am
        for i in range(self.y2 - self.y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pxl.append(self.x1 + a)
                self.pxl.append(self.x1 + a)
    def right(self, am=1):
        global pxl, pyl
        if type(am) == float:
            return
        pxl = []
        self.pxl = []
        self.x1 += am
        self.x2 += am
        for i in range(self.y2 - self.y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pxl.append(self.x1 + a)
                self.pxl.append(self.x1 + a)
    def down(self, am=1):
        global pyl
        if type(am) == float:
            return
        pyl = []
        self.pyl = []
        self.y1 += am
        self.y2 += am
        for i in range(self.y2 - self.y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pyl.append(self.y1 + i)
                self.pyl.append(self.y1 + i)
    def up(self, am=1):
        global pyl
        if type(am) == float:
            return
        pyl = []
        self.y1 -= am
        self.y2 -= am
        for i in range(self.y2 - self.y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pyl.append(self.y1 + i)
                self.pyl.append(self.y1 + i)
    def goto(self, x, y):
        global pxl, pyl
        self.x1 = x
        self.x2 = x + self.dimx
        self.y1 = y
        self.y2 = y + self.dimy
        self.pxl, self.pyl = [], []
        pxl, pyl = [], []
        for i in range(self.y2 - self.y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pxl.append(self.x1 + a)
                pyl.append(self.y1 + i)
                self.pxl.append(self.x1 + a)
                self.pyl.append(self.y1 + i)
    def touching(self, obj, dis = 0):
        global pxl, pyl, obx, oby
        for i in range(len(obj.obx)):
            if (self.x1 - 1 - dis) < obj.obx[i] < (self.x2 + 1 + dis):
                for a in range(len(obj.oby)):
                    if (self.y1 - 1 - dis) < obj.oby[a] < (self.y2 + 1 + dis):
                        return True
        return False
    def touEg(self, edge = "all"):
        if edge == "all": 
            if self.x2 == wnx or self.x1 == 1 or self.y1 == 1 or self.y2 == wny:
                return True
        elif edge == "left":
            if self.x1 == 1:
                return True
        elif edge == "right":
            if self.x2 == wnx:
                return True
        elif edge == "bottom":
            if self.y2 == wny:
                return True
        elif edge == "top":
            if self.y1 == 1:
                return True
        return False
    def __del__(self):
        #runned before deleting
        global pxl, pyl
        pxl, pyl = [], []
        
            
class obj:
    def __init__(self, x1, y1, x2, y2, color):
        global obx, oby, obc
        self.obx = []
        self.oby = []
        ycor = 0
        for i in range(y2 - y1 + 1):
            for a in range(x2 - x1 + 1):
                obx.append(x1 + a)
                oby.append(y1 + i)
                self.obx.append(x1 + a)
                self.oby.append(y1 + i)
        self.x1, self.y1, self. x2, self.y2, obc = x1, y1, x2, y2, color
        self.dimx = x2 - x1
        self.dimy = y2 - y1
        
    def goto(self, x, y):
        global obx, oby
        obx.pop(self.obx)
        oby.pop(self.oby)
        self.obx, self.oby = [], []
        self.x1 = x
        self.x2 = x + self.dimx
        self.y1 = y
        self.y2 = y + self.dimy
        for i in range(y2 - y1 + 1):
            for a in range(self.x2 - self.x1 + 1):
                pxl.append(self.x1 + a)
                pyl.append(self.y1 + i)
                self.obx.append(self.x1 + a)
                self.oby.append(self.y1 + i)
        
        
        
class screen:
    def __init__(self, xdim, ydim, bgcolor = 'white'):
        global wnx, wny, coldi
        self.xdim = xdim
        self.ydim = ydim
        self.bgcolor = bgcolor
        wnx = xdim
        wny = ydim
        print(((coldi[bgcolor] * xdim) + "\n")  * ydim)
        
    def update(self):
        global pxl, pyl, coldi
        clear()
        ycor = 0
        ie = 0
        ieo = 0
        try:
            curx = pxl[ie]
            cury = pyl[ie]
        except IndexError:
            curx = 0
            cury = 0
        try:
            curox = obx[ieo]
            curoy = oby[ieo]
        except IndexError:
            curox = 0
            curoy = 0
        for i in range(self.ydim):
            ycor += 1
            xcor = 0
            for i in range(self.xdim):
                xcor += 1
                pri = 0
                while curx < 1 or cury < 1:
                    ie += 1
                    try:
                        curx = pxl[ie]
                        cury = pyl[ie]
                    except IndexError:
                        print("", end="")
                try:
                    curx = pxl[ie]
                    cury = pyl[ie]
                except IndexError:
                    print("", end="")
                try:
                    if xcor > pxl[ie] and ycor > pyl[ie]:
                        ie += 1
                except IndexError:
                    print("", end="")
                if xcor == curx and ycor == cury:
                    ie += 1
                    pri = 1
                
                if xcor == curox and ycor == curoy:
                    ieo += 1
                    pri = 2
                    try:
                        curox = obx[ieo]
                        curoy = oby[ieo]
                    except IndexError:
                        curox = 0
                        curoy = 0
                if pri == 1:
                    print("⬛ ", end="")
                elif pri == 2:
                    print(coldi[obc], end="")
                else:
                    print(coldi[self.bgcolor], end="")
            print()
        time.sleep(.07)
    def bgColor(self, col):
        self.bgcolor = col
def getinp(am):
    return get(am)

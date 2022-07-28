import os


classes = {}
coli = []
def _bresenham(start, end):
    # referenced from http://www.poshy.net/java/graphic/linedraw4.htm
    # tooken from https://gist.github.com/hallazzang/df3fde293e875892be02 
    ret = []
    x0,y0 = start
    x1,y1 = end
    dx = x1 - x0
    dy = y1 - y0

    if dy < 0:
        dy = -dy
        stepy = -1
    else:
        stepy = 1

    if dx < 0:
        dx = -dx
        stepx = -1
    else:
        stepx = 1

    dx <<= 2
    dy <<= 2

    ret.append((x0, y0))

    if dx > dy:
        fraction = dy - (dx >> 1)
        while x0 != x1:
            if fraction >= 0:
                y0 += stepy
                fraction -= dx
            x0 += stepx
            fraction += dy
            ret.append((x0, y0))
    else:
        fraction = dx - (dy >> 1)
        while y0 != y1:
            if fraction >= 0:
                x0 += stepx
                fraction -= dy
            y0 += stepy
            fraction += dx
            ret.append((x0, y0))
    return ret
class pen:
    def __init__(self,x:int,y:int,color:str="⬛") -> None:
        self.x,self.y,self.color=x,y,color
        coli.append((y,x,color))
    def goto(self,x:int,y:int):
        for i in _bresenham((self.x,self.y),(x,y)):
            temp = i[::-1]
            temp = list(temp)
            temp.append(self.color)
            temp = tuple(temp)
            coli.append(temp)
        self.x,self.y = x,y
    def left(self,amount:int):
        self.goto(self.x - amount, self.y)
    def right(self,amount:int):
        self.goto(self.x + amount, self.y)
    def up(self,amount:int):
        self.goto(self.x, self.y - amount)
    def down(self,amount:int):
        self.goto(self.x, self.y + amount)
class obj:
    def __init__(self,x:int,y:int,xdim:int=1,ydim:int=1,color="⬛") -> None:
        self.x,self.y,self.xdim,self.ydim=x,y,xdim,ydim
        self.coli = []
        for i in range(ydim):
            for a in range(xdim):
                self.coli.append((i + y, a + x,color))
        self.show()
        #adding atributes
        self.hitx1,self.hity1,self.hitx2,self.hity2,self.color = x,y,x+xdim,y+ydim,color
    def touching(self,obj=None,objClass=None):
        if objClass != None:
            try:
                cls = classes[objClass]
            except KeyError:
                raise Exception(f"Class \"{objClass}\" does not exist.")
            for ob in cls.objs:
                if (self.hitx1 <= ob.hitx1 and self.hitx2 >= ob.hitx1) or (self.hitx1 <= ob.hitx2 and self.hity2 >= ob.hitx2):
                    return True
            return False
        try:
            if (self.hitx1 <= obj.hitx1 and self.hitx2 >= obj.hitx1) or (self.hitx1 <= obj.hitx2 and self.hity2 >= obj.hitx2):
                return True
        except AttributeError:
            raise Exception(f"Object \"{obj}\" does not exist.")
        return False
    def show(self):
        for i in self.coli:
            coli.append(i)
    def hide(self):
        for i in self.coli:
            coli.remove(i)
    def __del__(self):
        try:
            self.hide()
        except ValueError:
            pass
    def goto(self,x:int,y:int):
        self.hide()
        self.coli = []
        for i in range(self.ydim):
            for a in range(self.xdim):
                self.coli.append((i + y, a + x,self.color))
        self.show()
        self.x,self.y = x,y
    def left(self,amount:int):
        self.goto(self.x - amount, self.y)
    def right(self,amount:int):
        self.goto(self.x + amount, self.y)
    def up(self,amount:int):
        self.goto(self.x, self.y - amount)
    def down(self,amount:int):
        self.goto(self.x, self.y + amount)
class window:
    def __init__(self,dimx:int,dimy:int,clear:bool=False) -> None:
        self.dimx,self.dimy,self.clearScreen=dimx,dimy,clear
    def _fix(self):
        global coli
        used = []
        temp = []
        for i in coli:
            if not (i[0],i[1]) in used:
                used.append((i[0],i[1]))
                temp.append(i)
        coli = temp

    def clear(self):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
    def update(self):
        ie = 1
        coli.sort()
        self._fix()
        if self.clearScreen:
            self.clear()
        try:
            curx = coli[0][1]
            cury = coli[0][0]
            curcolor = coli[0][2]
        except IndexError:
            curx = -1
            cury = -1
        for ycor in range(self.dimy):
            for xcor in range(self.dimy):
                if xcor == curx and ycor == cury:
                    print(curcolor,end="")
                    try:
                        curx = coli[ie][1]
                        cury = coli[ie][0]
                        curcolor = coli[ie][2]
                        ie += 1
                    except IndexError:
                        curx = -1
                        cury = -1
                else:

                    print("⬜",end="")
            print()


class objClass:
    def __init__(self,name) -> None:
        self.objs = []
        self.name = name
        classes[name] = self
    def append(self,obj:obj):
        self.objs.append(obj)
        classes[self.name] = self
    def remove(self,obj):
        try:
            self.obj.remove(obj)
            classes[self.name] = self
        except ValueError:
            raise Exception(f"Object \"{obj}\" is not in the class \"{self.name}\".")

        


if __name__ == "__main__":
    p1 = obj(4,3,2,2)
    obj1 = obj(1,1,color="🟫")
    obj2 = obj(4,3,color="🟫")
    cls = objClass("wall")
    cls.append(obj1)
    cls.append(obj2)
    pen1 = pen(0,0)
    pen1.goto(3,8)
    wn = window(10,10,True)
    wn.update()
    if p1.touching(objClass="wall"):
        print("touching")
    else:
        print("not touching")

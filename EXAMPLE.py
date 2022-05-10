import game, random, time
wn = game.screen(29, 30) #setting up
ob1 = game.obj(9, 30, 9, 30, "purple") #adding color
ob2 = game.obj(20, 30, 29, 30, "red") # will make it all red because currently it's just a global variable that determines the color but I'll have to make some kind of list thingy
p1 = game.player(1, 2, 3, 4) # spawn player
df, rt, vel = 0, .1, 0 #vars for grav
def grav(): # if in the air then bring down a certain amount
    global df, rt, vel
    if not (p1.touEg("bottom") or p1.touching(ob2, 1)): # if youching floor or object dont go down
        vel += rt #adding velocity
        rt += .02
    else:
        vel = 0
        rt = .1
        df = 0
    df += vel #downforce
    tdf = 0
    while df > 1: #get total downforce (cant go down by float)
        tdf += 1 # total downforce
        df -= 1
    while (p1.y2 + tdf) > 30: #dont go through the floor
        tdf -= 1
    p1.down(tdf)
while True: #game loop
    wn.update() #update screen
    grav() 
    inp = game.getinp(1) #detect keypress (1) is asking how many keys to look for
    # movement
    if inp == "w" and (p1.touEg("bottom") or p1.touching(ob2, 1)): # dont fly
        p1.up(1)
    elif inp == "a":
        p1.left()
    elif inp == "s":
        if p1.y2 < 30: # dont go through the floor
            p1.down()
    elif inp == "d":
        p1.right()
    if p1.touching(ob1): # if touching kill thingy go to spawn
        p1.goto(1, 28)

import pgzrun
import random

WIDTH = 1000
HEIGHT = 600


BACKGROUND_TITLE = "background_logo"
BACKGROUND_LEVEL1 = "background_level"
BACKGROUND_LEVEL2 = "background_level2"
BACKGROUND_LEVEL3 = "background_level3"
BACKGROUND_IMG = "background_"
PLAYER_IMG = "player_ship"
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"
SCOREBOX_HEIGHT = 60

level = 0
level_screen = 0
score = 0
junk_collect=0
lvl2_LIMIT=5
lvl3_LIMIT=10
JUNK_SPEED = 5
SATELLITE_SPEED = 3
DEBRIS_SPEED = 3
LASER_SPEED = -5

#initialize player
def init():
    global player, junks, satellite, debris, lasers
    player - Actor(PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT/2)

    #initialize junks
    
    junks = []
    for i in range(5):
        junk=actor(JUNK_IMG)
        x_pos=random.randint(-500,-50)
        y_pos=random.randint (SCOREBOX_HEIGHT, HEIGHT-junk.height)
        junk.topright=(x_pos, y_pos)
        junks.append(junk)

    #initialize satellite
    satellite=Actor(SATELLITE_IMG)
    x_sat=random.randint(-500, -50)
    y_sat=random.randint (SCOREBOX_HEIGHT, HEIGHT-satellite.height)
    satellite.topright-(x_sat. y_sat)

    #initialize satellite
    debris=Actor(DEBRIS_IMG)
    x_deb=random.randint(-500, -50)
    y_deb=random.randint (SCOREBOX_HEIGHT, HEIGHT-debris.height)
    debris.topright-(x_deb. y_deb)

    #initialize lasers
    lasers = []
    player.laserActive = 1
    
#initialize title screen buttons
start_button = Actor(START_IMG)
start_button.centre = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)


#game loop
init()

def update():
    global level, level_screen, BACKGROUND_IMG, junk_collect
    if junk_collect == lvl2_LIMIT:
        level==2
    if junk_collect == lvl3_LIMIT:
        level==3
    if level == 1: #instructions screen
        BACKGROUND_IMG = BACKGROUND_LEVEL1
    if level>=1:
        if level_screen==1:
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN==1:
                level_screen = 2
        if level_screen==2:
            updatePlayer()
            updateJunk()
        if level ==2 and level_screen<=3:
            BACKGROUND_IMG= BACKGROUND_LEVEL2
            level_screen=3
            if keyboard.RETURN == 1:
                level_screen = 4
        if level_screen ==4:
            updatePlayer()
            updateJunk()
            updateSatellite()
        if level==3 and level_screen <=5:
            BACKGROUND_IMG = BACKGROUNDLEVEL3
            if keyboard.RETURN == 1:
                level_screen=6
        if level_screen==6:
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()
            

            
            updateSatellite()
            updateDebris()
            updateLasers()

def updatePlayer():
    if (keyboard.up == 1):
        player.y += -5
    elif (keyboard.down == 1):
        player.y += 5
    if player.top<60:
        player.top=60

    if player.bottom >HEIGHT:
        player.bottom = HEIGHT

    if keyboard.space == 1:
        laser=Actor(LASER_IMG)
        laser.midright=player.midleft
        fireLasers(laser)

def updateJunk():
    global score
    for junk in junks:junk.x += JUNK_SPEED
    collision = player.colliderect(junk)
    if junk.left > WIDTH or collision == 1:
        x_pos = -50
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)

    if (collision == 1):
        score += 1

def updateSatellite():
    global score
    satellite.x += SATELLITE_SPEED

    collision=player.colliderect(satellite)
    if satellite.left>WIDTH or collision==1:
        x_sat=random.randint(-500, -50)
        y_sat=random.randint(SCOREBOX_HEIGHT, HEIGHT-satellite.height)
        satellite.topright=(x_sat, y_sat)

    if collision==1:
        score+=-10

def updateDebris():
    global score
    debris.x+=DEBRIS_SPEED

    collision = player.colliderect(debris)
    if debris.left>WIDTH or collision ==1:
        x_deb=random.randint(-500,-50)
        y_deb=random.randint(SCOREBOX_HEIGHT, HEIGHT-debris.height)
        debris.topright=(x_deb, y_deb)

    if collision ==1:
        score+=-10

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0, 0))
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level == -1:
        start_button.draw()
        show_instructions = "insert instructions"
        screen.draw.text(show_instrutions, midtop=(WIDTH/2,70), fontsize=35, color="white")
    if level >=1:
        player.draw()
        for junk in junks:
            junk.draw()
        satellite.draw()
        debris.draw()
        for laser in lasers:
            laser.draw()
    #draw some text on the screen
    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(750, 15), fontsize=35, color="white")

def updateLasers():
    global score
    for laser in lasers:
        laser.x+=LASER_SPEED
        #remove laser if off screen
        
        if laser.right<0:
            lasers.remove(laser)
        #check for collisions
        if satellite.colliderect(laser)==1:
            lasers.remove(laser)
            x_sat=random.randint(-500,-50)
            y_sat=random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score+=-5
        if debris.colliderect(laser)==1:
            lasers.remove(laser)
            x_deb=random.randint(-500,-50)
            y_deb=random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score+=-5

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level=1
        level_screen=1
        print("start button is pressed")

    if instructions_button.collidepoint(pos):
        level=-1
        print("Instructions button is pressed")
                            
    
pgzrun.go()                            
                    
    
        


    

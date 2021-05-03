
import pgzrun
import random
import time

# define screen
WIDTH = 1000
HEIGHT = 550
SCOREBOX_HEIGHT = 60  

# count score
score = 0  
junk_collect = 0
level = 0
level_screen = 0
lvl2_LIMIT = 5
lvl3_LIMIT = 10
TIME_LIMIT = 60

# sprite speeds
junk_speed = sat_speed = 3
debris_speed = 5
laser_speed = -5
start_time = 0
elapse_time = 0

BACKGROUND_TITLE = "background_logo"
BACKGROUND_LEVEL1 = "background_level1"
BACKGROUND_LEVEL2 = "background_level2"
BACKGROUND_LEVEL3 = "background_level3"

BACKGROUND_IMG = "background_logo"  
PLAYER_IMG = "player_ship"  
JUNK_IMG = "space_junk"
SATELLITE_IMG = "satellite_adv"  
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_img"
START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"


def init():
    # INITIALIZE SPRITES
    global player, junks, satellite, debris, lasers
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 10, HEIGHT / 2)


    junks = [] 
    for i in range(5):
        junk = Actor(JUNK_IMG)  
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
        junk.pos = (x_pos, y_pos)  
        junks.append(junk)

    # initialize satellite
    satellite = Actor(SATELLITE_IMG)  
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)  

    # initialize debris
    debris = Actor(DEBRIS_IMG)
    x_deb = random.randint(-500, -50)
    y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

    # initialize lasers
    lasers = []  
    player.laserActive = 1
    
    #background music
    music.play("background")

# initialize title screen buttons
start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level = 1
        level_screen = 1
    if instructions_button.collidepoint(pos):
        level = -1

def timer():
    global start_time, elapse_time
    current_time = time.time()
    elapse_time = current_time - start_time

# MAIN GAME LOOP

init()


def update():  # main update function
    global score, junk_collect, level, level_screen, BACKGROUND_IMG, elapse_time, start_time

    if elapse_time > TIME_LIMIT:  #end game
        level_screen = 0
        level = -2
    if junk_collect == lvl2_LIMIT:  #level 2
        level = 2
    if junk_collect == lvl3_LIMIT:  #level 3
        level = 3
    if level == -1:  #instructions
        BACKGROUND_IMG = BACKGROUND_LEVEL1

    if score >= 0 and level >= 1:
        if level_screen == 1:  #level 1 title screen
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2
                music.play("sweet")
                start_time = time.time()
        if level_screen >= 2:  #timer
            timer()
        if level_screen == 2:  #level 1 gameplay
            updatePlayer()  
            updateJunk()
        if level == 2 and level_screen <= 3:  # level 2 title screen
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            level_screen = 3
            music.stop()
            if keyboard.RETURN == 1:
                level_screen = 4
                music.play("spacelife") #adds music to each level
        if level_screen == 4:  #level 2 gameplay
            updatePlayer()
            updateJunk()
            updateSatellite()
        if level == 3 and level_screen <= 5:  #level 3 title screen
            level_screen = 5
            music.stop()
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            if keyboard.RETURN == 1:
                level_screen = 6
                music.play("suspense") #adds music to each level
        if level_screen == 6:  #level 3 game play
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()

    if score < 0 or level == -2:  #game over screen
        music.stop()
        if keyboard.RETURN == 1:
            BACKGROUND_IMG = BACKGROUND_TITLE
            score = 0
            junk_collect = 0
            level = 0
            start_time = 0
            elapse_time = 0
            init()
 

def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0, 0))
    if level == -1:
        start_button.draw()
        show_instructions = "Use the UP and DOWN arrow keys to move the spaceship\n\nLEVEL 1:\nCollect Space Junk to increase your score\n\nLEVEL 2:\nCollect Space Junk and avoid active satellites\n\nLEVEL 3:\nCollect Space Junk, avoid active satellites, and shoot dead satellites\nPress SPACEBAR to shoot!"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 70), fontsize=35, color="white")
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level >= 1:
        player.draw()
        for junk in junks:
            junk.draw() 
    if level >= 2:
        satellite.draw()
    if level == 3:
        debris.draw()
        for laser in lasers:
            laser.draw()

    #game over screen
    if score < 0:
        game_over = "GAME OVER\nPress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH / 2, HEIGHT / 2), fontsize=60, color="white")

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(650, 15), fontsize=35, color="white")
    show_collect_value = "Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(450, 15), fontsize=35, color="white")
    show_time = "Time: "
    screen.draw.text(show_time, topleft=(850, 15), fontsize=35, color="white")

    if level >= 1 and TIME_LIMIT >= elapse_time:
        show_level = "LEVEL " + str(level)
        screen.draw.text(show_level, topright=(375, 15), fontsize=35, color="white")
        show_time = "Time: " + str(TIME_LIMIT - int(elapse_time))
        screen.draw.text(show_time, topleft=(850, 15), fontsize=35, color="white")

    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "LEVEL " + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center=(WIDTH/2, HEIGHT/2), fontsize=70, color="white")

    if elapse_time > TIME_LIMIT:
        show_end_screen = "You win!\nScore: " + str(score) + "\nPress ENTER to play again"
        screen.draw.text(show_end_screen, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="white")


#Updates
        
def updatePlayer():
    if keyboard.up == 1:
        player.y += -5 
    elif keyboard.down == 1:
        player.y += 5
    if player.top < SCOREBOX_HEIGHT:
        player.top = SCOREBOX_HEIGHT
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    #check if firing lasers
    if keyboard.space == 1 and level == 3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)


def updateJunk():
    global score, junk_collect
    for junk in junks:  
        junk.x += junk_speed

        collision = player.colliderect(junk)

        if junk.left > WIDTH or collision == 1:  
            x_pos = random.randint(-500, -50)
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1: 
            score += 1
            junk_collect += 1
            sounds.collect.play()

def updateSatellite():
    global score
    satellite.x += sat_speed  
    collision = player.colliderect(satellite)

    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint(-500, -50)
        y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -15


def updateDebris():
    global score
    debris.x += debris_speed
    collision = player.colliderect(debris)

    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint(-500, -50)
        y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score += -15


def updateLasers():
    global score
    for laser in lasers:
        laser.x += laser_speed
        if laser.right < 0:
            lasers.remove(laser)
        if satellite.colliderect(laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint(-500, -50)
            y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5
            sounds.explosion.play()
        if debris.colliderect(laser) == 1:
            lasers.remove(laser)
            x_deb = random.randint(-500, -50)
            y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 5
            sounds.explosion.play()


# activating lasers 

def makeLaserActive():  
    global player
    player.laserActive = 1


def fireLasers(laser):
    if player.laserActive == 1:  
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  
        sounds.laserfire02.play()  #play sound effect
        lasers.append(laser)  


pgzrun.go()  #runs the game



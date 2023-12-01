#################################################
# Doodle Jump Ultra Term Project
# name: Daniel Zhu
# andrew id: danielzh
#################################################

##################################
## Extras Edits
##################################

#1. attempt to make the platforms move randomly
#2. attempt to put enemies in game
#3. attempt to make Doodle shoot   
#4. attempt to make a Start Menus

##################################

from cmu_112_graphics import *
import random
import math

##################################
## Citations
##################################
# Base code given by 112 TA's as part of the Ultra Pivot
#
# Features:
#
# Image insertion: Thursday 3/31 Mini Lecture on Images
# All graphics functions based from: https://www.cs.cmu.edu/~112/notes/notes-graphics.html
# All animation functions based from: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
##################################
## Helpers
##################################

def rectanglesCollide(left1, top1, width1, height1, left2, top2, width2, height2):
    if (left1 + width1 >= left2
        and left2 + width2 >= left1
        and top1 + height1 >= top2
        and top2 + height2 >= top1):
        return True
    else:
        return False

##################################
## Platform
##################################

class Platform(object):
    def __init__(self, app, cx, cy):
        self.cx = cx
        self.cy = cy
        self.width, self.height = getPlatformDims(app)
        self.springiness = app.height // 19

        # Try app.height // 10 for something like a spring
        # Or app.height / 2 a rocket!

    def getLeftTop(self):
        return (self.cx - self.width // 2, self.cy - self.height // 2)

    def collidesWithRectangle(self, other):
        left1, top1 = self.getLeftTop()
        left2, top2 = other.getLeftTop()

        return rectanglesCollide(left1, top1, self.width, self.height, 
                                 left2, top2, other.width, other.height)

    def __eq__(self, other):
        return self.cx == other.cx and self.cy == other.cy


class Doodle(object):
    def __init__(self, app):
        self.width, self.height = getDoodleDims(app)
        self.cx = app.width // 2
        self.cy = app.height - (2 * self.height)

        self.speed = self.width // 5
        self.facingDirection = app.left

        self.dx = 0
        self.dy = 0

    def getLeftTop(self):
        return (self.cx - self.width // 2, self.cy - self.height // 2)

    def collidesWithRectangle(self, other):
        left1, top1 = self.getLeftTop()
        left2, top2 = other.getLeftTop()

        return rectanglesCollide(left1, top1, self.width, self.height, 
                                 left2, top2, other.width, other.height)

def moveDoodle(app, doodle):
    doodle.dy += app.gravity

    for key in app.keysHeld:
        if key == 'Left':
            doodle.cx -= doodle.speed
            doodle.facingDirection = app.left
        if key == 'Right':
            doodle.cx += doodle.speed
            doodle.facingDirection = app.right

    doodle.cy += doodle.dy

    doodleWrapAround(app, doodle)
    doodleScrollUp(app, doodle)
    doodleCheckGameOver(app, doodle)

    if doodle.dy > 0:
        doodleCheckPlatformCollisions(app, doodle)
        
#####################################
## Doodle dies if touches Monster
#####################################
      
def hitMonsterGameOver(app, doodle):
    for i in range(len(app.monsters)):

        monstercx = app.platforms[i].cx
        monstercy = app.platforms[i].cy
        
        if ((monstercx - 40 <= doodle.cx <= monstercx + 40) 
                and (monstercy - 25 <= doodle.cy <= monstercy + 25)):        
            return True

def doodleCheckGameOver(app, doodle):
    left, top = doodle.getLeftTop()
    if (top + doodle.height > (app.height - app.scrollY) 
                or hitMonsterGameOver(app, doodle)):
        app.gameOver = True
        
####################################
'''
def getDoodleDims(app):
    width = app.width // 7
    height = app.width // 7
    return width, height

'''
######################################

def doodleScrollUp(app, doodle):
    if doodle.cy < (app.height // 2) - app.scrollY:
        app.scrollY = (app.height // 2 - doodle.cy)
        app.spawnProtection += 1
      
    highestPlatformY = getHighestPlatformY(app)
    if highestPlatformY > -(app.scrollY + app.height):
        generatePlatforms(app, -highestPlatformY + app.height)

    newPlatforms = []
    for platform in app.platforms:
        if (platform.cy + app.scrollY - platform.height // 2) <= app.height:
            newPlatforms.append(platform)
    app.platforms = newPlatforms


def doodleWrapAround(app, doodle):
    left, top = doodle.getLeftTop()
    if (left + doodle.width) < 0:
        doodle.cx = app.width - (doodle.width // 2)
    elif left > app.width:
        doodle.cx = doodle.width // 2

def doodleCheckPlatformCollisions(app, doodle):
    for platform in app.platforms:
        if doodleCollidesWithPlatform(doodle, platform):
            _, platformTop = platform.getLeftTop()
            doodle.cy = platformTop - (doodle.height // 2)
            doodle.dy = -(platform.springiness)

def doodleCollidesWithPlatform(doodle, platform):
    platformLeft, platformTop = platform.getLeftTop()
    left, top = doodle.getLeftTop()

    # Only collide with a platform if our bottom was just
    # above its bottom
    return (doodle.collidesWithRectangle(platform) and 
            (platformTop + platform.height > (top + doodle.height - doodle.dy)))

##################################
## Platform generation
##################################

def distance(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def getHighestPlatform(app):
    highestPlatformY = getHighestPlatformY(app)
    for platform in app.platforms:
        if platform.cy == highestPlatformY:
            return platform

def getHighestPlatformY(app):
    platformCYs = []
    for platform in app.platforms:
        platformCYs.append(platform.cy)
    return min(platformCYs)

def getPlatformDims(app):
    width = app.width // 6
    height = app.height // 30
    return width, height

def getDoodleDims(app):
    width = app.width // 7
    height = app.width // 7
    return width, height

def collidesWithAnyPlatform(app, testPlatform, newPlatforms):
    for platform in (newPlatforms + app.platforms):
        if testPlatform.collidesWithRectangle(platform):
            return True
    return False

def generateOnePlatform(app, height, newPlatforms):
    platformWidth, platformHeight = getPlatformDims(app)
    xMargin = (platformWidth // 2) + (app.width // 20)

    while True:
        cx = random.randrange(xMargin, app.width - xMargin)
        cy = random.randrange(0, app.height) - height
        testPlatform = Platform(app, cx, cy)

        if collidesWithAnyPlatform(app, testPlatform, newPlatforms):
            continue

        return testPlatform

def getNumberOfPlatforms(app):
    # 1 less platform every 2000 pixels
    platformsRemoved = int(app.scrollY // 2000)

    # Never add fewer than 4 platforms
    return max(11 - platformsRemoved, 3)

def hasNearbyAbovePlatform(app, platform, newPlatforms):
    # Ignore platforms near the top of the screen
    isNotAtTop = False
    for possibleNeighbor in newPlatforms:
        if platform.cy > possibleNeighbor.cy:
            isNotAtTop = True
    
    if not isNotAtTop:
        return True

    for possibleNeighbor in newPlatforms:
        if platform == possibleNeighbor:
            continue
        if platform.cy < possibleNeighbor.cy:
            continue
        dist = distance(platform.cx, platform.cy, 
                        possibleNeighbor.cx, possibleNeighbor.cy)
        if dist <= (max(app.width, app.height) // 3):
            return True
    return False

def isValidPlatformGroup(app, newPlatforms):
    for platform in newPlatforms:
        if not hasNearbyAbovePlatform(app, platform, newPlatforms):
            return False
    
    # Doodle must be able to reach the new set of platforms via
    # the highest platform currently on the app
    if not hasNearbyAbovePlatform(app, getHighestPlatform(app), newPlatforms):
        return False
    return True

def generatePlatforms(app, height):
    while True:
        newPlatforms = []
        for i in range(getNumberOfPlatforms(app)):
            platform = generateOnePlatform(app, height, newPlatforms)
            newPlatforms.append(platform)
        if isValidPlatformGroup(app, newPlatforms):
            break
    return app.platforms.extend(newPlatforms)
    
##################################
##Added feature: Moving Platform
################################## 

#Randomly selects which platfor moves  
def selectMovingPlatforms(app):
    while len(app.movingPlat) < 5:
        platformIndex = random.randint(0, len(app.platforms) - 1)
        app.movingPlat.append(platformIndex)

    return movePlatform(app)

#Moves the platform  
def movePlatform(app):
    for i in app.movingPlat:  
        
        if app.platforms[i].cy < app.platforms[i].cy + app.height:     
            app.platforms[i].cx += 2.5 * app.direction
            
            if (app.platforms[i].cx > app.width or app.platforms[i].cx < 1):
                app.direction = -app.direction
                
#################################
## Added feature: Shooting
#################################

def doodleShoot(app):
    for i in range(len(app.bullets)):
        app.bullets[i][0] += app.bullets[i][2]
        app.bullets[i][1] += app.bullets[i][3]

#################################

##################################
## Event Handlers
##################################

def loadDoodleImages(app):
    doodleWidth, doodleHeight = getDoodleDims(app)

    # Falling Doodle
    doodleLeftImg = app.loadImage('images/doodle.png')
    doodleLeftImg = doodleLeftImg.resize((doodleWidth, doodleHeight),
                                         resample=Image.ANTIALIAS)

    doodleRightImg = doodleLeftImg.transpose(Image.FLIP_LEFT_RIGHT)

    app.doodleLeftTk = ImageTk.PhotoImage(doodleLeftImg)
    app.doodleRightTk = ImageTk.PhotoImage(doodleRightImg)

    # Jumping Doodle
    doodleJumpingLeftImg = app.loadImage('images/doodleJumping.png')
    doodleJumpingLeftImg = doodleJumpingLeftImg.resize(
                                    (doodleWidth, doodleHeight),
                                    resample=Image.ANTIALIAS)

    doodleJumpingRightImg = doodleJumpingLeftImg.transpose(
                                    Image.FLIP_LEFT_RIGHT)

    app.doodleJumpingLeftTk = ImageTk.PhotoImage(doodleJumpingLeftImg)
    app.doodleJumpingRightTk = ImageTk.PhotoImage(doodleJumpingRightImg)


def loadImages(app):
    # Load background
    backgroundImg = app.loadImage('images/background.png')
    backgroundImg = backgroundImg.resize((app.width, app.height), 
                                         resample=Image.ANTIALIAS)

    app.backgroundTk = ImageTk.PhotoImage(backgroundImg)

    # Load platform
    platformWidth, platformHeight = getPlatformDims(app)
    platformImg = app.loadImage('images/platform.png')
    platformImg = platformImg.resize((platformWidth, platformHeight),
                                     resample=Image.ANTIALIAS)
    app.platformTk = ImageTk.PhotoImage(platformImg)
    
##################################
## Import Monster 
##################################
    
    monsterImg = app.loadImage('images/monster.png')
    monsterImg = monsterImg.resize((platformWidth, platformHeight),
                                     resample=Image.ANTIALIAS)
    app.monsterTk = ImageTk.PhotoImage(monsterImg)

##################################
    
    # Load doodles
    loadDoodleImages(app)

def appStarted(app):
    app.timerDelay = 30

    app.left = 'left'
    app.right = 'right'

    app.gravity = 1.5
    app.scrollY = 0
    app.gameOver = False

    loadImages(app)

    app.doodle = Doodle(app)
    app.platforms = [Platform(app, app.width // 2, app.height - app.doodle.height)]
    generatePlatforms(app, 0)
    app.keysHeld = set()
#################################    
#Edited section
    app.movingPlat = []
    app.monsters = []
    app.platWidth = 50
    app.platHeight = 10
    app.direction = 5
    app.bullets = []
    app.bulletXAxis = 0
    app.bulletYAxis = 10
    app.cx = app.width // 2
    app.cy = app.height // 2
    app.gameStart = True
    app.spawnProtection = 0
##################################
## Edits made to timerFired
##################################

def timerFired(app):
    if app.gameOver:
        return     
    moveDoodle(app, app.doodle)
    selectMovingPlatforms(app)
    selectMonsters(app)
    doodleShoot(app)
##################################

def keyPressed(app, event):
    if app.gameOver and event.key == 'r':
        appStarted(app) 
        
################################################      
## Edits added in for Shooting and Menu Start
################################################

    elif app.gameStart and event.key == 't':
        app.gameStart = False 
        
    elif (event.key == 'Up'):
        app.bulletYAxis = -10
        app.bullets.append([app.cx, app.cy, 0, app.bulletYAxis])
        
#################################################

    app.keysHeld.add(event.key)
        
def keyReleased(app, event):
    app.keysHeld.remove(event.key) 

##################################
## Drawing
##################################

def drawGameOver(app, canvas):
    canvas.create_text(app.width // 2, app.height // 2, 
                       text='Game Over', font="Arial 25 bold")
    canvas.create_text(app.width // 2, app.height // 2 + app.height // 15, 
                       text="Press 'r' to restart", font="Arial 15 bold")

###########################################
## Added Feature: Start Menu
###########################################

def drawGameStart(app, canvas):
    font = 'Arial 12 bold'
    canvas.create_text(app.width / 2, 100, text = 'Game Start', font = 'Arial 25 bold')
    canvas.create_text(app.width / 2, 200, 
                        text = '1. Use left and right arrow keys to move', font = font)
    canvas.create_text(app.width/2, 250, 
                        text = '2. Use up arrow key to shoot', font = font)
    canvas.create_text(app.width / 2, 300, 
                        text = "3. Stay on the platforms", font = font)
    canvas.create_text(app.width / 2, 350, 
                    text = "4. Don't step on monsters!", font = font)
    canvas.create_text(app.width / 2, 400, 
                            text ='Press "t" to start the game', font = font)
            
############################################

def drawPlatform(app, canvas, platform):
    canvas.create_image(platform.cx, platform.cy + app.scrollY, 
                        image=app.platformTk)

def drawDoodle(app, canvas, doodle):
    if doodle.dy < 0:
        if doodle.facingDirection == app.left:
            image = app.doodleJumpingLeftTk
        else:
            image = app.doodleJumpingRightTk
    else:
        if doodle.facingDirection == app.left:
            image = app.doodleLeftTk
        else:
            image = app.doodleRightTk
        
    canvas.create_image(doodle.cx, doodle.cy + app.scrollY, 
                        image=image)
#####################################
# Edited Drawings for Monsters
#####################################
def selectMonsters(app):
    if app.spawnProtection < 10:
        
        while len(app.monsters) < 1:
            monsterIndex = random.randint(0, len(app.platforms) - 1)
            app.monsters.append(monsterIndex)

   #  return movePlatform(app)

def drawMonster(app, canvas, platform):
    for i in range(len(app.monsters)):

        monstercx = app.platforms[i].cx
        monstercy = app.platforms[i].cy
        
        canvas.create_image(monstercx, (monstercy + app.scrollY) - 15, 
                        image = app.monsterTk)
        

'''
       
        if app.platforms[i].cy < app.platforms[i].cy + app.height:     
            app.platforms[i].cx += 2.5 * app.direction
            
            if (app.platforms[i].cx > app.width or app.platforms[i].cx < 1):
                app.direction = -app.direction

    i = random.randrange(0,100)
    if i < 2:
        canvas.create_image(platform.cx, (platform.cy + app.scrollY) - 15, 
                        image = app.monsterTk)

    i = random.randrange(0,100)
    z = random.randrange(0,10)
    if i < 101:
        if z < 5:
            canvas.create_image(platform.cx, (platform.cy + app.scrollY) - 15, 
                        image = app.monsterTk)

''' 
        
def drawBullet(app, canvas):
    r = 6
    for i in range(len(app.bullets)):
        x, y = app.bullets[i][0], app.bullets[i][1]
        y -= app.scrollY
        canvas.create_oval(x, y, x + r, y + r, fill = 'green')
        
#######################################
    
def redrawAll(app, canvas):
    # Draw background
    canvas.create_image(app.width//2, app.height//2, image=app.backgroundTk)

    if app.gameOver:
        drawGameOver(app, canvas)
    elif app.gameStart:
        drawGameStart(app, canvas)
        return

    for platform in app.platforms:
        drawPlatform(app, canvas, platform)
        drawMonster(app, canvas, platform)
    drawBullet(app, canvas)
    drawDoodle(app, canvas, app.doodle)

    # Draw score
    canvas.create_text(app.width//20, app.height // 20, 
                       text=int(app.scrollY), font="Arial 15 bold", anchor='nw')

##################################
## Run the app
##################################

runApp(width=400, height=500)
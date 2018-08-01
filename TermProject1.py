import pygame, sys, os
from pygame.locals import *
import math

pygame.mixer.pre_init(44100,-16, 2, 1024)
pygame.init()

class Animation(object):
    def __init__(self, width, height):
        self.width, self.height = width , height
        self.screen = pygame.display.set_mode((width, height))

    def mouseButtonUp(self, event): pass

    def mouseButtonDown(self, event): pass

    def keyPressed(self, event) : pass

    def mouseMotion(self, event): pass

    def drawGame(self): pass

    def run(self) :
    	self.clock = pygame.time.Clock()
    	self.framesPerSec = 60
        running = True
        while running : 
            for event in pygame.event.get() : 
                if event.type == QUIT: 
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION :
                	self.mouseMotion(event)
                if event.type == MOUSEBUTTONDOWN :
                	self.mouseButtonDown(event)
                if event.type == KEYDOWN :
                	self.keyPressed(event)
            self.playGame()
            pygame.display.update()
            self.clock.tick(self.framesPerSec)

class BlueBalls(Animation):
	def __init__(self, width, height):
		super(BlueBalls, self).__init__(width, height)	
		self.init(width, height)

	def init(self, width, height):
		level = 1
		self.text = Text(self.width, self.height)
		self.button = Button(self.width, self.height)
		self.music = Music()
		self.court = Court(width, height)
		self.ball = Ball(width, height, self.court, level)
		self.opponent = Opponent(width, height, self.court)		
		self.user = User(width, height, self.court)
		# For my direction of the ball , True = away from user
		self.direction = True
		self.isBallMoving = True
		# False = opp, True = user
		self.checkPlayer = False
		self.music.playTheme()
		self.displayMenu = True
		self.displayHelp = False
		self.beginLevel = False
		self.gameOver = False
		self.level = 1
		self.isMusicPlaying = True
		self.score = 0
		self.displayTransitionScreenTwo = False
		self.displayTransitionScreenThree = False

	def keyPressed(self, event):
		if event.key == K_ESCAPE:
			pygame.quit()
			sys.exit()

	def mouseMotion(self, event):
		xPos, yPos = pygame.mouse.get_pos()
		if self.displayMenu == True:
			self.checkForSelectedButtons(xPos, yPos)
		elif self.displayHelp == True:
			self.checkBackButton(xPos, yPos)
		elif self.gameOver == True :
			self.checkReturnButton(xPos, yPos)
		else : self.moveUserPad(xPos, yPos)

	def checkForSelectedButtons(self, xPos, yPos):
		self.checkStartButton(xPos, yPos)
		self.checkHelpButton(xPos, yPos)
		# self.checkHighScoreButton(xPos, yPos)

	def checkStartButton(self, xPos, yPos):
		centerX = self.width / 2
		buttonWidth = self.button.buttonWidth
		startYPos = self.button.startYPos
		buttonHeight = self.button.buttonHeight
		if ((xPos >= centerX - buttonWidth /2  and 
			xPos <= centerX + buttonWidth / 2) and 
		   (yPos >= startYPos   and 
			yPos <= startYPos + buttonHeight)):

		   	self.button.startSelected = True
		   	return True
		else : self.button.startSelected = False

	def checkHelpButton(self, xPos, yPos):
		centerX = self.width / 2
		buttonWidth = self.button.buttonWidth
		startYPos = self.button.helpYPos
		buttonHeight = self.button.buttonHeight
		if ((xPos >= centerX - buttonWidth /2  and 
			xPos <= centerX + buttonWidth / 2) and 
		   (yPos >= startYPos   and 
			yPos <= startYPos + buttonHeight)):
		   	self.button.helpSelected = True
		   	return True
		else : self.button.helpSelected = False

	def moveUserPad(self, xPos, yPos):
		(cX , cY)= self.width / 2, self.height / 2
		(winWidth, winHeight) = self.court.largeWidth, self.court.largeHeight
		# dividing by two because i want to know the distance form center
		padWidth = self.user.width / 2
		padHeight = self.user.height /2
		if xPos >= cX :
			# I want to always be inside the big court screen
			self.user.cX = min(xPos, cX + winWidth / 2 - padWidth)
		else : self.user.cX = max(xPos, cX - winWidth / 2 + padWidth)
		if yPos >= cY :
			self.user.cY = min(yPos, cY + winHeight / 2 - padHeight)
		else :  self.user.cY = max(yPos, cY - winHeight / 2 + padHeight)

	def mouseButtonDown(self, event):
		leftClicked, rightClicked, centerClicked = pygame.mouse.get_pressed()
		xPos, yPos = pygame.mouse.get_pos()
		if leftClicked == True :
			if self.displayMenu == True :
				self.checkGameButtonsClicked(xPos, yPos)
			elif self.displayHelp == True :
				self.checkBackButtonClicked(xPos,yPos)
			elif self.gameOver == True :
				self.checkReturnButtonClicked(xPos, yPos)
			elif self.displayTransitionScreenOne == True :
				self.displayTransitionScreenOne = False
				self.music.playLevel1()
				self.isMusicPlaying = True
			elif self.displayTransitionScreenTwo == True :
				self.displayTransitionScreenTwo = False
				self.music.playLevel2()
				self.isMusicPlaying = True
			elif self.displayTransitionScreenThree == True :
				self.displayTransitionScreenThree = False
				self.music.playLevel3()
				self.isMusicPlaying = True
			elif self.beginLevel == False: 
				#this will see if the user clicked on the paddle to start
				self.checkToStartGame(xPos, yPos)

	def checkReturnButtonClicked(self, xPos, yPos):
		if self.checkReturnButton(xPos, yPos) == True:
			self.init(self.width, self.height)

	def checkReturnButton(self, xPos, yPos):
		buttonWidth = self.button.buttonWidth
		startYPos = 0
		buttonHeight = self.button.buttonHeight
		if ((xPos >= 0  and 
			xPos <= buttonWidth) and 
		   (yPos >= startYPos   and 
			yPos <= startYPos + buttonHeight)):
		   	self.button.returnSelected = True
		   	return True
		else : self.button.returnSelected = False

	def checkBackButton(self, xPos, yPos):
		buttonWidth = self.button.buttonWidth
		startYPos = 0
		buttonHeight = self.button.buttonHeight
		if ((xPos >= 0  and 
			xPos <= buttonWidth) and 
		   (yPos >= startYPos   and 
			yPos <= startYPos + buttonHeight)):
		   	self.button.backSelected = True
		   	return True
		else : self.button.backSelected = False

	def checkBackButtonClicked(self, xPos, yPos):
		if self.checkBackButton(xPos, yPos) == True:
			self.displayHelp = False
			self.displayMenu = True

	def checkGameButtonsClicked(self, xPos, yPos):
		if self.checkStartButton(xPos, yPos) == True :
			self.displayMenu = False
			self.music.stopTheme()
			self.isMusicPlaying = False
			self.displayTransitionScreenOne = True
			
		elif self.checkHelpButton(xPos, yPos) == True :
			self.displayMenu = False
			self.displayHelp = True

	def drawTransitionScreenToLevelOne(self, screen):
		self.court.drawCourt(screen)
		self.text.drawLevelOneText(screen)

	def drawTransitionScreenToLevelTwo(self, screen):
		self.court.drawCourt(screen)
		self.text.drawLevelTwoText(screen)

	def drawTransitionScreenToLevelThree(self, screen):
		self.court.drawCourt(screen)
		self.text.drawLevelThreeText(screen)

	def checkToStartGame(self, xPos, yPos):
		#check if the paddle clicks on the ball
		centerX = self.width / 2
		centerY = self.height / 2
		radius = self.ball.radius
		padWidth = self.user.width / 2
		padHeight = self.user.height / 2
		if ((xPos + padWidth > centerX - radius and 
			 xPos - padWidth < centerX + radius) and
			 (yPos + padHeight > centerY - radius and
			  yPos - padHeight < centerY + radius)):
			self.music.userHit.play()
	 		self.beginLevel = True

	def playGame(self):
		self.screen.fill((0,0,0,0))
		if self.displayMenu == True:
			self.drawMenu(self.screen)
		elif self.displayHelp == True:
			self.drawHelp(self.screen)
		elif self.gameOver == True :
			self.drawGameOver(self.screen)
		elif self.displayTransitionScreenOne == True :
			self.drawTransitionScreenToLevelOne(self.screen)
		elif self.displayTransitionScreenTwo == True :
			self.drawTransitionScreenToLevelTwo(self.screen)
		elif self.displayTransitionScreenThree == True :
			self.drawTransitionScreenToLevelThree(self.screen)	
		else : 
			self.drawGame()
			self.opponent.findVelocity(self.framesPerSec)
			self.user.findVelocity(self.framesPerSec)
			if self.beginLevel == True:
				if self.isBallMoving == True:
					self.moveScreen()
					self.ball.move(self.oldScreenWidth, self.oldScreenHeight,
								   self.music, self.direction)
				self.checkHits(self.user.xVel, self.user.yVel)
			self.opponent.move(self.direction, self.ball, self.isBallMoving, self.level)

	def drawGameOver(self, screen):
		self.music.stopLevel1()
		self.music.stopLevel2()
		self.music.stopLevel3()
		self.court.drawCourt(screen)
		text = "You Couldn't Finish!!!!"
		text2 = "#Blueballs"
		self.drawTopText(screen, text)
		self.drawBottomText(screen, text2)
		self.drawScore(screen)
		self.button.drawReturn(screen)

	def drawBottomText(self, screen, text):
		bottomText = pygame.font.Font(None, 20)
		textWidth, textHeight = bottomText.size(text)
		bottomText = bottomText.render(text, 10, (0, 255, 255))
		textYPos = self.height / 2
		textXPos = self.width / 2 - textWidth / 2
		screen.blit(bottomText, (textXPos, textYPos))

	def drawTopText(self, screen, text):	
		topText = pygame.font.Font(None, 45)
		(textWidth, textHeight) = topText.size(text) 
		topText = topText.render(text, 10 ,(0, 255, 255)) 
		textYPos = self.height / 4
		textXPos = (self.width / 2) - (textWidth / 2)	
		screen.blit(topText, (textXPos, textYPos))

	def drawHelp(self, screen):
		self.court.drawCourt(screen)
		self.text.drawHelpText(screen)
		self.button.drawBackButton(screen)	

	def drawMenu(self, screen):
		button = self.button
		self.court.drawCourt(screen)
		heightDif = self.height / 10
		tittleHeight = self.height / 10
		self.startButtonHeight = self.height / 2 - heightDif
		self.helpButtonHeight = self.height / 2 
		self.highScoreButtonHeight = self.height / 2 + 2 * heightDif
		button.drawButtons(screen)

	def checkHits(self, userXVel, userYVel):
		court = self.court
		newScreenArea = self.newScreenArea
		#check right when the screen changes direction
		if ((newScreenArea < court.smallArea and self.direction == True) or
			(newScreenArea > court.largeArea and self.direction == False)):
			if self.direction == True : 
				if self.checkIfHit(self.opponent) == True:
					self.music.oppHit.play()
				else : 
					self.music.oppMiss.play()
					self.doIfPlayerMiss(self.opponent)
			else: 
				if self.checkIfHit(self.user) == True :
					self.ball.dVx = self.user.xVel
					self.ball.dVy = self.user.yVel
					self.addScore(userXVel, userYVel)
					self.music.userHit.play()
				else : 
					self.music.userMiss.play()
					self.doIfPlayerMiss(self.user)
			self.direction = not self.direction

	def addScore(self, xVel, yVel):
		regPnts = 100
		levelPnts = 500 * (self.level - 1)
		extraPnts = (xVel**2 + yVel**2) * 2500
		self.score += int(regPnts + round(extraPnts, -1)) + levelPnts

	def doIfPlayerMiss(self, player):
		player.lives -= 1
		if player == self.user :
			if player.lives < 0 :
				self.gameOver = True
		else : 
			if player.lives < 0 :
				self.level += 1
				player.dx += 200
				player.dy += 200
				if self.level == 2:
					self.music.stopLevel1()
					self.displayTransitionScreenTwo = True
				elif self.level == 3:
					self.music.stopLevel2()
					self.displayTransitionScreenThree = True
				self.opponent.lives = 2
		self.beginLevel = False
		self.ball.reset(self.court, self.level)
		self.isBallMoving = True
	
	def checkIfHit(self, player):
		ball = self.ball
		court = self.court
		self.checkLeftRight(player.cX, player.width)
		self.checkTopBottom(player.cY, player.height)
		if self.isBallMoving == True : 
			return True

	def checkLeftRight(self, padcX, padWidth):
		ball = self.ball
		if (ball.cX + ball.radius > padcX - padWidth /2  and
		    ball.cX - ball.radius < padcX + padWidth / 2):
			self.direction = not self.direction
		else : self.isBallMoving = False

	def checkTopBottom(self, padcY , padHeight):
		ball = self.ball
		if (ball.cY + ball.radius > padcY - padHeight /2  and
		    ball.cY - ball.radius < padcY + padHeight / 2):
			self.direction = not self.direction
		else : self.isBallMoving = False

	def moveScreen(self):
		width, height = self.width, self.height
		court, ball= self.court, self.ball
		self.oldScreenWidth = ball.screenWidth
		self.oldScreenHeight = ball.screenHeight
		self.oldScreenArea = ball.screenWidth * ball.screenHeight
		self.getAreaConstant(width, height, self.oldScreenArea)
		self.getNewArea(ball, court, width, height, self.oldScreenArea)

	def getNewArea(self, ball, court, width, height, oldScreenArea):
		self.newScreenArea = self.oldScreenArea - self.constant
		heightRatio = math.sqrt(self.newScreenArea / 
					 (width * height * court.widthToHeightRatio))
		ball.screenHeight = (height * heightRatio)
		ball.screenWidth = (width *  heightRatio * court.widthToHeightRatio)

	def getAreaConstant(self, width, height, oldScreenArea):
		if self.direction == True:
			self.constant = oldScreenArea / (width * height) * 15000
		else : self.constant = -oldScreenArea / (width * height) * 15000
		
	def drawGame(self):
		screen, ball, court = self.screen, self.ball, self.court
		user, opponent = self.user, self.opponent
		court.drawCourt(screen)
		self.drawStats(screen)
		opponent.makePaddle(screen)
		ball.drawBall(screen)
		ball.drawBallScreen(screen, self.width, self.height)
		user.makePaddle(screen)

	def drawStats(self, screen):
		self.drawScore(screen)
		self.opponent.drawLives(screen)
		self.user.drawLives(screen)
		# self.drawBonus(screen)

	def drawScore(self, screen):
		yPos = (self.height - self.court.largeHeight) / 1.7
		xPos = (self.width - self.court.largeWidth) / 1
		score = "Score: " + str(self.score)
		self.scoreText = pygame.font.Font(None, self.width / 25)
		self.scoreText = self.scoreText.render(score, 10, (255, 255, 255))
		screen.blit(self.scoreText, (xPos,yPos))
		
class Court(object):
	def __init__(self, width, height):
		self.width, self.height = width , height
		self.color = (0, 255, 0)
		self.getCloseWall()
		self.getFarWall()
		self.getInsideBoxes()
		self.getDiags()

	def drawCourt(self, screen):   
		pygame.draw.lines(screen, self.color, True, self.closeWallPnts, 2)
		pygame.draw.lines(screen, self.color, True, self.farWallPnts, 1)
		self.drawDiags(screen)
		self.drawInsideBoxes(screen)

	def drawInsideBoxes(self, screen):
		for points in self.insideBoxes :
			pygame.draw.lines(screen, self.color, True, points, 1)

	def drawDiags(self, screen):
		pointsInBox = 4
		start = self.diagsStart
		end = self.diagsEnd
		for point in xrange(pointsInBox) :
			pygame.draw.line(screen, self.color, start[point],end[point], 1)

	def getInsideBoxes(self):
		width, height = self.width, self.height
		self.insideBoxes = []
		newArea = self.largeArea
		while (newArea) >(self.smallArea) :
			heightRatio = math.sqrt(newArea / 
						 (width * height * self.widthToHeightRatio))
			# wH = wallHeight, wW = wallWidth, cX = centerX, cY, centerY
			wH = height * heightRatio
			wW = width *  heightRatio * self.widthToHeightRatio
			cX, cY = width /2 , height / 2
			self.insideBoxes.append( [(cX - wW /2, cY - wH/2),
									  (cX + wW /2, cY - wH/2),
								  	  (cX + wW /2, cY + wH/2), 
								  	  (cX - wW /2, cY + wH/2 )])
			newArea *= self.areaRatio

	def getDiags(self):
		self.diagsStart = []
		self.diagsEnd = []
		pointsInBox = 4
		for point in xrange(pointsInBox):
			self.diagsStart.append(self.closeWallPnts[point])
			self.diagsEnd.append(self.farWallPnts[point])


	def getFarWall(self):
		width, height = self.width, self.height
		# wH = wallHeight, wW = wallWidth, cX = centerX, cY, centerY
		heightRatio = .20
		wH = height * heightRatio
		wW = width *  heightRatio * self.widthToHeightRatio
		cX, cY = width /2 , height / 2
		self.smallWidth, self.smallHeight = (wW,wH)
		self.smallArea = wH * wW
		self.farWallPnts = [(cX - wW /2, cY - wH/2), (cX + wW /2, cY - wH/2),
							(cX + wW /2, cY + wH/2), (cX - wW /2, cY + wH/2 )]

	def getCloseWall(self):
		width, height = self.width, self.height
		# wH = wallHeight, wW = wallWidth, cX = centerX, cY, centerY
		heightRatio = .79
		widthRatio = .86
		wH = height * heightRatio
		wW = width * widthRatio
		self.largeWidth, self.largeHeight = (wW), (wH)
		self.widthToHeightRatio = widthRatio / heightRatio
		self.areaRatio = .7
		self.largeArea = wH * wW
		cX, cY = width / 2 , height/2
		self.closeWallPnts = [(cX - wW /2, cY - wH/2), (cX + wW /2, cY - wH/2),
							  (cX + wW /2, cY + wH/2), (cX - wW /2, cY + wH/2)]

class Ball(object):
	def __init__(self, width, height, court, level):
		self.winWidth, self.winHeight = (width, height)
		self.court = court
		self.init(court, level)

	def init(self, court, level):
		self.cX, self.cY = self.winWidth / 2 ,  self.winHeight /2
		self.screenWidth, self.screenHeight = ((court.largeWidth), 
											   (court.largeHeight))
		(self.dx, self.dy) = (0,0)
		self.maxArea =  self.screenWidth * self.screenHeight
		if level == 1 :
			self.color = (24, 116, 205)
		elif level == 1 :
			self.color = (28, 134, 238)
		else : self.color = (0 , 191, 255)
		self.screenColor = (64, 224, 208)
		#change in velocity of the ball
		self.dVx , self.dVy = (0, 0)

	def reset(self, court, level):
		self.init(court, level)

	def drawBall(self, screen):
		self.radius = int(self.screenWidth / 20.0)
		pygame.draw.circle(screen , self.color,(int(self.cX), int(self.cY)), 
						   self.radius)

	def drawBallScreen(self, screen, width, height):
		# self.screenWidth
		cX, cY = width / 2, height / 2 
		wW, wH = self.screenWidth, self.screenHeight
		point1 = (cX - wW /2, cY - wH /2)
		point2 = (cX + wW /2, cY - wH /2)
		point3 = (cX + wW /2, cY + wH /2)
		point4 = (cX - wW /2, cY + wH /2)
		pygame.draw.lines(screen, self.screenColor, True,
						 [point1, point2, point3, point4], 2 )

	def move(self, oldScreenWidth, oldScreenHeight, music, direction):
		self.dx -= (self.dVx) * 1.0
		self.dy -= (self.dVy) * 1.0
		self.doChangeInCenters()
		self.getNewCenters(oldScreenWidth, oldScreenHeight)
		self.checkSidesHit(music)

	def doChangeInCenters(self):
		# Use the large screen as main reference
		self.newdx = self.dx * self.screenWidth / self.court.largeWidth
		self.newdy = self.dy * self.screenHeight / self.court.largeHeight
		self.cX += self.newdx
		self.cY += self.newdy

	def checkSidesHit(self, music):
		width, height = self.winWidth, self.winHeight
		# check if the ball hits the left or right of the moving screen
		leftScreen = (width / 2) - (self.screenWidth / 2)
		rightScreen = (width / 2) + (self.screenWidth / 2)
		topScreen = (height / 2) - (self.screenHeight / 2)
		bottomScreen = (height / 2) + (self.screenHeight / 2)
		if ((self.cX - self.radius < leftScreen and self.dx < 0) or 
			(self.cX + self.radius > rightScreen and self.dx > 0)) :
			music.leftRightHit.play()
			self.dx *= -1
		if ((self.cY - self.radius < topScreen and self.dy < 0) or 
			(self.cY + self.radius > bottomScreen and self.dy > 0 )) :
			music.topBottomHit.play()
			self.dy *= -1

	def getNewCenters(self, oldScreenWidth, oldScreenHeight):
		screencX, screencY = self.winWidth/2 ,self.winHeight / 2
		#get distance from the center in x and y
		disFromcX, disFromcY = screencX - self.cX, screencY - self.cY
		#proportion it to the old screen
		disFromcX /= oldScreenWidth
		disFromcY /= oldScreenHeight
		# use same ratio to get new centers
		self.cX = (screencX - (self.screenWidth * disFromcX))
		self.cY = (screencY - (self.screenHeight * disFromcY))

class Paddle(object):
	def __init__(self, width, height, court):
		self.court = court
		(self.winWidth, self.winHeight) = (width, height)
		self.cX, self.cY = width / 2, height / 2
		self.fillColor = (155, 155, 155, 155)

	def drawLives(self, screen):
		diffBetweenRadii = self.winWidth / 66
		radius = int(self.winWidth / 165)
		#these are the opponents lives
		if self.livesXPos > self.winWidth / 2: 
 			difference =  - diffBetweenRadii
 		else : difference = diffBetweenRadii
 		for lives in xrange(self.lives) :
 			xPos, yPos = self.livesXPos, self.livesYPos
 			newDiff = lives * difference
 			newXPos, newYPos = (xPos + newDiff, yPos)
 			pygame.draw.circle(screen, self.borderColor, 
 							  (int(newXPos), int(newYPos)), radius)

	def makePaddle(self, screen):
		#determive the scale factors
		unitW , unitH = int(self.width / 10.0), int(self.height / 6.0)
		self.makeCorners(screen, unitW, unitH, self.cX, self.cY)
		self.makeLines(screen, unitW, unitH, self.cX, self.cY)

	def makeCorners(self, screen, unitW, unitH, cX, cY):
		pi = math.pi
		width = 4 * unitW
		height = 4 * unitH
		# top left Corner
		pygame.draw.arc(screen, self.borderColor, 
				[cX - 5 * unitW, cY - 3 * unitH, width, height],
				 pi / 2 , pi , self.borderWidth)
		pygame.draw.arc(screen, self.borderColor, 
				[cX + 1 * unitW, cY - 3 * unitH, width, height],
				 0 , pi /2 , self.borderWidth)
		pygame.draw.arc(screen, self.borderColor, 
				[cX + 1 * unitW, cY - 1 * unitH, width, height],
				-pi /2, 0, self.borderWidth)
		pygame.draw.arc(screen, self.borderColor, 
				[cX - 5 * unitW, cY - 1 * unitH, width, height],
				-pi , -pi / 2, self.borderWidth)

	def makeLines(self, screen, unitW, unitH, cX, cY): 
		#top line
		pygame.draw.line(screen,self.borderColor,
						(cX - 3 * unitW, cY - 3 * unitH),
						(cX + 3 * unitW, cY - 3 * unitH), self.borderWidth ) 
		#bottom line
		pygame.draw.line(screen, self.borderColor,
						(cX - 3 * unitW, cY + 3 * unitH),
						(cX + 3 * unitW, cY + 3 * unitH), self.borderWidth ) 
		# left line
		pygame.draw.line(screen, self.borderColor,
						(cX - 5 * unitW, cY - 1 * unitH),
						(cX - 5 * unitW, cY + 1 * unitH), self.borderWidth ) 
		# right line
		pygame.draw.line(screen, self.borderColor,
						(cX + 5 * unitW, cY - 1 * unitH),
						(cX + 5 * unitW, cY + 1 * unitH), self.borderWidth ) 

class User(Paddle):
	def __init__(self, width, height, court):
		super(User, self).__init__(width, height, court)
		self.width =self.width = court.largeWidth / 5
		self.height = court.largeHeight / 5
		self.borderColor = (0,0,209)
		self.borderWidth = 3
		self.lives = 5
		self.prevPos = pygame.mouse.get_pos()
		self.livesXPos = (self.winWidth - court.largeWidth) * 1.5
		self.livesYPos = (self.winHeight - court.largeHeight) / 2 * 1.9

	def findVelocity(self, framesPerSec):
		xPos, yPos = pygame.mouse.get_pos()
		prevX, prevY = self.prevPos
		dx, dy = xPos - prevX, yPos - prevY
		# v = dx / dt
		self.xVel = float(dx)/framesPerSec
		self.yVel = float(dy)/framesPerSec
		self.prevPos = xPos, yPos

class Opponent(Paddle):
	def __init__(self, width, height, court):
		super(Opponent, self).__init__(width, height, court)
		self.width = court.smallWidth / 5
		self.height = court.smallHeight / 5
		self.borderColor = (205,0,0) # red ish
		self.borderWidth = 1
		self.lives = 2
		self.prevPos = self.width / 2, self.height / 2
		self.livesXPos = self.winWidth - (self.winWidth - court.largeWidth) * 1.5
		self.livesYPos = (self.winHeight - court.largeHeight) / 2 * 1.9
		self.dx = 500
		self.dy = 500

	def findVelocity(self, framesPerSec):
		xPos, yPos = self.cX, self.cY
		prevX, prevY = self.prevPos
		dx, dy = xPos - prevX, yPos - prevY
		# v = dx / dt
		self.xVel = float(dx)/framesPerSec 
		self.yVel = float(dy)/framesPerSec
		self.prevPos = xPos, yPos

	def move(self, direction, ball, isBallMoving, level):
		if level == 3 and self.lives == 0:
			self.moveToBall(ball, level)
		elif direction == False: 
			self.moveToCenter()
		elif isBallMoving == True:
			self.moveToBall(ball, level)

	def moveToCenter(self):
		wincX, wincY = self.winWidth / 2 , self.winHeight / 2
		self.getSpeedOfPad(wincX, wincY)
		self.cX += self.actualdx
		self.cY += self.actualdy

	def getSpeedOfPad(self, wincX, wincY):
		dx, dy = wincX - self.cX, wincY - self.cY
		dis = math.sqrt((dx)**2 + (dy)**2)
		if dis > self.width:
			move = 15
		else : move = 20
		self.actualdx  = dx * move / self.court.largeWidth
		self.actualdy = dy * move / self.court.largeHeight

	def moveToBall(self, ball, level):
		self.translateCoords(ball)
		if self.ballcX > self.cX:
			dx = self.dx
		else : dx = -self.dx
		if self.ballcY > self.cY:
			dy = self.dy
		else : dy = -self.dy
		actualdx = dx / self.court.largeWidth
		actualdy = dy / self.court.largeHeight
		if level == 3 and self.lives == 0: 
			self.cX = self.ballcX
			self.cY = self.ballcY
		else:
			self.cX += actualdx
			self.cY += actualdy

	def translateCoords(self, ball):
		oldX, oldY = ball.cX , ball.cY
		dX =  oldX - self.winWidth / 2
		dY = oldY - self.winHeight / 2  
		netDX = (dX) / ball.screenWidth
		netDY = (dY) / ball.screenHeight
		self.ballcX = self.winWidth / 2 + (self.court.smallWidth * netDX)
		self.ballcY = self.winHeight / 2 + (self.court.smallHeight * netDY)


class Music(object):
	def __init__(self):
		self.getGameMusic()
		self.getGameSounds()

	def getGameSounds(self):
		directory = os.getcwd() + "/TermProject/TermProjectSounds/"
		self.userHit = pygame.mixer.Sound(directory + 'UserHit.wav')
		self.oppHit = pygame.mixer.Sound(directory + 'OppHit.wav')
		self.userMiss = pygame.mixer.Sound(directory + 'UserMiss.wav')
		self.oppMiss = pygame.mixer.Sound(directory + 'OppMiss.wav')
		self.leftRightHit = pygame.mixer.Sound(directory + 'LRHit.wav')
		self.topBottomHit = pygame.mixer.Sound(directory + 'TBWall.wav')
		self.userHit.set_volume(.1)
		self.oppHit.set_volume(.1)
		self.userMiss.set_volume(.1)
		self.oppMiss.set_volume(.1)
		self.leftRightHit.set_volume(.1)
		self.topBottomHit.set_volume(.1)

	def getGameMusic(self):
		directory = os.getcwd() + "/TermProject/TermProjectSounds/"
		self.mainTheme = pygame.mixer.Sound(directory + 'OpeningAudio.wav')
		self.level1 = pygame.mixer.Sound(directory + 'Level1Audio.wav')
		self.level2 = pygame.mixer.Sound(directory + 'Level2Audio.wav')
		self.level3 = pygame.mixer.Sound(directory + 'Level3Audio.wav')

	def playTheme(self):
		self.mainTheme.play(-1)

	def stopTheme(self):
		self.mainTheme.fadeout(1000)

	def playLevel1(self):
		self.level1.set_volume(.05)
		self.level1.play(-1)

	def stopLevel1(self):
		self.level1.fadeout(500)

	def playLevel2(self):
		self.level2.set_volume(.05)
		self.level2.play(-1)

	def stopLevel2(self):
		self.level2.fadeout(500)

	def playLevel3(self):
		self.level3.set_volume(.05)
		self.level3.play(-1)

	def stopLevel3(self):
		self.level3.fadeout(500)

class Button(object):
	def __init__(self, width, height):
		self.width, self.height = width , height
		self.loadImages()
		self.init(width, height)
		
	def loadImages(self):
		directory = os.getcwd() + "/TermProject/TermProjectPics/"
		tittle = pygame.image.load(directory + "logo.png")
		startGame = pygame.image.load(directory + "startGame.png")
		startSelect = pygame.image.load(directory + "startGameSelect.png")
		help = pygame.image.load(directory + 'helpMain.png')
		helpInverted = pygame.image.load(directory + 'helpInverted.png')
		back = pygame.image.load(directory + 'back.png')
		backSelect = pygame.image.load(directory + 'backSelect.png')
		returnMainMenu = pygame.image.load(directory + 'mainMenu.png')
		returnSelect = pygame.image.load(directory + 'mainMenuSelected.png')
		self.getSizes(tittle, startGame, startSelect, help, helpInverted,
					  back, backSelect, returnMainMenu, returnSelect)

	def init(self, width, height):
		self.startSelected = False
		self.helpSelected = False
		self.highScoreSelected = False
		self.backSelected = False
		self.returnSelected = False
		self.heightDif = self.height / 10
		self.tittleHeight = self.height / 10
		self.startYPos = self.height / 2 - self.heightDif
		self.helpYPos = self.height / 2 
		self.highScoreYPos = self.height / 2 + 2 * self.heightDif
		
	def getSizes(self,tittle, startGame, startSelect, help, helpInverted,
				 back, backSelect, returnMainMenu, returnSelect):
		self.tittleWidth = int(.7 * self.width)
		self.tittleHeight = int(.2 * self.height)
		self.buttonWidth = int(self.width / 5)
		self.buttonHeight = int(self.height / 15)
		self.tittle = pygame.transform.smoothscale(tittle, 
					 (self.tittleWidth, self.tittleHeight))
		self.startGame = pygame.transform.smoothscale(startGame, 
						(self.buttonWidth, self.buttonHeight))
		self.startGameSelect = pygame.transform.smoothscale(startSelect,
							  (self.buttonWidth, self.buttonHeight))
		self.help = pygame.transform.smoothscale(help, 
				   (self.buttonWidth, self.buttonHeight))
		self.helpInverted = pygame.transform.smoothscale(helpInverted, 
						   (self.buttonWidth, self.buttonHeight))
		self.back = pygame.transform.smoothscale(back, 
					(self.buttonWidth, self.buttonHeight))
		self.backSelect = pygame.transform.smoothscale(backSelect, 
					(self.buttonWidth, self.buttonHeight))
		self.returnMainMenu = pygame.transform.smoothscale(returnMainMenu, 
					(self.buttonWidth, self.buttonHeight))
		self.returnSelect = pygame.transform.smoothscale(returnSelect, 
					(self.buttonWidth, self.buttonHeight))

	def drawButtons(self, screen):
		self.drawTittle(screen, self.tittleHeight)
		self.drawPlayGameButton(screen, self.startYPos)
		self.drawHelpButton(screen, self.helpYPos)
		# self.drawHighScoreButton(screen, self.highScoreYPos)

	def drawReturn(self, screen):
		(xPos , yPos) = (0,0)
		if self.returnSelected == True :
			screen.blit(self.returnSelect, (xPos, yPos))
		else : screen.blit(self.returnMainMenu, (xPos, yPos))

	def drawBackButton(self, screen):
		(xPos , yPos) = (0,0)
		if self.backSelected == True :
			screen.blit(self.backSelect, (xPos, yPos))
		else : screen.blit(self.back, (xPos, yPos))

	def drawTittle(self, screen, yPos):
		tittleWidth = self.tittleWidth
		xPos = self.width / 2 - tittleWidth / 2
		screen.blit(self.tittle, (xPos, yPos))

	def drawPlayGameButton(self, screen, yPos): 
		buttonWidth = self.buttonWidth
		xPos = self.width / 2 - buttonWidth / 2
		if self.startSelected == True :
			screen.blit(self.startGameSelect, (xPos, yPos))
		else : screen.blit(self.startGame, (xPos, yPos))

	def drawHelpButton(self, screen, yPos): 
		buttonWidth = self.buttonWidth
		xPos = self.width / 2 - buttonWidth / 2
		if self.helpSelected == True : 
			screen.blit(self.helpInverted, (xPos, yPos))
		else : screen.blit(self.help, (xPos, yPos))

	def drawHighScoreButton(self, screen, yPos): pass

class Text(object):
	def __init__(self, width, height):
		self.width, self.height = width, height
		self.getLevelTransitionText(width)
		self.getHelpText(width)

	def getHelpText(self, width):\
		self.helpInstruc = ['''Move the blue Paddle and attempt to finish.''',
'''Left Mouse Click on the level Screen.''',
'''Click the ball with the Paddle to begin a ''',
'''level. Hit the ball while the ball is moving ''',
'''to curve the ball. You get 4 lives Total.''',
'''Press ESC to close''',
'''Carpe Diem.''', '''aka #yolo''',]
		
	def drawHelpText(self, screen):
		width, height = self.width, self.height
		lines = 0
		for text in self.helpInstruc :
			help = pygame.font.Font(None, width / 25)
			textDiff = (self.height / 10) * lines
			textWidth, textHeight = help.size(text)
			help = help.render(text, 10, (255, 255, 255))
			xPos = width / 2 - textWidth / 2
			yPos = height / 6 + textDiff
			screen.blit(help, (xPos, yPos))
			lines += 1

	def getLevelTransitionText(self, width):
		self.getLevel1Text(width)
		self.getLevel2Text(width)
		self.getLevel3Text(width)

	def getLevel1Text(self, width):
		self.levelOneMain = 'Level 1'
		self.levelOneMessage = 'Can you last?'

	def drawLevelOneText(self, screen):
		levelOne = pygame.font.Font(None, self.width / 10)
		levelMessage = pygame.font.Font(None, self.width/ 22)
		mainWidth, mainHeight = levelOne.size(self.levelOneMain)
		messageWidth, messageHeight = levelMessage.size(self.levelOneMessage)
		levelOne = levelOne.render(self.levelOneMain, 10, (255, 255, 255))
		levelMessage = levelMessage.render(self.levelOneMessage, 10, 
							  (255, 255,255))
		mainXPos = self.width / 2 - mainWidth / 2
		mainYPos = self.height / 4
		messageXPos = self.width / 2 - messageWidth / 2
		messageYPos = self.height / 2
		screen.blit(levelOne, (mainXPos, mainYPos))
		screen.blit(levelMessage, (messageXPos, messageYPos))
		
	def getLevel2Text(self, width):
		self.levelTwoMain = 'Level 2'
		self.levelTwoMessage = 'Its About to Get Faster'

	def drawLevelTwoText(self, screen):
		levelTwo = pygame.font.Font(None, self.width / 10)
		levelMessage = pygame.font.Font(None, self.width/ 22)
		mainWidth, mainHeight = levelTwo.size(self.levelTwoMain)
		messageWidth, messageHeight = levelMessage.size(self.levelTwoMessage)
		levelTwo = levelTwo.render(self.levelTwoMain, 10, (255, 255, 255))
		levelMessage = levelMessage.render(self.levelTwoMessage, 10, 
							  (255, 255,255))
		mainXPos = self.width / 2 - mainWidth / 2
		mainYPos = self.height / 4
		messageXPos = self.width / 2 - messageWidth / 2
		messageYPos = self.height / 2
		screen.blit(levelTwo, (mainXPos, mainYPos))
		screen.blit(levelMessage, (messageXPos, messageYPos))

	def getLevel3Text(self, width):
		self.levelThreeMain = 'Level 3'
		self.levelThreeMessage = 'Can you finish?'

	def drawLevelThreeText(self, screen):
		levelThree = pygame.font.Font(None, self.width / 10)
		levelMessage = pygame.font.Font(None, self.width/ 22)
		mainWidth, mainHeight = levelThree.size(self.levelThreeMain)
		messageWidth, messageHeight = levelMessage.size(self.levelThreeMessage)
		levelThree = levelThree.render(self.levelThreeMain, 10,(255, 255, 255))
		levelMessage = levelMessage.render(self.levelThreeMessage, 10, 
							  (255, 255,255))
		mainXPos = self.width / 2 - mainWidth / 2
		mainYPos = self.height / 4
		messageXPos = self.width / 2 - messageWidth / 2
		messageYPos = self.height / 2
		screen.blit(levelThree, (mainXPos, mainYPos))
		screen.blit(levelMessage, (messageXPos, messageYPos))

Play = BlueBalls(660, 480)
Play.run()
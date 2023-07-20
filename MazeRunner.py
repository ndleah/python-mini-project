# Maze Runner
# MazeRunner.py
# Miksam Kurumbang
# mkurumba


from GraphicsProject.graphics import *
from random import randrange
from time import *

#function creates the window
#(GW)
def window():
    win = GraphWin("Maze Runner", 700, 700)
    win.setBackground("lightblue")
    win.setCoords(0, 0, 20, 20)
    return win




#function creates the timer
def Time(win,st, otherTime):
   elapsedTime = otherTime - st
   Mins = elapsedTime//60
   Secs = elapsedTime % 60
   Mins =round(Mins)
   Secs = round(Secs)
   return Mins, Secs

#function draws the timer
def drawTimer():
   Min = 0
   Secs = 0
   key = win.getKey()
   start = time()
   timer = Text(Point(10, 17), str(Min) + " : " + str(Secs))
   timer.setTextColor("black")
   timer.setSize(14)
   timer.draw(win)

   return start, timer, key




#checks if the mouse click is in a rectangle
def checkButtonClick(clickedPoint,leftLower,rightUpper):
    # gets the x and y coordinate of the leftLower point of the rectangle
    leftX = leftLower.getX()
    leftY = leftLower.getY()
    # gets the x and y coordinate of the rightUpper point of the rectangle
    rightX = rightUpper.getX()
    rightY = rightUpper.getY()
    #gets the x and y coordinate of the clickedpoint
    checkClickX = clickedPoint.getX()
    checkClickY = clickedPoint.getY()

    #checks if the mouse click is in the rectangle
    if leftX < checkClickX and rightX > checkClickX and leftY < checkClickY and rightY > checkClickY:
        return "in"
    else:
        return "out"
#draws the title
def Title():
   title = Text(Point(10, 19), "MAZE RUNNER")
   title.setStyle("bold")
   title.setSize(15)
   title.draw(win)
   return title


def playerInfo():
   #(OTXT)
   welcome = Text(Point(10, 19), "WELCOME TO MAZE RUNNER")
   welcome.setStyle("bold")
   welcome.setSize(15)
   welcome.draw(win)
   # entry box for the color
   Player = Text(Point(4.5, 15), "NAME:")
   Player.setStyle("bold")
   Player.draw(win)
   PlayerName = Entry(Point(7,15), 10)
   PlayerName.draw(win)
   # # fake button to be clicked for entering the color.
   button = Rectangle(Point(8.7, 14.5), Point(10.8, 15.5))
   button.setFill("yellow")
   buttonLabel = Text(Point(9.7, 15), "Submit")
   button.draw(win)
   buttonLabel.draw(win)
   Instructions = Text(Point(7, 10), "USE THE KEYS W,A,S,D TO MOVE")
   Instructions.setStyle("bold")
   Instructions.draw(win)



   return welcome, Player,PlayerName , button , buttonLabel, Instructions



class ball:
   def __init__(self, center,window ):

      self.circle = Circle(center, .3)

      self.circle.getCenter().getX()
      self.circle.getCenter().getY()


      self.win = window


   #draws the circle
   def draw(self, win,x,y):
      self.circle = Circle(Point(x,y), .3)
      self.circle.setFill("red")

      self.circle.draw(win)
   #function allows the ball to move
   def move(self,key):

         if key == "d":
            self.circle.move(.5, 0)
         if key == "a":
            self.circle.move(-.5, 0)
         if key == "s":
            self.circle.move(0, -.5)
         if key == "w":
            self.circle.move(0, .5)

   def getBallcenter(self):
      x = self.circle.getCenter().getX()
      y = self.circle.getCenter().getY()

      return x,y

   def undrawBall(self):
      self.circle.undraw()

   def changeColor(self):
      #(RND)
      colorsList = ["red", "cyan", "yellow", "green", "blue", "indigo", "violet"]
      colors = randrange(0, 7)
      self.circle.setFill(colorsList[colors])





#builds the walls
#(CLOD)
class Walls:

   def __init__(self,verticalStart, verticalEnd,horizontalStart, horizontalEnd):
      self.verticalStart = verticalStart
      self.verticalEnd = verticalEnd
      self.horizontalStart = horizontalStart
      self.horizontalEnd = horizontalEnd
      self.verticalLine = Line(self.verticalStart, self.verticalEnd)
      self.horizontalLine = Line(self.horizontalStart, self.horizontalEnd)


#draws the walls
   def drawWalls(self):

      self.verticalLine.setWidth(4)
      self.verticalLine.draw(win)

      self.horizontalLine.setWidth(4)
      self.horizontalLine.draw(win)

   #gets the points needed to detect the walls
   def getPoints(self):

      return self.verticalStart.getX(),self.verticalStart.getY(),self.verticalEnd.getY(),self.horizontalStart.getX(),self.horizontalStart.getY(),self.horizontalEnd.getX()
   #undraws the walls
   def undrawWalls(self):

      self.verticalLine.undraw()

      self.horizontalLine.undraw()

#used to sort names with scores
class Player:
      def __init__(self, name, score):
         self.name = name
         self.score = score

      def getScore(self):
         return self.score

def useScore(aPlayer):
   return aPlayer.getScore()

#function creates players(collects the name and the score of the player)
def makePlayers():
   #(IFL)
   inputFilename = "scorefile.txt"
   inputfile = open(inputFilename, "r")
   inputfile.readline()
   #loop makes the list of the players
   players= []
   for line in inputfile:
      l = line.split("|")
      name = l[0]
      score = l[1]
      # newScore = score.replace(" : ","")
      score.strip()
      playerScore = int(score)
      player1 = Player(name,playerScore)
      players.append(player1)
   inputfile.close()
   return players

#finds the highscore
def findHighscore(players):
   players.sort(key=useScore)
   highscore = players[0]
   return highscore





# creates the maze(hard coded)
def createMaze():
   #(CLOD)

   border = Walls(Point(1, 15), Point(1, 4), Point(1, 4), Point(19, 4))
   border2 = Walls(Point(19, 16), Point(19, 5), Point(1, 16), Point(19, 16))
   wallset1 = Walls(Point(2, 16), Point(2, 14), Point(1, 13), Point(3, 13))
   wallset2 = Walls(Point(3, 14), Point(3, 12), Point(3, 12), Point(4, 12))
   wallset3 = Walls(Point(4, 12), Point(4, 11), Point(4, 11), Point(5, 11))
   wallset4 = Walls(Point(5, 13), Point(5, 11), Point(5, 12), Point(7, 12))
   wallset5 = Walls(Point(7, 13), Point(7, 10), Point(6, 13), Point(8, 13))
   wallset6 = Walls(Point(6, 14), Point(6, 13), Point(4, 14), Point(6, 14))
   wallset7 = Walls(Point(4, 15), Point(4, 13), Point(3, 15), Point(4, 15))
   wallset8 = Walls(Point(7, 16), Point(7, 14), Point(5, 15), Point(7, 15))
   wallset9 = Walls(Point(9, 16), Point(9, 13), Point(8, 14), Point(9, 14))
   wallset10 = Walls(Point(8, 15), Point(8, 14), Point(9, 14), Point(10, 14))
   wallset11 = Walls(Point(13, 16), Point(13, 15), Point(10, 15), Point(12, 15))
   wallset12 = Walls(Point(14, 16), Point(14, 13), Point(12, 14), Point(14, 14))
   wallset13 = Walls(Point(11, 15), Point(11, 13), Point(10, 13), Point(11, 13))
   wallset14 = Walls(Point(12, 15), Point(12, 14), Point(8, 12), Point(10, 12))
   wallset15 = Walls(Point(10, 13), Point(10, 10), Point(10, 11), Point(11, 11))
   wallset16 = Walls(Point(9, 11), Point(9, 10), Point(7, 10), Point(9, 10))
   wallset17 = Walls(Point(8, 10), Point(8, 9), Point(8, 11), Point(9, 11))
   wallset18 = Walls(Point(6, 11), Point(6, 5), Point(6, 10), Point(7, 10))
   wallset19 = Walls(Point(7, 9), Point(7, 8), Point(7, 8), Point(9, 8))
   wallset20 = Walls(Point(8, 7), Point(8, 6), Point(6, 7), Point(8, 7))
   wallset21 = Walls(Point(9, 9), Point(9, 7), Point(8, 6), Point(9, 6))
   wallset22 = Walls(Point(10, 7), Point(10, 5), Point(9, 9), Point(14, 9))
   wallset23 = Walls(Point(11, 8), Point(11, 4), Point(9, 7), Point(10, 7))
   wallset24 = Walls(Point(12, 8), Point(12, 6), Point(10, 8), Point(13, 8))
   wallset25 = Walls(Point(14, 9), Point(14, 7), Point(10, 10), Point(13, 10))
   wallset26 = Walls(Point(14, 9), Point(14, 7), Point(13, 7), Point(15, 7))
   wallset27 = Walls(Point(7, 6), Point(7, 5), Point(7, 5), Point(10, 5))
   wallset28 = Walls(Point(5, 5), Point(5, 4), Point(5, 5), Point(6, 5))
   wallset29 = Walls(Point(13, 10), Point(13, 9), Point(12, 6), Point(14, 6))
   wallset30 = Walls(Point(14, 6), Point(14, 5), Point(12, 5), Point(14, 5))
   wallset31 = Walls(Point(13, 5), Point(13, 4), Point(15, 6), Point(17, 6))
   wallset32 = Walls(Point(15, 6), Point(15, 4), Point(16, 5), Point(19, 5))
   wallset33 = Walls(Point(18, 7), Point(18, 5), Point(16, 7), Point(19, 7))
   wallset34 = Walls(Point(16, 8), Point(16, 7), Point(14, 8), Point(16, 8))
   wallset35 = Walls(Point(2, 12), Point(2, 11), Point(2, 11), Point(3, 11))
   wallset36 = Walls(Point(3, 11), Point(3, 8), Point(2, 8), Point(3, 8))
   wallset37 = Walls(Point(2, 8), Point(2, 6), Point(1, 9), Point(2, 9))
   wallset38 = Walls(Point(2, 11), Point(2, 9), Point(3, 10), Point(5, 10))
   wallset39 = Walls(Point(4, 10), Point(4, 7), Point(2, 7), Point(4, 7))
   wallset40 = Walls(Point(5, 9), Point(5, 7), Point(5, 7), Point(6, 7))
   wallset41 = Walls(Point(3, 6), Point(3, 5), Point(1, 5), Point(3, 5))
   wallset42 = Walls(Point(4, 6), Point(4, 4), Point(4, 6), Point(5, 6))
   wallset43 = Walls(Point(18, 15), Point(18, 10), Point(16, 14), Point(18, 14))
   wallset44 = Walls(Point(12, 12), Point(12, 11), Point(10, 11), Point(12, 11))
   wallset45 = Walls(Point(12, 14), Point(12, 13), Point(12, 13), Point(13, 13))
   wallset46 = Walls(Point(13, 13), Point(13, 11), Point(13, 12), Point(15, 12))
   wallset47 = Walls(Point(15, 15), Point(15, 12), Point(15, 15), Point(17, 15))
   wallset48 = Walls(Point(16, 14), Point(16, 11), Point(17, 13), Point(18, 13))
   wallset49 = Walls(Point(17, 13), Point(17, 10), Point(14, 10), Point(17, 10))
   wallset50 = Walls(Point(14, 11), Point(14, 10), Point(14, 11), Point(15, 11))
   wallset51 = Walls(Point(17, 9), Point(17, 8), Point(15, 9), Point(19, 9))
   wallset52 = Walls(Point(17, 8), Point(18, 8), Point(11, 12), Point(12, 12))

   #(LOOD)
   #list of all the wall piece
   wallList= [border,border2 ,wallset1 ,wallset2 ,wallset3 ,wallset4 ,wallset5 ,wallset6 ,wallset7 ,wallset8 ,wallset9 ,wallset10 ,wallset11 ,
   wallset12 ,wallset13 , wallset14 ,wallset15 ,wallset16 ,wallset17 ,wallset18 ,wallset19 ,wallset20 ,wallset21 ,wallset22 , wallset23 ,
   wallset24 ,wallset25 ,wallset26 ,wallset27 ,wallset28 ,wallset29 ,wallset30 ,wallset31 ,wallset32 ,wallset33 ,wallset34 ,wallset35 ,
   wallset36 ,wallset37 ,wallset38 ,wallset39 ,wallset40 ,wallset41 ,wallset42 ,wallset43 ,wallset44  ,wallset45  ,wallset46  ,wallset47  ,
   wallset48  ,wallset49, wallset50, wallset51,wallset52]
   return wallList

# function detects if the circle touches the wall
def detectWalls(x,y,verticalStartX,verticalStartY, verticalEndY,horizontalStartX,horizontalStartY,horizontalEndX):

   if (x <= verticalStartX + .1 and x >= verticalStartX -.1 and verticalStartY >= y and verticalEndY <= y) or (horizontalStartX <= x and horizontalEndX >= x and y <= horizontalStartY + .1 and y >= horizontalStartY - .1):
      return True
   else:
      return False


#function checks if mouse click is inside the submit button
def checkSubmit():
   checkSubmit = "out"
   while checkSubmit != "in":
      #(IMS)
      clickedPoint = win.getMouse()
      checkSubmit = checkButtonClick(clickedPoint, button.getP1(), button.getP2())

      if checkSubmit == "in":
         welcome.undraw(), Playertext.undraw(), PlayerName.undraw(), button.undraw(), buttonLabel.undraw(), Instructions.undraw()\
         #(IEB)
         name = str(PlayerName.getText())

   return name

#function gets the points of the walls pieces
def getpointList(wallList):
   # pointList is the list if points of the walls
   pointList = []
   # for loop gets the points from the objects
   for i in range(len(wallList)):
      pointList.append(wallList[i].getPoints())
      wallList[i].drawWalls()

   return pointList

#function checks if the ball touches the maze wall
def checkWall(wallList):
   for i in range(len(wallList)):
      verticalStartX = pointList[i][0]
      verticalStartY = pointList[i][1]
      verticalEndY = pointList[i][2]
      horizontalStartX = pointList[i][3]
      horizontalStartY = pointList[i][4]
      horizontalEndX = pointList[i][5]
      touchingWall = detectWalls(x, y, verticalStartX, verticalStartY, verticalEndY, horizontalStartX,horizontalStartY, horizontalEndX)
      #if the ball touches the wall it resets the ball to the beginning positon
      if touchingWall:
         circle.undrawBall()
         circle.draw(win, 1, 15.5)
         circle.changeColor()

#checks if the ball is at the end of the maze
def checkEnd():
   if x == 19 and y == 4.5:
      return True
   return False


#draws the score button
def scoreButton():
   button = Rectangle(Point(8.8, 2), Point(11.2, 3))
   button.setFill("Yellow")
   buttonLabel = Text(Point(10, 2.5), "View Score")
   button.draw(win)
   buttonLabel.draw(win)
   return button, buttonLabel

#function switches to the score screen (undraws everything and draws the text objects for the scores)
def viewScore(name,score):
   win.getMouse()
   for wall in wallList:
      wall.undrawWalls()
   circle.undrawBall()
   title.undraw()
   scoreButton.undraw()
   scoreButtonLabel.undraw()
   timer.undraw()

   Instructions = Text(Point(10, 2), "TO QUIT PRESS Q")
   Instructions.setStyle("bold")
   Instructions.draw(win)

   previousHighscore = Text(Point(10, 13), "Highscore")
   previousHighscore.setStyle("bold")
   previousHighscore.draw(win)

   current = Text(Point(10, 16), "Current Score")
   current.setStyle("bold")
   current.draw(win)

   scoreText = Text(Point(10,15),str(name)+ "\t" +str(score) )
   scoreText.setStyle("bold")
   scoreText.draw(win)

   players = makePlayers()

   highscore = findHighscore(players)
   highscoreText = Text(Point(10, 12), str(highscore.getName())+"\t"+str(highscore.getScore()))
   highscoreText.setStyle("bold")
   highscoreText.draw(win)








if __name__=='__main__':
   #creates the window, draws the circle
   win = window()
   circle = ball(Point(1, 15.5),win)
   #(OFL)
   #opens the outfile
   outputFileName = "scorefile.txt"
   outfile = open(outputFileName, "a")
   #asks for the players info
   welcome, Playertext,PlayerName, button , buttonLabel, Instructions = playerInfo()
   #(FNC)
   #checks if submit box is clicked
   name = checkSubmit()
   #draws the title
   title = Title()
   #gets the list of the wall pieces
   wallList = createMaze()
   #gets the points of each walls and draws it
   pointList = getpointList(wallList)

   circle.draw(win,1, 15.5)
   #draws the timer
   start, timer, key = drawTimer()

   while key != "q":
      x,y= circle.getBallcenter()

      time2 = time()
      Min, Secs = Time(win, start, time2)
      #for loops that goes through every wall and compares the circles center to the wall
      checkWall(wallList)
      #if the ball is at the end of the maze the score is sent to the output file
      if checkEnd():
         score = str(timer.getText())
         newscore = score.replace(" : ","")
         playerscore = int(newscore)
         print(name, "\t |",playerscore, file=outfile)
         break

      circle.move(key)
      x, y = circle.getBallcenter()
      checkWall(wallList)
      if checkEnd():
         score = str(timer.getText())
         newscore = score.replace(" : ","")
         playerscore = int(newscore)
         print(name,"\t |",playerscore, file=outfile)
         # currentPlayer = Player(name, score)
         break

      key = win.getKey()
      #updates the timer
      timer.setText(str(Min) + " : " + str(Secs))


      circle.move(key)
      key = win.getKey()

   #creates the score button
   scoreButton, scoreButtonLabel = scoreButton()
   #switches to the score screen
   viewScore(name, playerscore)


   #loop made to wait for an input and close instantly
   while key != "q":
      key = win.getKey()




win.close()


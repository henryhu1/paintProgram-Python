#Paint Project.py

from pygame import *
from random import *
from math import *
from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import *

root=Tk()
root.withdraw() #removes the extra TK window
root.attributes("-topmost",True) #any tkinter window will be in front of every other one

size=(1200,768)
screen = display.set_mode(size) 
#=====================================================================window
display.set_caption("PokéPaint") #window name
display.set_icon(image.load("Images/icon.png")) #window icon
#=====================================================================defining the colours
RED=(255,0,0,255)
GREEN=(0,255,0,255)
BLUE=(0,0,255,255)
WHITE=(255,255,255,255)
BLACK=(0,0,0,255)

YELLOW=(247,239,5,255)
GREY=(127,127,127,255)
#=====================================================================music
mixer.init()
mixer.music.load("music/opening1.ogg")
mixer.music.play()
stopOrPlay=0 #flag variable for stopping or playing music
#=====================================================================loop variables
startingScreen = True
running = True
#=====================================================================defining RECTS in title screen
startRect=Rect(500,274,200,60)
loadFileRect=Rect(500,354,200,60)
quitRect=Rect(500,434,200,60)
#=====================================================================Loading images on title screen
title=image.load("images/title.png") #title
startingBackground=image.load("images/startingscreen.jpg") #background
startingBackground=transform.scale(startingBackground,(1200,768))
startingStart=image.load("images/startingstart.png") #start picture
startingStartHighlight=image.load("images/startingstarthighlight.png") #clicked start picture
startingOpen=image.load("images/startingopen.png") #open/load file picture
startingOpenHighlight=image.load("images/startingopenhighlight.png") #clicked load file picture
startingQuit=image.load("images/startingquit.png") #quit picture
startingQuitHighlight=image.load("images/startingquithighlight.png") #clicked quit picture
#=====================================================================blitting before the loop
screen.blit(startingBackground,(0,0))
screen.blit(title,(353,100))
#=====================================================================
#=====================================================================TITLE SCREEN LOOP
#=====================================================================
while startingScreen:
    for evt in event.get(): 
##        print(evt)
        if evt.type == QUIT: 
            startingScreen = False #Exit both loops - the starting screen, and the actual paint loop
            running = False

        if evt.type==KEYDOWN: #Enter will start up paint
            if evt.key==K_RETURN:
                startingScreen=False

    mb=mouse.get_pressed()
    mx,my=mouse.get_pos()
#=====================================================================drawing the borders for the buttons (just yellow rectangles)
    draw.rect(screen,YELLOW,Rect(496,270,208,68))
    draw.rect(screen,YELLOW,Rect(496,350,208,68))
    draw.rect(screen,YELLOW,Rect(496,430,208,68))
#=====================================================================blitting the pictures for the buttons
    screen.blit(startingStart,startRect)
    screen.blit(startingOpen,loadFileRect)
    screen.blit(startingQuit,quitRect)
#=====================================================================clicking on the rects
    if startRect.collidepoint(mx,my): #start paint
        screen.blit(startingStartHighlight,startRect) #hovering over rect
        if mb[0]==1:
            startingScreen=False
            
    if loadFileRect.collidepoint(mx,my): #try loading up a file
        screen.blit(startingOpenHighlight,loadFileRect) #hovering over rect
        if mb[0]==1:
            try:
                fname=filedialog.askopenfilename(filetypes=[("Images","*.png;*.jpg;*.jpeg")])
                loadPic=image.load(fname)
                loadPic=transform.scale(loadPic,(700,600))
            except:
                print("Loading Error")
                pass
            startingScreen=False
            
    if quitRect.collidepoint(mx,my): #completely exit the program
        screen.blit(startingQuitHighlight,quitRect) #hovering over rect
        if mb[0]==1:
            startingScreen=False
            running=False
            
    display.flip()
#=====================================================================END 
#=====================================================================
#=====================================================================Next loop

#=====================================================================initializing tools and mouse positions
toolList=["pencil","brush","eraser","line","rectangle","ellipse","polygon","spray","fill","colourpick","stamp"] #list of tools
col=BLACK #default colour is black
tool="no tool" #default tool is nothing

sx,sy=mx,my #set sx and sy to something (starting x and y position)
#setting the above values to something prevents the program from crashing
#since their used in the events, the other parts of the program will start first,
#and if sx and sy aren't defined, then the program will crash

brushRadius=20 #default brush thickness
brushSwitch=0 #flag variable for switching from paint brush to alpha paint brush

eraserThickness=20 #default eraser thickness

shapeThickness=5 #thickness of the line's and shape's sides

#argument #4 for shapes
rectArg4=shapeThickness
ellipseArg4=shapeThickness
polyArg4=shapeThickness
#each fourth argument in drawing shapes starts off as the shape thickness variable

polygonList=[] #list of vertices of the shape when creating a polygon
polygonIndex=-1 #index of polygon list starts off as -1 (nothing is inside as of this point)

sprayRadius=20 #radius of the circle for spray tool

randStamp="1" #for choosing stamps
evolution="1" #for the evolution of stamps

stampList=[1,2,3,4,5,6,7] #list for blitting stamps
stampPlacement=0 #used to place the stamps

canvasNameList=["1","2","3","4","5"] #list for the background images' numbers
canvasPicList=[] #list of the pics for the background
for name in canvasNameList: #using canvasNameList to get all of the pictures into canvasPicList
    canvasBackgroundLoad=image.load("images/canvasbackground"+name+".png")
    canvasPicList.append(canvasBackgroundLoad) #canvasPicList is only used when changing the canvas background

checkCanvasBackground=False #checking if there is a background on the canvas, used for the eraser tool
#variables used to fix the problem when the user presses undo or redo with a background
backgroundBlitUndo=0
backgroundBlitRedo='' #the reason this is an empty string is to prevent problems with changing the background, undo-ing and redo-ing right at the beginning
                      #if backgroundBlitRedo=0, there will be problems with line 782, where this variable and the len of redoList are equal from the beginning
#=====================================================================stamps: transforming and flipping pre-set values
widthScale=100 #stamp scale for width
heightScale=100 #stamp scale for height
horizontalFlip=False #stamp flipping horizontally
verticalFlip=False #stamp flipping vertically
#=====================================================================load ALL images
title=transform.scale(title,(247,70)) #transform title to fit the paint loop

wheelPic=image.load("images/colourwheel.png") #picture of colour wheel (square)

#each tool has 4 pictures (except stamp): a default pic, a hover pic, a click-and-hold pic and a selected pic
pencilPic=image.load("images/pencil.png")
pencilHover=image.load("images/pencilhover.png")
pencilClick=image.load("images/pencilclick.png")
pencilSelect=image.load("images/pencilselect.png")

brushPic=image.load("images/brush.png")
brushHover=image.load("images/brushhover.png")
brushClick=image.load("images/brushclick.png")
brushSelect=image.load("images/brushselect.png")

eraserPic=image.load("images/eraser.png")
eraserHover=image.load("images/eraserhover.png")
eraserClick=image.load("images/eraserclick.png")
eraserSelect=image.load("images/eraserselect.png")

linePic=image.load("images/line.png")
lineHover=image.load("images/linehover.png")
lineClick=image.load("images/lineclick.png")
lineSelect=image.load("images/lineselect.png")

rectanglePic=image.load("images/rectangle.png")
rectangleHover=image.load("images/rectanglehover.png")
rectangleClick=image.load("images/rectangleclick.png")
rectangleSelect=image.load("images/rectangleselect.png")

ellipsePic=image.load("images/ellipse.png")
ellipseHover=image.load("images/ellipsehover.png")
ellipseClick=image.load("images/ellipseclick.png")
ellipseSelect=image.load("images/ellipseselect.png")

polygonPic=image.load("images/polygon.png")
polygonHover=image.load("images/polygonhover.png")
polygonClick=image.load("images/polygonclick.png")
polygonSelect=image.load("images/polygonselect.png")

sprayPic=image.load("images/spray.png")
sprayHover=image.load("images/sprayhover.png")
sprayClick=image.load("images/sprayclick.png")
spraySelect=image.load("images/sprayselect.png")

fillPic=image.load("images/fill.png")
fillHover=image.load("images/fillhover.png")
fillClick=image.load("images/fillclick.png")
fillSelect=image.load("images/fillselect.png")

colourPickPic=image.load("images/colourpick.png")
colourPickHover=image.load("images/colourpickhover.png")
colourPickClick=image.load("images/colourpickclick.png")
colourPickSelect=image.load("images/colourpickselect.png")

stampSliderLeftPic=image.load("images/stampsliderleft.png")
stampSliderRightPic=image.load("images/stampsliderright.png")

textBox=image.load("images/textbox.png") #picture of defualt text box

#each 1 step tool has two pics: a normal picture, and a hover picture
clearPic=image.load("images/clear.png") 
clearHighlight=image.load("images/clearhighlight.png")
undoPic=image.load("images/undo.png")
undoHighlight=image.load("images/undohighlight.png")
redoPic=image.load("images/redo.png")
redoHighlight=image.load("images/redohighlight.png")
savePic=image.load("images/save.png")
saveHighlight=image.load("images/savehighlight.png")
openPic=image.load("images/open.png")
openHighlight=image.load("images/openhighlight.png")
stopPic=image.load("images/stop.png")
stopHighlight=image.load("images/stophighlight.png")
playPic=image.load("images/play.png")
playHighlight=image.load("images/playhighlight.png")
skipPic=image.load("images/skip.png")
skipHighlight=image.load("images/skiphighlight.png")
#=====================================================================defining all RECTS in the program
canvasRect=Rect(20,70,700,600) #for the canvas
canvasBorder=Rect(15,65,710,610) #for the canvas border

canvasBackgroundDisplayRect=Rect(20,675,700,80) #canvas background picking rect
canvasBackgroundDisplayBorder=Rect(20,675,700,80) #the border for it

canvasBackgroundRect1=Rect(40,683,100,65) #canvas background 1's rect
canvasBackgroundRect2=Rect(180,683,100,65) #canvas background 2's rect
canvasBackgroundRect3=Rect(320,683,100,65) #canvas background 3's rect
canvasBackgroundRect4=Rect(460,683,100,65) #canvas background 4's rect
canvasBackgroundRect5=Rect(600,683,100,65) #canvas background 5's rect
#when the user isn't allowed to change backgrounds
#only one background will be blit onto the canvas
#this is to prevent the eraser tool bug,
#where the user has a background, then clickes undo
#and the eraser tool still draws the blit background instead of white circles
canvasBackgroundDisplayX=Surface((100,65),SRCALPHA) #this transparent surface will appear once a background is blit

pencilRect=Rect(764,220,70,70) #for the pencil
brushRect=Rect(844,220,70,70) #for the brush
eraserRect=Rect(924,220,70,70) #for the eraser
sprayRect=Rect(1004,220,70,70) #for the spray can
fillRect=Rect(1084,220,70,70) #for the fill tool
lineRect=Rect(764,300,70,70) #for drawing lines
rectangleRect=Rect(844,300,70,70) #for drawing rectangles
ellipseRect=Rect(924,300,70,70) #for drawing ellipses
polygonRect=Rect(1004,300,70,70) #for making polygons
colourPickRect=Rect(1084,300,70,70) #for the colour picker

textRect=Rect(764,390,400,200) #for the text box

stampSliderRect=Rect(764,600,400,50) #stamp rects
stampAlpha=Surface((25,50),SRCALPHA) #the transparent surface used when hovering over the arrows
stampLeftRect=Rect(764,600,25,50) #left arrow rect
stampDisplayRect=Rect(789,600,350,50) #the rect where stamps are displayed
stampSliderRect1=Rect(789,600,50,50) #first stamp rect
stampSliderRect2=Rect(839,600,50,50) #second stamp rect
stampSliderRect3=Rect(889,600,50,50) #third stamp rect
stampSliderRect4=Rect(939,600,50,50) #fourth stamp rect
stampSliderRect5=Rect(989,600,50,50) #fifth stamp rect
stampSliderRect6=Rect(1039,600,50,50) #sixth stamp rect
stampSliderRect7=Rect(1089,600,50,50) #seventh stamp rect
stampRightRect=Rect(1139,600,25,50) #right arrow rect

wheelRect=Rect(930,5,200,200) #for the colour wheel
wheelBorder=Rect(928,4,202,202) #colour wheel border
colourSelectRect=Rect(793,130,76,38) #colour select using tkinter colour chooser

displayRect=Rect(798,40,66,66) #for the display box
displayBorder=Rect(793,35,76,76) #display box border

clearRect=Rect(350,8,40,40) #for the clear button
undoRect=Rect(400,8,40,40) #for the undo button
redoRect=Rect(450,8,40,40) #for the redo button

saveRect=Rect(500,8,40,40) #for the save file button
openRect=Rect(550,8,40,40) #for the open file button

stopPlayRect=Rect(600,8,40,40) #for the stop and play button
skipRect=Rect(650,8,40,40) #for the skip button
#=====================================================================defining list for undo and redo, plus each index
undoList=[]
redoList=[]
undoIndex=0
redoIndex=0
#=====================================================================background image
a=randint(1,4) #only used to find a random background
background=image.load("images/back"+str(a)+".png") #taking "a", turning it into a string and loading a background
background=transform.scale(background,size) #scaling the background to fit the window size
screen.blit(background,(0,0)) #blitting the background
#=====================================================================drawing and blitting before loop
screen.blit(wheelPic,wheelRect) #colour wheel
draw.rect(screen,WHITE,wheelBorder,3) #border of colour wheel
draw.rect(screen,BLACK,Rect(791,128,80,42)) #border of the tkinter colour chooser rect

draw.rect(screen,BLACK,canvasBorder) #border of canvas
draw.rect(screen,WHITE,canvasRect) #drawing canvas

draw.rect(screen,WHITE,canvasBackgroundDisplayRect) #display box for canvas backgrounds
draw.rect(screen,BLACK,canvasBackgroundDisplayBorder,5) #border of th box
draw.rect(screen,BLACK,Rect(38,681,104,69))  #\
draw.rect(screen,BLACK,Rect(178,681,104,69)) # \
draw.rect(screen,BLACK,Rect(318,681,104,69)) #  }#border of the displayed canvas backgrounds
draw.rect(screen,BLACK,Rect(458,681,104,69)) # /
draw.rect(screen,BLACK,Rect(598,681,104,69)) #/

for i in range(1,6): #blitting each possible canvas background (5 in total)
    canvasBackgroundDisplay=image.load("images/canvasbackground"+str(i)+".png")
    canvasBackgroundDisplay=transform.scale(canvasBackgroundDisplay,(100,65))
    screen.blit(canvasBackgroundDisplay,(40+(i-1)*140,683))
draw.rect(canvasBackgroundDisplayX,(127,127,127,150),Rect(0,0,100,65))

draw.rect(screen,WHITE,displayRect) #display rect for displaying tools
draw.rect(screen,BLACK,displayBorder) #border

draw.rect(screen,BLACK,Rect(348,6,44,44)) #borders of 1-step tool buttons
draw.rect(screen,BLACK,Rect(398,6,44,44))
draw.rect(screen,BLACK,Rect(448,6,44,44))
draw.rect(screen,BLACK,Rect(498,6,44,44))
draw.rect(screen,BLACK,Rect(548,6,44,44))
draw.rect(screen,BLACK,Rect(598,6,44,44))
draw.rect(screen,BLACK,Rect(648,6,44,44))

screen.blit(clearPic,clearRect) #images for 1-step tools
screen.blit(undoPic,undoRect)
screen.blit(redoPic,redoRect)
screen.blit(savePic,saveRect)
screen.blit(openPic,openRect)
if stopOrPlay%2==0:
    screen.blit(stopPic,stopPlayRect)
else:
    screen.blit(playPic,stopPlayRect)
screen.blit(skipPic,skipRect)

draw.rect(screen,WHITE,colourSelectRect) #draws a white border around colour wheel
screen.blit(image.load("images/colourselecttext.png"),colourSelectRect) #tkinter colour chooser's text in colourSelectRect

draw.rect(screen,BLACK,Rect(762,388,404,204)) #border of text box
screen.blit(textBox,textRect) #default text box at its position

draw.rect(screen,BLACK,Rect(762,598,404,54)) #border of the whole stamp slider
draw.rect(screen,WHITE,stampDisplayRect) #drawing a white background for the stamp display rect
draw.rect(stampAlpha,(127,127,127,150),Rect(0,0,25,50)) #making a transparent rect to blit over the arrows

for i in stampList: #the starting stamps to display
    i=str(i)
    stampDisplayPic=image.load("images/stamps/stamp"+i+"("+evolution+").png")
    stampDisplayPic=transform.scale(stampDisplayPic,(50,50))
    i=int(i)
    screen.blit(stampDisplayPic,(789+stampPlacement*50,600))
    stampPlacement=(stampPlacement+1)%7
#=====================================================================Title
screen.blit(title,(0,0)) #paint program title at top-left hand corner
#=====================================================================blitting the opened file from the starting screen, if any
try:
    screen.blit(loadPic,(20,70))
except:
    pass
#=====================================================================
#=====================================================================MAIN LOOP STARTS
#=====================================================================
while running:
#=====================================================================important
    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    keys=key.get_pressed()
    
    k=False #keyboard event
    click=False #mouse button clicked event
    noClick=False #mouse button released event
    
    if len(undoList)==0: #start undo with a blank screen, or whenever it becomes empty, add the white canvas being displayed
        undoList.append(screen.subsurface(canvasRect).copy())

    if mb[0]==1:
        if tool in toolList:
            if canvasRect.collidepoint(mx,my): #any updates to the canvas will reset the redo list and index
                redoList=[] #reset redo list
                redoIndex=0
#=====================================================================events
    for evt in event.get(): 
##        print(evt)
        if evt.type == QUIT: 
            running = False
#=====================================================================clicking the mouse
        if evt.type==MOUSEBUTTONDOWN:
#=====================================================================left click
            if evt.button==1:
                click=True
                downScreenshot=screen.subsurface(canvasRect).copy() #takes a screenshot when the left mouse button is clicked
                
                sx,sy=evt.pos #start position for line,rectangle and ellipse tool

                if tool=="polygon" or tool=="polygonDraw": #using the polygon tool
                    if canvasRect.collidepoint(mx,my):
                        polygonList.append((sx,sy)) #appends sx and sy into the polygon vertices list
                        polygonIndex+=1 #index increases by 1
                        tool="polygonDraw" #tool becomes polygonDraw
#=====================================================================scroll up
            if evt.button==4:

                if tool=="brush": #only if the tool is brush will its thickness change
                    if brushRadius<35:
                        brushRadius+=1

                if tool=="eraser": #only if the tool is eraser will its thickness change
                    if eraserThickness<30:
                        eraserThickness+=1

                #only if the tool is line/rectangle/ellipse/polygon will its thickness change
                if tool=="line" or tool=="rectangle" or tool=="ellipse" or tool=="polygon" or tool=="polygonDraw":
                    if shapeThickness<12:
                        shapeThickness+=1

                elif tool=="spray": #only if the tool is spray will the spray radius change
                    if sprayRadius<35:
                        sprayRadius+=1

                elif tool=="stamp":
                    if widthScale<250 and heightScale<250:
                        widthScale+=1
                        heightScale+=1
#=====================================================================scroll down
            elif evt.button==5: 

                if tool=="brush": #only if the tool is brush will its thickness change
                    if brushRadius>10:
                        brushRadius-=1

                if tool=="eraser": #only if the tool is eraser will its thickness change
                    if eraserThickness>10:
                        eraserThickness-=1

                #only if the tool is line/rectangle/ellipse/polygon will its thickness change
                if tool=="line" or tool=="rectangle" or tool=="ellipse" or tool=="polygon" or tool=="polygonDraw":
                    if shapeThickness>1:
                        shapeThickness-=1

                elif tool=="spray": #only if the tool is spray will the spray radius change
                    if sprayRadius>10:
                        sprayRadius-=1

                elif tool=="stamp":
                    if widthScale>50 and heightScale>50:
                        widthScale-=1
                        heightScale-=1
#=====================================================================stamp scrolling
            if stampSliderRect.collidepoint(mx,my): #scrolling in the stamp selector (same code as clicking the left and right arrows)
                tempStampList=[] #a temporary stamp list (it will keep going back to an empty list after stamps change)
                if evt.button==4: #scrolling up in the stampSliderRect
                    screen.subsurface(stampDisplayRect).fill(WHITE) #redrawing a white background
                    for i in stampList: #takes the elements in stampList
                        if i+1<93: #the maximum number is 92
                            tempStampList.append(i+1) #append the number to the temporary stamp list
                        else:
                            tempStampList.append(i-91) #going over 92 will make it go back to 1 and start over
                    stampList=tempStampList #making stampList equal to the temporary one. This way, the elements in stampList will directly change
                                            #using stampList to change stamps won't change it's elements (which is supposed to happen
                                            #since the stamps are changing). Using a temporary list will be able to directly change everything inside it
                elif evt.button==5: #scrolling down in stampSliderRect
                    screen.subsurface(stampDisplayRect).fill(WHITE) #redrawing a white background
                    for i in stampList: #same thing with scrolling up
                        if i-1<=0: #the minimum number is 1
                            tempStampList.append(i+91)
                        else:
                            tempStampList.append(i-1) #this will make the appended element go up to 92 if i-1<=0
                    stampList=tempStampList
                for i in stampList: #drawing the new stamps
                    i=str(i)
                    try:                    #having three "try and except" allows the stamps to be blit.
                        try:                #some Pokémon don't have evolutions that go as high as the evolution variable
                            try:            #meaning that their images won't be blit using the evolution variable
                                stampDisplayPic=image.load("images/stamps/stamp"+i+"("+evolution+").png")
                            except:
                                stampDisplayPic=image.load("images/stamps/stamp"+i+"(3).png")
                        except:
                            stampDisplayPic=image.load("images/stamps/stamp"+i+"(2).png")
                    except:
                        stampDisplayPic=image.load("images/stamps/stamp"+i+"(1).png")
                                            #it will instead try blitting the next highest evolution of the Pokémon
                    stampDisplayPic=transform.scale(stampDisplayPic,(50,50)) #transforming the stamp to fit
                    i=int(i)
                    screen.blit(stampDisplayPic,(789+stampPlacement*50,600))
                    stampPlacement=(stampPlacement+1)%7 #only 7 positions are available, this will keep the stamps from extending out of the stampSliderRect
#=====================================================================release mouse
        if evt.type==MOUSEBUTTONUP:
            if evt.button==1:
                noClick=True
                
            draw.rect(screen,WHITE,wheelBorder,3) #redraw the border of the colour wheel when the mouse button is up

            if canvasRect.collidepoint(sx,sy) or canvasRect.collidepoint(mx,my): #take a screenshot when the mouse is let go
                if tool in toolList:
                    if tool!="colourpick": #don't allow the colour picker tool to be apart of undo and redo, since it doesn't draw anything
                        if evt.button==1:
                            upScreenshot=screen.subsurface(canvasRect).copy() #takes a screenshot when the mouse isn't pressed
                            undoList.append(upScreenshot)
                            undoIndex+=1
#=====================================================================keyboard
        if evt.type==KEYDOWN:
            k=True
            if evt.key==K_c: #pressing the "c" key clears the canvas, undoList and redoList
                draw.rect(screen,WHITE,canvasRect)
                undoList=[]
                undoIndex=0
                redoList=[]
                redoIndex=0
                checkCanvasBackground=False

            if evt.key==K_RETURN: #this is used for switching between the brush and the "alphabrush"
                if tool=="brush":
                    brushSwitch+=1
                    
            if evt.key==K_UP:
                if tool=="rectangle":
                    rectArg4=shapeThickness #turns the 4th argument in the rectangle tool into shapeThickness
                elif tool=="ellipse":
                    ellipseArg4=shapeThickness #turns the 4th argument in the ellipse tool into shapeThickness
                elif tool=="polygon" or tool=="polygonDraw":
                    polyArg4=shapeThickness #turns the 4th argument in the polygon tool into shapeThickness
                    
            if evt.key==K_DOWN:
                if tool=="rectangle":
                    rectArg4=0 #turns the 4th argument in the rectangle tool into 0 (filled rectangle)
                elif tool=="ellipse":
                    ellipseArg4=0 #turns the 4th argument in the ellipse tool into 0 (filled ellipse)
                elif tool=="polygon" or tool=="polygonDraw":
                    polyArg4=0 #turns the 4th argument in the polygon tool into 0 (filled polygon)
#=====================================================================stamp keyboards
            if tool=="stamp":
                if evt.key==K_RETURN: #evolving Pokémon
                    if tool=="stamp":
                        evolution=int(evolution)+1 #add to the evolution variable
                        if evolution==5: #the reason why the max evolution is 4 is because while most Pokémon don't evolve more than twice,
                            evolution=1  #Eevee, or stamp68, has 4 different evolutions. It makes it so that while every other Pokémon has reached its max evolution,
                                         #the user will have to press enter an additional time to reset all of the Pokémon back to its basic evolution
                        evolution=str(evolution)
                        screen.subsurface(stampDisplayRect).fill(WHITE) #redrawing a white background
                        for i in stampList: #drawing the new stamps
                            i=str(i)
                            try:            #Eevee is the reason why there is three "try and except"
                                try:
                                    try:
                                        stampDisplayPic=image.load("images/stamps/stamp"+i+"("+evolution+").png")
                                    except:
                                        stampDisplayPic=image.load("images/stamps/stamp"+i+"(3).png")
                                except:
                                    stampDisplayPic=image.load("images/stamps/stamp"+i+"(2).png")
                            except:
                                stampDisplayPic=image.load("images/stamps/stamp"+i+"(1).png")
                            stampDisplayPic=transform.scale(stampDisplayPic,(50,50)) #blitting the stamps exactly as how changing stamps is
                            i=int(i)
                            evolution=str(evolution)
                            screen.blit(stampDisplayPic,(789+stampPlacement*50,600))
                            stampPlacement=(stampPlacement+1)%7
                if evt.key==K_RIGHT: #flipping the stamps
                    horizontalFlip=True
                if evt.key==K_LEFT:
                    horizontalFlip=False
                if evt.key==K_UP:
                    verticalFlip=True
                if evt.key==K_DOWN:
                    verticalFlip=False
#=====================================================================text
    if tool in toolList: #info on each tool
        if tool=="brush":
            if brushSwitch%2==0:
                toolText=image.load("images/"+tool+"1text.png")
            else:
                toolText=image.load("images/"+tool+"2text.png")
        else:
            toolText=image.load("images/"+tool+"text.png")
        screen.blit(toolText,textRect)
    elif tool=="polygonDraw":
        screen.blit(image.load("images/polygontext.png"),textRect)
    else: #no tool selected means a blank text box will appear
        screen.blit(image.load("images/textbox.png"),textRect)
#=====================================================================blitting images for 1-step tools
    screen.blit(clearPic,clearRect)    
    screen.blit(undoPic,undoRect)
    screen.blit(redoPic,redoRect)

    screen.blit(savePic,saveRect)
    screen.blit(openPic,openRect)

    if stopOrPlay%2==0: #different images when the music is stopped or played
        screen.blit(stopPic,stopPlayRect)
    else:
        screen.blit(playPic,stopPlayRect)
    screen.blit(skipPic,skipRect)

    draw.rect(screen,WHITE,colourSelectRect) #draws a white border around colour wheel
    screen.blit(image.load("images/colourselecttext.png"),colourSelectRect)

    screen.blit(stampSliderRightPic,stampRightRect) #right arrow for stamps
    screen.blit(stampSliderLeftPic,stampLeftRect) #left arrow for stamps
#=====================================================================1-step tools hovering images and text
    if clearRect.collidepoint(mx,my):
        screen.blit(clearHighlight,clearRect)
        screen.blit(image.load("images/cleartext.png"),textRect)
    if undoRect.collidepoint(mx,my):
        screen.blit(undoHighlight,undoRect)
        screen.blit(image.load("images/undotext.png"),textRect)
    if redoRect.collidepoint(mx,my):
        screen.blit(redoHighlight,redoRect)
        screen.blit(image.load("images/redotext.png"),textRect)
    if saveRect.collidepoint(mx,my):
        screen.blit(saveHighlight,saveRect)
        screen.blit(image.load("images/savetext.png"),textRect)
    if openRect.collidepoint(mx,my):
        screen.blit(openHighlight,openRect)
        screen.blit(image.load("images/opentext.png"),textRect)
    if stopPlayRect.collidepoint(mx,my):
        if stopOrPlay%2==0:
            screen.blit(stopHighlight,stopPlayRect)
            screen.blit(image.load("images/stoptext.png"),textRect)
        else:
            screen.blit(playHighlight,stopPlayRect)
            screen.blit(image.load("images/playtext.png"),textRect)
    if skipRect.collidepoint(mx,my):
        screen.blit(skipHighlight,skipRect)
        screen.blit(image.load("images/skiptext.png"),textRect)

    if colourSelectRect.collidepoint(mx,my): #the colour chooser also changes when the user hovers over it
        draw.rect(screen,GREY,colourSelectRect) #hovering over the tkinter colour chooser rect will turn the rect grey
        screen.blit(image.load("images/colourselecttext.png"),colourSelectRect)

    if canvasBackgroundDisplayRect.collidepoint(mx,my):
        screen.blit(image.load("images/canvasbackgroundtext.png"),textRect)
#=====================================================================stamp slider
#this is for changing stamps when the user clicks on the arrows, it is the exact same method as scrolling
    if stampSliderRect.collidepoint(mx,my):
        if stampRightRect.collidepoint(mx,my):
            screen.blit(stampAlpha,stampRightRect) #using the transparent surface
            if click:
                screen.subsurface(stampDisplayRect).fill(WHITE)
                for i in stampList:
                    if i+1<93:
                        tempStampList.append(i+1)
                    else:
                        tempStampList.append(i-91)
                stampList=tempStampList
        elif stampLeftRect.collidepoint(mx,my):
            screen.blit(stampAlpha,stampLeftRect)
            if click:
                screen.subsurface(stampDisplayRect).fill(WHITE)
                for i in stampList:
                    if i-1<=0:
                        tempStampList.append(i+91)
                    else:
                        tempStampList.append(i-1)
                stampList=tempStampList
        for i in stampList:
            i=str(i)
            try:
                try:
                    try:
                        stampDisplayPic=image.load("images/stamps/stamp"+i+"("+evolution+").png")
                    except:
                        stampDisplayPic=image.load("images/stamps/stamp"+i+"(3).png")
                except:
                    stampDisplayPic=image.load("images/stamps/stamp"+i+"(2).png")
            except:
                stampDisplayPic=image.load("images/stamps/stamp"+i+"(1).png")
            stampDisplayPic=transform.scale(stampDisplayPic,(50,50))
            i=int(i)
            evolution=str(evolution)
            screen.blit(stampDisplayPic,(789+stampPlacement*50,600))
            stampPlacement=(stampPlacement+1)%7
        tempStampList=[]
#=====================================================================1-step tools' functions
    if click:
        if wheelRect.collidepoint(mx,my): #selecting colour using colour palette
            col=screen.get_at((mx,my))
            draw.rect(screen,GREEN,wheelBorder,3) #border turns green for a cool effect
        if colourSelectRect.collidepoint(mx,my): #selecting colour using tkinter
            col,colString=askcolor(title="Select a Colour")
            if col==None: #if the user exits the colour selector right away
                col=BLACK

        if clearRect.collidepoint(mx,my): #clearing the canvas (also clears undo and redo list, and each index)
            draw.rect(screen,WHITE,canvasRect)
            undoList=[]
            undoIndex=0
            redoList=[]
            redoIndex=0
            checkCanvasBackground=False

        if undoRect.collidepoint(mx,my): #undo-ing
            if len(undoList)>=2:
                screen.blit(undoList[undoIndex-1],(20,70))
                undoIndex-=1
                undidImage=undoList.pop()
                redoList.append(undidImage)
                redoIndex+=1

        if redoRect.collidepoint(mx,my): #redo-ing
            if len(redoList)>=1:
                screen.blit(redoList[redoIndex-1],(20,70))
                redoIndex-=1
                redidImage=redoList.pop()
                undoList.append(redidImage)
                undoIndex+=1

        if saveRect.collidepoint(mx,my): #saving the canvas as a file
            try:
                fname=filedialog.asksaveasfilename(defaultextension=".png")
                image.save(screen.subsurface(canvasRect),fname)
            except:
                print("Saving Error")
                pass

        if openRect.collidepoint(mx,my): #opening a file
            try:
                fname=filedialog.askopenfilename(filetypes=[("Images","*.png *.jpg *.jpeg")])
                loadPic=image.load(fname)
                loadPic=transform.scale(loadPic,(700,600))
                screen.blit(loadPic,(20,70))
            except:
                print("Loading Error")
                pass

        if stopPlayRect.collidepoint(mx,my): #stopping and playing music
            stopOrPlay+=1
            if stopOrPlay%2==1:
                mixer.music.pause()
            else:
                mixer.music.unpause()

        if skipRect.collidepoint(mx,my): #"skipping" (just stopping the music so that another song will be randomly chosen) (?)
            stopOrPlay=0
            musicNum=str(randint(1,24))
            mixer.music.load("music/music"+musicNum+".ogg")
            mixer.music.play()

        #changing canvas background
        if checkCanvasBackground==False: #only if there isn't already a background will the canvasBackgroundPic variable update
            if canvasBackgroundRect1.collidepoint(mx,my): 
                canvasBackgroundPic=canvasPicList[0]
            elif canvasBackgroundRect2.collidepoint(mx,my):
                canvasBackgroundPic=canvasPicList[1]
            elif canvasBackgroundRect3.collidepoint(mx,my):
                canvasBackgroundPic=canvasPicList[2]
            elif canvasBackgroundRect4.collidepoint(mx,my):
                canvasBackgroundPic=canvasPicList[3]
            elif canvasBackgroundRect5.collidepoint(mx,my):
                canvasBackgroundPic=canvasPicList[4]
        #only when the mouse is over the canvasBackgroundRect's will the background change
            if canvasBackgroundRect1.collidepoint(mx,my) or canvasBackgroundRect2.collidepoint(mx,my) or canvasBackgroundRect3.collidepoint(mx,my) or canvasBackgroundRect4.collidepoint(mx,my) or canvasBackgroundRect5.collidepoint(mx,my):
                checkCanvasBackground=True
                for i in range(0,5):
                    screen.blit(canvasBackgroundDisplayX,(40+i*140,683))
                try: #try to blit the canvas background if there's one that's been clicked
                    canvasBackgroundPic=transform.scale(canvasBackgroundPic,(700,600))
                    screen.blit(canvasBackgroundPic,(20,70))
                    upScreenshot=screen.subsurface(canvasRect).copy() #takes a screenshot when the mouse isn't pressed
                    undoList.append(upScreenshot)
                    undoIndex+=1
                    backgroundBlitUndo=undoList.index(upScreenshot) #stores the index where the user blit the background, this will be used when the user clicks undo when there's a background
                except:
                    pass
    #these next lines of code fix the problem when the user clickes undo or redo when there's a background on the canvas
    if backgroundBlitUndo==len(undoList) or clearRect.collidepoint(mx,my) and click and checkCanvasBackground==True:
        checkCanvasBackground=False
        if len(redoList)>0:
            backgroundBlitRedo=redoList.index(redoList[-1])
        backgroundBlitUndo=0
        for i in range(1,6): #blitting each possible canvas background (5 in total)
            canvasBackgroundDisplay=image.load("images/canvasbackground"+str(i)+".png")
            canvasBackgroundDisplay=transform.scale(canvasBackgroundDisplay,(100,65))
            screen.blit(canvasBackgroundDisplay,(40+(i-1)*140,683))
    if backgroundBlitRedo==len(redoList) and len(redoList)>0 and checkCanvasBackground==False:
        for i in range(0,5):
            screen.blit(canvasBackgroundDisplayX,(40+i*140,683))
        checkCanvasBackground=True
        if len(undoList)>0:
            backgroundBlitUndo=undoList.index(undoList[-1])
        backgroundBlitRedo=0
#=====================================================================display the tool thickness and colour
    if tool=="pencil":
        screen.subsurface(displayRect).fill(WHITE)
        draw.circle(screen,col,(831,73),2)
        draw.circle(screen,BLACK,(831,73),2,1) #black circle to identify lighter colours easier

    elif tool=="brush":
        screen.subsurface(displayRect).fill(WHITE)
        draw.circle(screen,col,(831,73),brushRadius)
        draw.circle(screen,BLACK,(831,73),brushRadius,1) #black circle to identify lighter colours easier

    elif tool=="eraser":
        screen.subsurface(displayRect).fill(WHITE)
        if checkCanvasBackground:
            draw.rect(screen,BLACK,Rect(831-eraserThickness/2,73-eraserThickness/2,eraserThickness,eraserThickness),1)
        else:
            draw.circle(screen,BLACK,(831,73),eraserThickness,1) #same thing with eraser thickness, the circles being drawn fits the line better when it's smaller
        
    elif tool=="line":
        screen.subsurface(displayRect).fill(WHITE)
        draw.line(screen,col,(831,40),(831,105),shapeThickness) #displaying a line

    elif tool=="rectangle":
        screen.subsurface(displayRect).fill(WHITE)
        if rectArg4==0:
            draw.rect(screen,col,Rect(811,53,40,40)) #displaying a filled rectangle
        else:
            for rectThickness in range(1,shapeThickness+1):
                draw.rect(screen,col,Rect(811-rectThickness,53-rectThickness,40+2*rectThickness,40+2*rectThickness),1) #displaying an unfilled rectangle

    elif tool=="ellipse":
        screen.subsurface(displayRect).fill(WHITE)
        if ellipseArg4==0:
            draw.circle(screen,col,(831,73),20) #displaying a filled circle
        else:
            draw.circle(screen,col,(831,73),20+shapeThickness,shapeThickness) #displaying an unfilled ellipse

    elif tool=="polygon" or tool=="polygonDraw":
        screen.subsurface(displayRect).fill(WHITE)
        if polyArg4==0:
            draw.polygon(screen,col,[(831,50),(811,95),(851,95)]) #displaying a filled triangle (demonstrating a polygon)
        else:
            draw.polygon(screen,col,[(831,50),(811,95),(851,95)],shapeThickness) #displaying an unfilled triangle

    elif tool=="spray":
        screen.subsurface(displayRect).fill(WHITE)
        draw.circle(screen,col,(831,73),sprayRadius) #circle displaying the radius of the spray tool
        draw.circle(screen,BLACK,(831,73),sprayRadius,1) #black circle to identify lighter colours easier
        
    elif tool=="fill":
        screen.subsurface(displayRect).fill(col)

    elif tool=="colourpick":
        screen.subsurface(displayRect).fill(WHITE)
        draw.circle(screen,col,(831,73),10)
        draw.circle(screen,BLACK,(831,73),10,1) #black circle to identify lighter colours easier

    elif tool=="stamp":
        screen.subsurface(displayRect).fill(WHITE)
        displayRectStamp=transform.scale(myStamp,(66,66))
        screen.blit(displayRectStamp,displayRect)
        
    else:
        screen.subsurface(displayRect).fill(WHITE)
#=====================================================================selecting the TOOLS    
    if tool!="pencil":
        screen.blit(pencilPic,pencilRect)
        if pencilRect.collidepoint(mx,my):
            screen.blit(pencilHover,pencilRect)
            if mb[0]==1:
                if pencilRect.collidepoint(mx,my):
                    screen.blit(pencilClick,(764,221))
                    if noClick:
                        tool="pencil"
    if tool=="pencil":
        screen.blit(pencilSelect,pencilRect)

    if tool!="brush":
        screen.blit(brushPic,brushRect)
        if brushRect.collidepoint(mx,my):
            screen.blit(brushHover,brushRect)
            if mb[0]==1:
                if brushRect.collidepoint(mx,my):
                    screen.blit(brushClick,(844,221))
                    if noClick:
                        tool="brush"
    if tool=="brush":
        dx=omx-mx #horizontal distance
        dy=omy-my #vertical distance
        dist=int(sqrt(dx**2+dy**2))
        screen.blit(brushSelect,brushRect)
        if brushSwitch%2==1: #preparing the "alphabrush", or the highlighter
            col=list(col)
            col[3]=44
            col=tuple(col)
            highlightScreen=Surface((brushRadius*2,brushRadius*2),SRCALPHA)
            draw.circle(highlightScreen,col,(brushRadius,brushRadius),brushRadius)

    if tool!="eraser":
        screen.blit(eraserPic,eraserRect)
        if eraserRect.collidepoint(mx,my):
            screen.blit(eraserHover,eraserRect)
            if mb[0]==1:
                if eraserRect.collidepoint(mx,my):
                    screen.blit(eraserClick,(924,221))
                    if noClick:
                        tool="eraser"
    if tool=="eraser":
        dx=omx-mx #horizontal distance
        dy=omy-my #vertical distance
        dist=int(sqrt(dx**2+dy**2))
        screen.blit(eraserSelect,eraserRect)

    if tool!="spray":
        screen.blit(sprayPic,sprayRect)
        if sprayRect.collidepoint(mx,my):
            screen.blit(sprayHover,sprayRect)
            if mb[0]==1:
                if sprayRect.collidepoint(mx,my):
                    screen.blit(sprayClick,(1004,221))
                    if noClick:
                        tool="spray"
    if tool=="spray":
        screen.blit(spraySelect,sprayRect)

    if tool!="fill":
        screen.blit(fillPic,fillRect)
        if fillRect.collidepoint(mx,my):
            screen.blit(fillHover,fillRect)
            if mb[0]==1:
                if fillRect.collidepoint(mx,my):
                    screen.blit(fillClick,(1084,221))
                    if noClick:
                        tool="fill"
    if tool=="fill":
        screen.blit(fillSelect,fillRect)

    if tool!="line":
        screen.blit(linePic,lineRect)
        if lineRect.collidepoint(mx,my):
            screen.blit(lineHover,lineRect)
            if mb[0]==1:
                if lineRect.collidepoint(mx,my):
                    screen.blit(lineClick,(764,301))
                    if noClick:
                        tool="line"
    if tool=="line":
        screen.blit(lineSelect,lineRect)

    if tool!="rectangle":
        screen.blit(rectanglePic,rectangleRect)
        if rectangleRect.collidepoint(mx,my):
            screen.blit(rectangleHover,rectangleRect)
            if mb[0]==1:
                if rectangleRect.collidepoint(mx,my):
                    screen.blit(rectangleClick,(844,301))
                    if noClick:
                        tool="rectangle"
                        rectArg4=shapeThickness
    if tool=="rectangle":
        screen.blit(rectangleSelect,rectangleRect)

    if tool!="ellipse":
        screen.blit(ellipsePic,ellipseRect)
        if ellipseRect.collidepoint(mx,my):
            screen.blit(ellipseHover,ellipseRect)
            if mb[0]==1:
                if ellipseRect.collidepoint(mx,my):
                    screen.blit(ellipseClick,(924,301))
                    if noClick:
                        tool="ellipse"
                        ellipseArg4=shapeThickness
    if tool=="ellipse":
        screen.blit(ellipseSelect,ellipseRect)
    
    if tool!="polygon" or tool!="polygonDraw":
        screen.blit(polygonPic,polygonRect)
        if polygonRect.collidepoint(mx,my):
            screen.blit(polygonHover,polygonRect)
            if mb[0]==1:
                if polygonRect.collidepoint(mx,my):
                    screen.blit(polygonClick,(1004,301))
                    if noClick:
                        tool="polygon"
                        polyArg4=shapeThickness
    if tool=="polygon" or tool=="polygonDraw":
        screen.blit(polygonSelect,polygonRect)
    
    if tool!="colourpick":
        screen.blit(colourPickPic,colourPickRect)
        if colourPickRect.collidepoint(mx,my):
            screen.blit(colourPickHover,colourPickRect)
            if mb[0]==1:
                if colourPickRect.collidepoint(mx,my):
                    screen.blit(colourPickClick,(1084,301))
                    if noClick:
                        tempTool=tool #sets a variable to the previously selected tool
                        tool="colourpick"
    if tool=="colourpick":
        screen.blit(colourPickSelect,colourPickRect)

    if click: #this is where stamps are selected
        if stampDisplayRect.collidepoint(mx,my):
            tool="stamp"
            if stampSliderRect1.collidepoint(mx,my):
                stampNum=i-6 #i has a pre-existing value from changing the stamps, and will also be used to select stamps
                if stampNum<=0:
                    stampNum+=92
            if stampSliderRect2.collidepoint(mx,my):
                stampNum=i-5
                if stampNum<=0:
                    stampNum+=92
            if stampSliderRect3.collidepoint(mx,my):
                stampNum=i-4
                if stampNum<=0:
                    stampNum=+92
            if stampSliderRect4.collidepoint(mx,my):
                stampNum=i-3
                if stampNum<=0:
                    stampNum+=92
            if stampSliderRect5.collidepoint(mx,my):
                stampNum=i-2
                if stampNum<=0:
                    stampNum+=92
            if stampSliderRect6.collidepoint(mx,my):
                stampNum=i-1
                if stampNum<=0:
                    stampNum+=92
            if stampSliderRect7.collidepoint(mx,my):
                stampNum=i
                if stampNum<=0:
                    stampNum+=92
    if tool=="stamp":
        if click:
            stampChance=randint(1,100) #used to pick a random stamp, possibly some rare ones
        if stampChance<=96: #chance of NOT getting a rare stamp (96% chance)
            try:                            #same concept with selecting stamps as changing stamps 
                try:
                    try:
                        myStamp=image.load("images/stamps/stamp"+str(stampNum)+"("+str(evolution)+").png")
                    except:
                        myStamp=image.load("images/stamps/stamp"+str(stampNum)+"(3).png")
                except:
                    myStamp=image.load("images/stamps/stamp"+str(stampNum)+"(2).png")
            except:
                myStamp=image.load("images/stamps/stamp"+str(stampNum)+"(1).png")
            myStamp=transform.scale(myStamp,(widthScale,heightScale)) #scaling the stamp
            myStamp=transform.flip(myStamp,horizontalFlip,verticalFlip) #flipping the stamp
        else: #if the user gets a rare stamp (4% chance)
            if click:
                rareStamp=str(randint(93,155)) #this is where the rare stamp's numbers starts
                #in the images folder, under the stamps folder, stamp92 is the last common stamp, after that up to 155, there are rare stamps
                print("YOU GOT A LEGENDARY/MYTHICAL POKÉMON!!!")
                myStamp=image.load("images/stamps/stamp"+rareStamp+"(1).png")
                if canvasRect.collidepoint(mx,my) and click:
                    myStamp=transform.scale(myStamp,(widthScale,heightScale)) #scaling the stamp
                    myStamp=transform.flip(myStamp,horizontalFlip,verticalFlip) #flipping the stamp
#=====================================================================using the tools
    if canvasRect.collidepoint(mx,my):
        if mb[0]==1:
            screen.set_clip(canvasRect) #only the canvas can be "updated"
                        
            if tool=="pencil": #draws
                draw.line(screen,col,(omx,omy),(mx,my),1)

            if tool=="brush":
                if brushSwitch%2==1: #this is when the "alphabrush", or highlighter, is selected
                    if omx!=mx or omy!=my:
                        screen.blit(highlightScreen,(mx-brushRadius,my-brushRadius))
                else: #the normal brush tool
                    if mx==omx and my==omy:
                        draw.circle(screen,col,(mx,my),brushRadius)
                    for i in range(1,dist+1):
                        cx=int(omx+i*dx/dist)
                        cy=int(omy+i*dy/dist)
                        draw.circle(screen,col,(cx,cy),brushRadius)

            if tool=="eraser":
                if checkCanvasBackground:
                        if Rect(int(0.5*eraserThickness+20),int(0.5*eraserThickness+70),-1*eraserThickness+700,-1*eraserThickness+600).collidepoint(mx,my):
                        #that is the rect in which the mouse has to be contained in so that the program won't crash, since there isn't enough room to get on the canvas background picture
                        #it is directly correlated to the size of the eraser
                            eraserBackground=canvasBackgroundPic.subsurface((mx-(eraserThickness*0.5+20),my-(eraserThickness*0.5+70),eraserThickness,eraserThickness))
                            #to align the eraser with the background
                            #the eraser used a lot of linear relations, with its contained rect and aligning the non-canvas eraser
                            screen.blit(eraserBackground,(mx-eraserThickness/2,my-eraserThickness/2))
                            for i in range(1,dist+1): #same thing as brush, blitting images between omx,omy and mx,my
                                cx=int(omx+i*dx/dist)
                                cy=int(omy+i*dy/dist)
                                if int(0.5*eraserThickness+20)<cx<int(0.5*eraserThickness+20)+-1*eraserThickness+700 and int(0.5*eraserThickness+70)<cy<int(0.5*eraserThickness+70)+-1*eraserThickness+600:
                                    eraserBackgroundBetween=canvasBackgroundPic.subsurface((cx-(eraserThickness*0.5+20),cy-(eraserThickness*0.5+70),eraserThickness,eraserThickness))
                                    screen.blit(eraserBackgroundBetween,(cx-eraserThickness/2,cy-eraserThickness/2))
                else: #normal eraser
                    if mx==omx and my==omy:
                        draw.circle(screen,WHITE,(mx,my),eraserThickness)
                    for i in range(1,dist+1):
                        cx=int(omx+i*dx/dist)
                        cy=int(omy+i*dy/dist)
                        draw.circle(screen,WHITE,(cx,cy),eraserThickness)

            if tool=="spray": #spray paints
                for sprayCircle in range(1,25):
                    xStartPoint,yStartPoint=randint(mx-sprayRadius,mx+sprayRadius),randint(my-sprayRadius,my+sprayRadius)
                    if (xStartPoint-mx)**2+(yStartPoint-my)**2<=sprayRadius**2:
                        draw.circle(screen,col,(xStartPoint,yStartPoint),0)

            if tool=="fill": #fills canvas
                screen.subsurface(canvasRect).fill(col)

            if tool=="line": #creates lines
                screen.blit(downScreenshot,(20,70))
                draw.line(screen,col,(sx,sy),(mx,my),shapeThickness)

            if tool=="rectangle": #creates rectangles
                screen.blit(downScreenshot,canvasRect)
                if rectArg4!=0:
                    rectArg4=shapeThickness #refreshes the thickenss for drawing rectangles
                    for rectThickness in range(1,shapeThickness+1): #using a for loop to draw multiple rectangles to make unfilled rectangles thicker
                        draw.rect(screen,col,(min(mx,sx)-rectThickness,min(my,sy)-rectThickness,max(mx,sx)-min(mx,sx)+2*rectThickness,max(my,sy)-min(my,sy)+2*rectThickness),1)
                else:
                    draw.rect(screen,col,Rect(sx,sy,mx-sx,my-sy)) #a filled rectangle

            if tool=="ellipse": #creates ellipses
                if ellipseArg4!=0:
                    ellipseArg4=shapeThickness #refreshes the thickenss for drawing ellipses
                screen.blit(downScreenshot,(20,70))
                if ellipseArg4*2>=max(mx,sx)-min(mx,sx) or ellipseArg4*2>=max(my,sy)-min(my,sy):
                    draw.line(screen,col,(sx,sy),(mx,my),ellipseArg4)
                else:
                    draw.ellipse(screen,col,(min(mx,sx),min(my,sy),max(mx,sx)-min(mx,sx),max(my,sy)-min(my,sy)),ellipseArg4)


            if tool=="colourpick": #gets colour
                col=screen.get_at((mx,my))
                if noClick:
                    tool=tempTool #sets the tool back to the previous tool

            if tool=="stamp":
                screen.blit(downScreenshot,(20,70))
                screen.blit(myStamp,(mx-widthScale/2,my-heightScale/2))

            screen.set_clip(None) #modify everything

    omx,omy=mx,my

    if tool=="polygonDraw": #draws polygons/shapes
        if canvasRect.collidepoint(mx,my):
            screen.set_clip(canvasRect)    #this tool has a different mechanism than the other tools
                                           #since it draws lines freely without left-clicking
            screen.blit(downScreenshot,(20,70))

            startX,startY=polygonList[0] #set a tuple to be the first index in the list "polygon"
            startRect=Rect(startX-10,startY-10,20,20) #creating a 20x20 Rect around the first coordinates of polygon

            if polyArg4!=0: #used to determine if the polygon will be filled or not
                polyArg4=shapeThickness

            draw.line(screen,col,polygonList[polygonIndex],(mx,my),shapeThickness)

            if startRect.collidepoint(mx,my) and len(polygonList)>=3: #if the mouse cursor is in the startRect, the mouse will snap to the first coordinate of the polygon
                draw.line(screen,col,polygonList[polygonIndex],polygonList[0],shapeThickness)
                mouse.set_pos([startX,startY])

                if (mx,my)==(startX,startY) and mb[0]==1: #when the final side of the polygon has been drawn - 

                    draw.polygon(screen,col,polygonList,polyArg4) #for filling the polygon

                    polygonList=[]                                #everything resets
                    polygonIndex=-1
                    tool="polygon"
    
        else: #if the mouse leaves the canvas, then the polygon will stop from being drawn, but the lines that were already drew stay on the canvas
            polygonList=[]
            polygonIndex=-1
            tool="polygon"
            undoList.append(screen.subsurface(canvasRect).copy())
            undoIndex+=1
        
        screen.set_clip(None)
#=====================================================================music
    #if mixer.music.get_busy()!=0 and stopOrPlay%2!=0:   #if there isn't any music playing, (?)
    #    musicNum=str(randint(1,24)) #then a new song will be chosen
    #    mixer.music.load("music/music"+musicNum+".ogg")
    #    mixer.music.play()
#=====================================================================
    display.flip() 
quit() # closes out pygame window

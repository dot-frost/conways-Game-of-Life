#!/usr/bin/python3

import random

import pygame

from EventListener import EventListener
from Game import Game
from settings import *


def rectClicked(event , rect):
    if event.button != 1 :
        return
    x, y = event.pos
    xStart , yStart = rect.topleft
    xStop , yStop = rect.bottomright
    return (x in range(xStart, xStop+1)) & (y in range(yStart, yStop+1))


game = Game(WINDOW_SIZE,FPS)

BOARD_ROWS = WINDOW_SIZE[1] // CELL_SIZE
BOARD_COLS = WINDOW_SIZE[0] // CELL_SIZE

game.addEventListener(pygame.QUIT, EventListener(lambda event: game.quit()))

def onPressEscape(event):
    if event.key != pygame.K_ESCAPE:
        return
    if game.status == game.MAIN_MENU:
        game.quit()
        return
    if game.status == game.PLAY_MODE:
        game.status = game.DRAW_MODE
        return
    game.status = game.MAIN_MENU

game.addEventListener(pygame.KEYUP, EventListener(onPressEscape))


font = pygame.font.Font(pygame.font.match_font('ubuntu'), (WINDOW_SIZE[1] // 100)*7)

# Create Buttun
def createButton(text):
    BUTTON_WIDTH = (WINDOW_SIZE[0] // 100) * 40
    BUTTON_HEIGHT = (BUTTON_WIDTH // 100) * 35
    Button = pygame.Surface((BUTTON_WIDTH,BUTTON_HEIGHT))
    Button.fill('black')
    pygame.draw.polygon(Button, 'red', [(0,0), (BUTTON_WIDTH,0), (BUTTON_WIDTH,BUTTON_HEIGHT), (0,BUTTON_HEIGHT)] , (WINDOW_SIZE[0] // 100)*2)
    Text = font.render(text, True, 'white')
    TextRect = Text.get_rect(center=(BUTTON_WIDTH//2,BUTTON_HEIGHT//2))
    Button.blit(Text, TextRect)
    return Button

# Main Menu
mainMenu = pygame.Surface(WINDOW_SIZE)
mainMenu.fill('gray')


### Start Button
startButton = createButton('Start')
startButtonRect = startButton.get_rect(center=(WINDOW_SIZE[0]//2,(WINDOW_SIZE[1]//100)*30))

mainMenu.blit(startButton, startButtonRect)

def startButtonCliked(event):
    if game.status == game.MAIN_MENU and rectClicked(event, startButtonRect):
       game.status = game.DRAW_MODE

game.addEventListener(pygame.MOUSEBUTTONDOWN, EventListener(startButtonCliked))
### End Start Button

### Quit Buttun

quitButton = createButton('Quit')
quitButtonRect =  quitButton.get_rect(center=(WINDOW_SIZE[0]//2,(WINDOW_SIZE[1]//100)*60))

mainMenu.blit(quitButton, quitButtonRect)
def quitButtonCliked(event):
    if game.status == game.MAIN_MENU and rectClicked(event, quitButtonRect):
       game.quit()

game.addEventListener(pygame.MOUSEBUTTONDOWN, EventListener(quitButtonCliked))
### End Quit Button
def billitToDisplay(surface,rect):
    if game.status == game.MAIN_MENU:
        game.blit(surface, rect)

game.add(billitToDisplay, [mainMenu, (0,0)])

# End MainMenu



universe = [[0 for j in range(BOARD_COLS)] for i in range(BOARD_ROWS)]


board = pygame.Surface(WINDOW_SIZE)

block = pygame.Surface((CELL_SIZE,CELL_SIZE))
block.fill('blue')

pygame.draw.polygon(block, 'black', ([1,1], [1,CELL_SIZE-2],[CELL_SIZE-2,CELL_SIZE-2],[CELL_SIZE-2,1]), 1)

def RunGame():
    if game.status != game.PLAY_MODE:
        return

    Renderboard()

    universeTemp = [[ct for ct in rt] for rt in universe]

    for rowIndex, row in enumerate(universeTemp):
        for colIndex, col in enumerate(row):
            if col != 1:
                continue

            countAlive = 0
            for i in range(-1,2):
                for j in range(-1,2):
                    newROW = rowIndex + i
                    newCOl = colIndex + j
                    
                    if newROW < 0 or newROW > (BOARD_ROWS - 1) or newCOl < 0 or newCOl > (BOARD_COLS - 1) or (newROW == rowIndex and newCOl == colIndex):
                        continue

                    if universeTemp[newROW][newCOl] == 1:
                        countAlive+=1
                        continue

                    countAliveAroundDead = 0
                    for iD in range(-1,2):
                        for jD in range(-1,2):
                            newROWD = newROW + iD
                            newCOlD = newCOl + jD
                            
                            if newROWD < 0 or newROWD > (BOARD_ROWS - 1) or newCOlD < 0 or newCOlD > (BOARD_COLS - 1) or (newROWD == newROW and newCOlD == newCOl):
                                continue

                            if universeTemp[newROWD][newCOlD] == 1:
                                countAliveAroundDead+=1
                                continue

                    if countAliveAroundDead == 3:
                        universe[newROW][newCOl] = 1
            
            if col == 1 and (countAlive > 3 or countAlive < 2):
                universe[rowIndex][colIndex] = 0
                continue
                
            if countAlive == 3:
                universe[rowIndex][colIndex] = 1


def Renderboard():
    if game.status == game.MAIN_MENU:
        return

    board.fill('black')
    for rowIndex, row in enumerate(universe):
        for colIndex, col in enumerate(row):
            if universe[rowIndex][colIndex] == 1:
                board.blit(block, ((CELL_SIZE-1) * colIndex + 1 * colIndex , (CELL_SIZE-1) * rowIndex + 1 * rowIndex))
    game.blit(board, (0,0))


def boardClicked(event):
    if event.button != 1 or game.status == game.MAIN_MENU:
        return
    game.draw_status = True
    boardDrow(event)
    


def boardNotClicked(event):
    if event.button != 1 or game.status == game.MAIN_MENU:
        return
    game.draw_status = False

def boardDrow(event):
    if game.status == game.MAIN_MENU or game.draw_status == False:
        return
    x , y = event.pos
    row = y//CELL_SIZE
    col = x//CELL_SIZE
    if (row < BOARD_ROWS and col < BOARD_COLS):
        universe[row][col] = 1

def boardEraze(event):
    if event.button != 3 or game.status == game.MAIN_MENU:
        return
    x , y = event.pos
    row = y//CELL_SIZE
    col = x//CELL_SIZE
    if (row < BOARD_ROWS and col < BOARD_COLS):
        universe[row][col] = 0

def setModePlay(event):
    if event.key == 13:
        game.status = game.PLAY_MODE

game.addEventListener(pygame.MOUSEBUTTONDOWN, EventListener(boardEraze))
game.addEventListener(pygame.MOUSEBUTTONDOWN, EventListener(boardClicked))
game.addEventListener(pygame.MOUSEBUTTONUP, EventListener(boardNotClicked))
game.addEventListener(pygame.MOUSEMOTION, EventListener(boardDrow))
game.addEventListener(pygame.KEYDOWN, EventListener(setModePlay))

def drawMode():
    if game.status != game.DRAW_MODE:
        return
    
    Renderboard()

game.add(drawMode)
game.add(RunGame)

game.play()

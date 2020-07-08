import sys
import pygame
import random
import numpy as np
import math
import time
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((1040, 800))
pygame.display.set_caption("gomoku")
screen.fill((250, 250, 250))
background = pygame.image.load("bg.png")
black = pygame.image.load("black.png")
white = pygame.image.load("white.png")
f1 = pygame.image.load("f1.png")
f1p = (864, 388)
f2 = pygame.image.load("f2.png")
f2p = (842, 398)
f3 = pygame.image.load("f3.png")
f3p = (819, 365)
f4 = pygame.image.load("f4.png")
f4p = (864, 388)
restart = pygame.image.load("restart.png")
talk = pygame.image.load("talk.png")
frame = pygame.image.load("frame.png")

playNow = 1
table = np.zeros((15, 15))
win = 0
text = "Hi, I'm gomoku!"

# the first step by computer
theFirstOneI = math.floor(random.random() * 15)
theFirstOneJ = math.floor(random.random() * 2)
table[theFirstOneI][theFirstOneJ] = 1
playNow = 2
prevWhite = [theFirstOneI, theFirstOneJ]
prevBlack = [theFirstOneI, theFirstOneJ]

# draw the screen, should be called after each iteration
def draw():
    screen.fill((250, 250, 250))
    screen.blit(background, (26, 26))
    screen.blit(frame, (810, 300))
    global text
    if(prevWhite == [theFirstOneI, theFirstOneJ]):
        screen.blit(f1, f1p)
        screen.blit(talk, (788, 150))
    elif(win == 0):
        screen.blit(f4, f4p)
        text = ""
    elif(win == 1):
        screen.blit(f2, f2p)
        screen.blit(talk, (788, 150))
        text = "     You lose!"
        screen.blit(restart, (835, 550))
    elif(win == 2):
        screen.blit(f3, f3p)
        screen.blit(talk, (788, 150))
        text = "     You win!"
        screen.blit(restart, (835, 550))
    else:
        screen.blit(f1, f1p)
        screen.blit(talk, (788, 150))
        text = "        Draw!"
        screen.blit(restart, (835, 550))
    for i in range(15):
        for j in range(15):
            if(table[i][j] == 1):
                screen.blit(black, (29 + 50 * j, 29 + 50 * i))
            elif(table[i][j] == 2):
                screen.blit(white, (29 + 50 * j, 29 + 50 * i))
    head_font = pygame.font.SysFont(None, 40)
    text_surface = head_font.render(text, True, (0, 0, 0))
    screen.blit(text_surface, (805, 197))
    pygame.display.update()

def checkWin(player, i, j):
    count = 1
    global win
    for x in range(1, 5):
        if (i - x >= 0 and table[i - x][j] == player):
            count += 1
        else:
            break
    for x in range(1, 5):
        if (i + x < 15 and table[i + x][j] == player):
            count += 1
        else:
            break
    if (count >= 5):
        win = player
        return
    count = 1
    for x in range(1, 5):
        if (j - x >= 0 and table[i][j - x] == player):
            count += 1
        else:
            break
    for x in range(1, 5):
        if (j + x < 15 and table[i][j + x] == player):
            count += 1
        else:
            break
    if (count >= 5):
        win = player
        return
    count = 1
    for x in range(1, 5):
        if (i - x >= 0 and j - x >= 0 and table[i - x][j - x] == player):
            count += 1
        else:
            break
    for x in range(1, 5):
        if (i + x < 15 and j + x < 15 and table[i + x][j + x] == player):
            count += 1
        else:
            break
    if (count >= 5):
        win = player
        return
    count = 1
    for x in range(1, 5):
        if (i - x >= 0 and j + x < 15 and table[i - x][j + x] == player):
            count += 1
        else:
            break
    for x in range(1, 5):
        if (i + x < 15 and j - x >= 0 and table[i + x][j - x] == player):
            count += 1
        else:
            break
    if (count >= 5):
        win = player
        return

# the evaluation function
def checkScore(player, i, j):
    sum = 0
    count = [1, 1, 1, 1]
    flag = [[0, 0], [0, 0], [0, 0], [0, 0]]
    open = [0, 0, 0, 0]
    for x in range(1, 5):
        if(i - x >= 0 and flag[0][0] == 0):
            if(table[i - x][j] == player):
                count[0] += 1
            elif(table[i - x][j] == 0):
                open[0] += 1
                flag[0][0] = 1
            else:
                flag[0][0] = 1
        if(i + x < 15 and flag[0][1] == 0):
            if(table[i + x][j] == player):
                count[0] += 1
            elif(table[i + x][j] == 0):
                open[0] += 1
                flag[0][1] = 1
            else:
                flag[0][1] = 1
        if(j - x >= 0 and flag[1][0] == 0):
            if(table[i][j - x] == player):
                count[1] += 1
            elif(table[i][j - x] == 0):
                open[1] += 1
                flag[1][0] = 1
            else:
                flag[1][0] = 1
        if(j + x < 15 and flag[1][1] == 0):
            if(table[i][j + x] == player):
                count[1] += 1
            elif(table[i][j + x] == 0):
                open[1] += 1
                flag[1][1] = 1
            else:
                flag[1][1] = 1
        if(i - x >= 0 and j - x >= 0 and flag[2][0] == 0):
            if(table[i - x][j - x] == player):
                count[2] += 1
            elif(table[i - x][j - x] == 0):
                open[2] += 1
                flag[2][0] = 1
            else:
                flag[2][0] = 1
        if(i + x < 15 and j + x < 15 and flag[2][1] == 0):
            if(table[i + x][j + x] == player):
                count[2] += 1
            elif(table[i + x][j + x] == 0):
                open[2] += 1
                flag[2][1] = 1
            else:
                flag[2][1] = 1
        if(i - x >= 0 and j + x < 15 and flag[3][0] == 0):
            if(table[i - x][j + x] == player):
                count[3] += 1
            elif(table[i - x][j + x] == 0):
                open[3] += 1
                flag[3][0] = 1
            else:
                flag[3][0] = 1
        if(i + x < 15 and j - x >= 0 and flag[3][1] == 0):
            if(table[i + x][j - x] == player):
                count[3] += 1
            elif(table[i + x][j - x] == 0):
                open[3] += 1
                flag[3][1] = 1
            else:
                flag[3][1] = 1
    for x in range(4):
        if(count[x] >= 5):
            sum += 1000000
        elif(count[x] == 4):
            if(open[x] == 2):
                sum += 5000
            elif(open[x] == 1):
                sum += 300
            else:
                sum += 50
        elif(count[x] == 3):
            if(open[x] == 2):
                sum += 300
            elif(open[x] == 1):
                sum += 50
            else:
                sum += 10
        elif(count[x] == 2):
            if(open[x] == 2):
                sum += 50
            else:
                sum += 10
        else:
            sum += 10
    return sum


draw()
while (1):
    for event in pygame.event.get():
        if (event.type == QUIT):
            pygame.quit()
            sys.exit()
        elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and playNow == 2 and not win):
            x, y = event.pos[0], event.pos[1]
            if (x >= 25 and x <= 775 and y >= 25 and y <= 775):
                x = (x - 25) // 50
                y = (y - 25) // 50
                if (table[y][x] == 0):
                    prevWhite = [y, x]
                    table[y][x] = 2
                    playNow = 1
                    checkWin(2, y, x)
            draw()
        elif (event.type == MOUSEBUTTONDOWN and event.button == 1 and win):
            x, y = event.pos[0], event.pos[1]
            if(x >= 835 and x <= 973 and y >= 550 and y <= 612):
                playNow = 1
                table = np.zeros((15, 15))
                win = 0
                text = ""
                theFirstOneI = math.floor(random.random() * 15)
                theFirstOneJ = math.floor(random.random() * 2)
                table[theFirstOneI][theFirstOneJ] = 1
                playNow = 2
                prevWhite = [7, 2]
                prevBlack = [theFirstOneI, theFirstOneJ]
            draw()
    if (playNow == 1 and not win):
        # minimax search
        maxScore = -2147483647
        maxScore1 = 0
        maxPos = []
        possible0 = []
        possible1 = []
        for i in range(15):
            for j in range(15):
                if (table[i][j] == 0):
                    possible0.append([i, j, (prevBlack[0] - i) ** 2 + (prevBlack[1] - j) ** 2])
                    possible0.append([i, j, (prevWhite[0] - i) ** 2 + (prevWhite[1] - j) ** 2])
                    possible1.append([i, j, (prevBlack[0] - i) ** 2 + (prevBlack[1] - j) ** 2])
                    possible1.append([i, j, (prevWhite[0] - i) ** 2 + (prevWhite[1] - j) ** 2])
        possible0 = sorted(possible0, key=lambda s: s[2])
        possible1 = sorted(possible1, key=lambda s: s[2])
        for i in range(min(150, len(possible0))):
            score0 = checkScore(1, possible0[i][0], possible0[i][1])
            table[possible0[i][0]][possible0[i][1]] = 1
            maxScore1 = -2147483647
            for j in range(min(150, len(possible1))):
                if (table[possible1[j][0]][possible1[j][1]] == 0):
                    score1 = checkScore(2, possible1[j][0], possible1[j][1])
                    if(score1 > maxScore1):
                        maxScore1 = score1
            if (score0 - maxScore1 > maxScore):
                maxScore = score0 - maxScore1
                maxPos = [possible0[i][0], possible0[i][1]]
            table[possible0[i][0]][possible0[i][1]] = 0
        if(not maxPos):
            win = 3
        else:
            prevBlack = [maxPos[0], maxPos[1]]
            pygame.display.update()
            table[maxPos[0]][maxPos[1]] = 1
            playNow = 2
            checkWin(1, maxPos[0], maxPos[1])
        draw()

import sys
import os
import PySimpleGUI as sg
# import tkinter as tk
from threading import Thread
from time import sleep
from pygame import mixer
import mancala

def start(gMode):
    sg.theme("DarkGrey12")
    layout = []
    layout.append([sg.VPush()])
    [layout.append([]) for i in range(0, 3)]
    [layout[1].append(sg.Button("0", key=f"comp:{i+6}", pad=5, size=(5,3), button_color=("white", "darkRed"), font=('Arial', 15))) for i in range(6, 0, -1)]
    layout[2].append(sg.Button("0", key='comp:13', size=(5,3), button_color=("white", "darkRed"), font=('Arial', 15)))
    layout[2].append(sg.Text("Player's Turn", font=('Arial', 20, 'bold'), text_color="springGreen3", pad=(70,0)))
    layout[2].append(sg.Button("0", key='player:6', size=(5,3), button_color=("white", "green"), font=('Arial', 15)))
    [layout[3].append(sg.Button("0", key=f"player:{i}", pad=5, size=(5,3), button_color=("white", "green"), font=('Arial', 15))) for i in range(0, 6)]


    layout.append([sg.Text("", font=('Arial', 30, 'bold'), text_color='gold')])
    layout.append([sg.Button("New Game", key='-newGame-', size=(10, 1), font=('Arial', 15, 'bold'), visible=False)])
    layout.append([sg.VPush()])

    window = sg.Window("Mancala", layout, size=(1000,1000), finalize=True, element_padding=(0,20), element_justification='c')

    # Fill guiBoard for convenience
    guiBoard = []
    [guiBoard.append(layout[3][i]) for i in range(0, 6)]
    guiBoard.append(layout[2][-1])
    [guiBoard.append(layout[1][i]) for i in range(5, -1, -1)]
    guiBoard.append(layout[2][0])


    def sfx(s):
        mixer.init()
        mixer.music.load(f'{s}.mp3')
        mixer.music.play()

    def newGame():
        return mancala.Mancala(gMode)

    def updateGuiBoard():
        for i in range(0, len(guiBoard)):
            game.getCell(i)
            guiBoard[i].update(f"{game.getCell(i)}")

    def animateMove(ind, amt, game, isPlayer):
        pOtherSide = {0:12, 1:11, 2:10, 3:9, 4:8, 5:7}
        cOtherSide = {12:0, 11:1, 10:2, 9:3, 8:4, 7:5}

        time = .5
        board = []
        [board.append(b) for b in game.board]

        guiBoard[ind].update(button_color = ('black', 'white'))
        sleep(time)
        if ind < 7:
            guiBoard[ind].update("0", button_color = ('white', 'green'))
        else:
            guiBoard[ind].update("0", button_color = ('white', 'darkRed'))

        j = ind
        for i in range(ind+1, ind+amt+1):
            j += 1
            if isPlayer:
                if i in [13, 27, 41, 55, 69]:
                    j += 1    # Skip Computer's bank
            else:
                if i in [6, 20, 34, 48, 62]:
                    j += 1    # Skip Player's bank
            btnNum = guiBoard[j%14].get_text()
            guiBoard[j%14].update(f"{int(btnNum) + 1}",button_color = ('black', 'white'))
            if j%14 == 6:
                sfx('positive')
                sleep(time+.5)
            elif j%14 == 13:
                sfx('negative')
                sleep(time+.5)
            else:
                sfx('move')
                sleep(time) # 1 second pauses in between

            
            if j % 14 < 7:
                guiBoard[j%14].update(button_color = ('white', 'green'))
            else:
                guiBoard[j%14].update(button_color = ('white', 'darkRed'))
        
        if j % 13 != 0:
            changed = False
            if j > 13:
                j -= 1
                changed = True
            print(j, guiBoard[j%13].get_text(), j%14)
            if isPlayer:
                print("Animate Capture: ", int(guiBoard[j%13].get_text()) == 1, (j+1 if changed else j) not in [6, 20, 34, 48, 62], j%14 < 6, int(guiBoard[pOtherSide[j%6]].get_text()) != 0)
            else:
                if j % 13 > 6:
                    print("Animate Capture: ", int(guiBoard[j%13].get_text()) == 1, (j+1 if changed else j) not in [13, 27, 41, 55, 69], j%14 > 6, int(guiBoard[cOtherSide[j%13]].get_text()) != 0)
            if isPlayer and int(guiBoard[j%13].get_text()) == 1 and (j+1 if changed else j) not in [6, 20, 34, 48, 62] and j%14 < 6 and board[pOtherSide[j%6]] != 0:
                guiBoard[j%13].update(button_color = ('white', 'gold'))
                guiBoard[pOtherSide[j%13]].update( button_color = ('white', 'gold'))
                guiBoard[6].update(f"{1+board[pOtherSide[j%13]] + board[6]}", button_color=('white', 'gold'))
                sfx('capture')
                sleep(time)
                guiBoard[j%13].update("0", button_color = ('white', 'green'))
                guiBoard[pOtherSide[j%13]].update("0", button_color = ('white', 'darkRed'))
                guiBoard[6].update(button_color=('white', 'green'))
            elif not isPlayer and j % 13 > 6:
                if int(guiBoard[j%13].get_text()) == 1 and (j+1 if changed else j) not in [13, 27, 41, 55, 69] and j%14 > 6 and int(guiBoard[cOtherSide[j%13]].get_text()) != 0:
                    guiBoard[j%13].update(button_color = ('white', 'gold'))
                    guiBoard[cOtherSide[j%13]].update( button_color = ('white', 'gold'))
                    guiBoard[13].update(f"{1+board[cOtherSide[j%14]] + board[13]}", button_color=('white', 'gold'))
                    sfx('negCapture')
                    sleep(time)
                    guiBoard[j%13].update("0", button_color = ('white', 'darkRed'))
                    guiBoard[cOtherSide[j%13]].update("0", button_color = ('white', 'green'))
                    guiBoard[13].update(button_color=('white', 'darkRed'))
            if changed:
                j += 1
    """
                    P                    C
    0  1  2  3  4  5  6  7  8  9  10 11 12 13
    14 15 16 17 18 19 20 21 22 23 24 25 26 27
    28 29 30 31 32 33 34 35 36 37 38 39 40 41
    """
        
    game = newGame()

    playerTurn = True
    gameOver = False

    ind = 0
    amt = 0
    locked = False

    updateGuiBoard()
    while True:
        if not gameOver:
            if playerTurn:
                print("\n\033[1;32mPlayer's Turn\033[00m")
                layout[2][1].update("Player's Turn", font=('Arial', 20, 'bold'), text_color='springGreen3')
                event, values = window.read()
                if event == None:
                    return
                elif event == 'afterAnimate':
                    extraTurn = game.playerMove(ind, amt)
                    gameOver = game.isGameOver()
                    updateGuiBoard()
                    if not extraTurn:
                        playerTurn = False
                        sleep(1) # pause between turn switch
                        window.write_event_value('compPick', '0')
                    locked = False
                elif event != '-newGame-' and not locked:
                    locked = True
                    ent, ind = event.split(":")
                    amt = int(window[event].get_text())
                    ind = int(ind)
                    print(ent, ind, amt)
                    if ind < 6 and amt != 0:
                        window.start_thread(lambda: animateMove(ind, amt, game, True), ('afterAnimate'))
                    else:
                        locked = False
            else:
                print("\n\033[1;31mComputer's  Turn\033[00m")
                layout[2][1].update("Computer's  Turn", font=('Arial', 16, 'bold'), text_color='tomato2')
                event, values = window.read()
                if event == 'compPick':
                    ind, amt = game.compPick()
                    window.start_thread(lambda: animateMove(ind, amt, game, False), ('afterAnimate'))
                elif event == 'afterAnimate':
                    extraTurn = game.computerMove(ind, amt)
                    gameOver = game.isGameOver()
                    updateGuiBoard()
                    if not extraTurn:
                        playerTurn = True
                    else:
                        window.write_event_value('compPick', '0')
        else:
            print("Game Over")
            layout[5][0].update(visible = True)
            if game.board[6] > game.board[13]:
                layout[4][0].update("You Win!", text_color='gold')
                sfx('winner')
            else:
                layout[4][0].update("Computer Won. :(", text_color='tomato2')
                sfx('lose')
            event, values = window.read()
            if event == None:
                return
            elif event == '-newGame-':
                game = newGame()
                gameOver = False
                playerTurn = True
                updateGuiBoard()
                layout[5][0].update(visible = False)
                layout[4][0].update("")


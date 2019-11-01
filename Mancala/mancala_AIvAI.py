"""
Created on Mon Sep 30 2019

@author: Yuxuan He
"""

from tkinter import *
from random import randint
import GameAI_no_pruning, GameAI
import time
import numpy as np

# player 0 plays red (bottom part of the board)
# player 1 plays green (upper part of the board),

root = Tk()

noOfBases = 2
# set who's the first player
# whoseTurnInitial = randint(0,1)
# whoseTurn = whoseTurnInitial
whoseTurn = 1 # uncomment if u want first player to always start

smallFieldsArray = []
basesArray = []
buttonIDs = [0,1,2,3,4,5,6,7,8]

playerNo0Starts = 0
playerNo1Starts = 0
playerNo0Wins = 0
playerNo1Wins = 0
numberOfGames = 0
play = True

if (whoseTurn == 0):
    playerNo0Starts += 1
else :
    playerNo1Starts += 1

def disableButtons():
    val = 2 if whoseTurn == 0 else 1
    for i in range(0, 6):
        smallFieldsArray[6*val - (i+1)].config(state='disabled')
        if(smallFieldsArray[i + 6*whoseTurn]['text'] != '0'):
            smallFieldsArray[i + 6*whoseTurn].config(state='normal')

# check if the game is over. If it is, transfer the remaining pebbles to the correct player
def checkIfEnd():
    counter = 0
    for i in range(0,6):
        if (smallFieldsArray[i]['text'] != '0'):
            break
        else:
            counter = counter + 1
    # game is over, tranfer pebbles to player 1
    if (counter == 6):
        for i in range(6, 12):
            basesArray[1]['text'] = str(int(basesArray[1]['text']) + int(smallFieldsArray[i]['text']))
        for i in range(0,12):
            smallFieldsArray[i].config(state='disabled', text='0')
        return True
    else:
        counter = 0
        for i in range(6,12):
            if (smallFieldsArray[i]['text'] != '0'):
                break
            else:
                counter = counter + 1
        # game if over, transfer pebbles to player 0
        if (counter == 6):
            for i in range(0, 6):
                basesArray[0]['text'] = str(int(basesArray[0]['text']) + int(smallFieldsArray[i]['text']))
            for i in range(0,12):
                smallFieldsArray[i].config(state='disabled', text='0')
            return True
    return False

# function for checking if the total ammount of pebles (correctness check)
def checkSum():
    suma = 0
    for i in range(0, 12):
        suma = suma + int(smallFieldsArray[i]['text'])
    for i in range(0,2):
        suma = suma + int(basesArray[i]['text'])

def increaseButtonValue(button):
    temp_value = int(button['text'])
    button.config(text = str(temp_value+1))

    # if the field the last pebble goes into is empty, and it belongs to the player
    # that currently has his turn, check if the opposite field is not empty
    # if it is not empty, then steal the pebbles
def checkForEmptyField(button, buttonIndex):
    temp_value = int(button['text'])
    oppositeFieldIndex = 11 - buttonIndex
    temp_opposite_value = int(smallFieldsArray[oppositeFieldIndex]['text'])
    if (temp_value == 0 and temp_opposite_value != 0):
        for  i in range(0,  temp_opposite_value +1 ):
            increaseButtonValue(basesArray[whoseTurn])
        smallFieldsArray[oppositeFieldIndex].config(text = "0")
    else:
        increaseButtonValue(button)

def buttonClick(button, buttonID):

    global whoseTurn, playerNo0Wins, playerNo1Wins, numberOfGames, play
    value = int(button['text'])
    button.config(text="0")
    startingIndex = int(buttonID)+1
    i = int(buttonID)+1
    while (i < int(buttonID)+value+1):
        # check if the points need to be inserted into left base
        if(startingIndex == 6 and whoseTurn == 0):
            increaseButtonValue(basesArray[0])
            # check if the point inserted into the base was the last pebble.
            # if so, give the same  player another turn (else instruction)
            if (i+1 < int(buttonID)+value+1):
                increaseButtonValue(smallFieldsArray[startingIndex])
            else:
                whoseTurn = -1 * whoseTurn + 1
            startingIndex = startingIndex + 1
            i = i + 2
        # check if the points need to be inserted into rigth base
        elif(startingIndex == 12 and whoseTurn == 1):
            increaseButtonValue(basesArray[1])
            # check if the point inserted into the base was the last pebble.
            # if so, give the same  player another turn (else instruction)
            if (i+1 < int(buttonID)+value+1):
                increaseButtonValue(smallFieldsArray[0])
            else:
                whoseTurn = -1 * whoseTurn + 1
            i = i+2
            startingIndex = 1
        # reset counting at the right side
        elif(startingIndex == 12):
            startingIndex = 0

        # check for stealing
        else:
            if( i+1 == int(buttonID)+value+1 and (startingIndex < 6 and whoseTurn == 0 or startingIndex > 5 and whoseTurn == 1)):
                    checkForEmptyField(smallFieldsArray[startingIndex], startingIndex)

        # increase the field value normally
            else:
                increaseButtonValue(smallFieldsArray[startingIndex])
            startingIndex = startingIndex + 1
            i = i+1

    whoseTurn = -1 * whoseTurn + 1
    disableButtons()

    #checkSum()
    if(checkIfEnd()):
        numberOfGames += 1
        if (int(basesArray[0]['text']) > int(basesArray[1]['text'])):
            playerNo0Wins += 1
            print("player 0 wins")
        elif (int(basesArray[0]['text']) < int(basesArray[1]['text'])):
            playerNo1Wins += 1
            print("player 1 wins")
        else:
            print("DRAW")
        if numberOfGames == 100:
            print("Player 0 wins: ", playerNo0Wins)
            print("Player 1 wins: ", playerNo1Wins)
            print("Draws: ", 100 - playerNo0Wins - playerNo1Wins)
            print("Player 0 starts: ", playerNo0Starts)
            print("Player 1 starts: ", playerNo1Starts)
            play = False
        else :
            print("Game number: ", numberOfGames + 1)
            resetBoard(smallFieldsArray, basesArray)

    return

def setupBoard():
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[0], 0)))
    smallFieldsArray[0].grid(row=2, column=0+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[1], 1)))
    smallFieldsArray[1].grid(row=2, column=1+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[2], 2)))
    smallFieldsArray[2].grid(row=2, column=2+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[3], 3)))
    smallFieldsArray[3].grid(row=2, column=3+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[4], 4)))
    smallFieldsArray[4].grid(row=2, column=4+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="red", command=lambda: buttonClick(smallFieldsArray[5], 5)))
    smallFieldsArray[5].grid(row=2, column=5+1)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[6], 6)))
    smallFieldsArray[6].grid(row=0, column=9-3)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[7], 7)))
    smallFieldsArray[7].grid(row=0, column=8-3)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[8], 8)))
    smallFieldsArray[8].grid(row=0, column=7-3)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[9], 9)))
    smallFieldsArray[9].grid(row=0, column=6-3)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[10], 10)))
    smallFieldsArray[10].grid(row=0, column=5-3)
    smallFieldsArray.append(Button(root, text="4", height = 5,  width = 10, fg="green", command=lambda: buttonClick(smallFieldsArray[11], 11)))
    smallFieldsArray[11].grid(row=0, column=4-3)
    for i in range(0, noOfBases):
        basesArray.append(Button(root, text="0", height = 10, width = 10, fg="blue", state='disabled'))
    basesArray[0].grid(row=0, column=7, rowspan=3)
    basesArray[1].grid(row=0, column=0, rowspan=3)

def resetBoard(smallFieldsArray, basesArray):
    global playerNo0Starts,  playerNo1Starts, whoseTurn
    for field in smallFieldsArray:
        field['text'] = 4
    for base in basesArray:
        base['text'] = 0
    whoseTurn = randint(0,1)
    #whoseTurn = 0 # uncomment if u want first player to always start
    if whoseTurn == 0:
        playerNo0Starts += 1
    else:
        playerNo1Starts += 1
    return


## start the game
setupBoard()
disableButtons()
# pass a value to change the search tree depth
MinMaxAI_1 = GameAI.AI(5) #insert a depth value
MinMaxAI_2 = GameAI.AI(7)
MinMaxAI_3 = GameAI_no_pruning.AI(7)

start = time.time()

while (play):
    root.update_idletasks()
    root.update()

    if(whoseTurn == 0):
        choice = MinMaxAI_2.makeDecision(smallFieldsArray, basesArray, whoseTurn)
    #    choice = MinMaxAI_3.makeDecision(smallFieldsArray, basesArray, whoseTurn) # can only play as player 0!
    #    choice = randint(0,6)
        #print(choice)
        buttonClick(smallFieldsArray[choice], choice)
        # if you want to print the board after each step in cmd, uncomment the codes below
        # but it will take a little more time for each step.
        # result=np.zeros(12)
        # for i in range(12):
        #     result[i]=int(smallFieldsArray[i]['text'])
        # store_result=np.zeros(2)
        # store_result[0]=int(basesArray[0]['text'])
        # store_result[1]=int(basesArray[1]['text'])
        # print('player0')
        # print("------------------------")
        # print("  ", end="")
        # print(*["%2d" % x for x in reversed(result[6:])], sep="|")
        # print("%2d------------------%2d" % (store_result[1], store_result[0]))
        # print("  ", end="")
        # print(*["%2d" % x for x in result[0:6]], sep="|")
        # print("------------------------")
        # time.sleep(0.5)
    if(not play): break

    if(whoseTurn == 1):
    #    choice = MinMaxAI_2.makeDecision(smallFieldsArray, basesArray, whoseTurn)
        choice = randint(0,5)
        choice += 6  #very important!!!
        #print(choice)
        buttonClick(smallFieldsArray[choice], choice)
        # if you want to print the board in cmd after each step, uncomment the codes below
        # but it will take a little more time for each step.
        # result=np.zeros(12)
        # for i in range(12):
        #     result[i]=int(smallFieldsArray[i]['text'])
        # store_result=np.zeros(2)
        # store_result[0]=int(basesArray[0]['text'])
        # store_result[1]=int(basesArray[1]['text'])
        # print('player1')
        # print("------------------------")
        # print("  ", end="")
        # print(*["%2d" % x for x in reversed(result[6:])], sep="|")
        # print("%2d------------------%2d" % (store_result[1], store_result[0]))
        # print("  ", end="")
        # print(*["%2d" % x for x in result[0:6]], sep="|")
        # print("------------------------")
        # time.sleep(0.5)
end = time.time()
print(end-start)
#a = int(smallFieldsArray[4]['text'])

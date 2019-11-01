from random import randint
import numpy as np
class AI:

    def __init__(self, maxTreeDepth):
        self.maxTreeDepth = maxTreeDepth

    def extractGameState(self, smallFieldsArray, basesArray, whoseTurn):
        gameFields_temp = []
        gameFields = []
        for i in range(0, 14):
            if i < 6:
                gameFields_temp.append(int(smallFieldsArray[i]['text']))
            elif i == 6:
                gameFields_temp.append(int(basesArray[0]['text']))
            elif i < 13:
                gameFields_temp.append(int(smallFieldsArray[i-1]['text']))
            elif i == 13:
                gameFields_temp.append(int(basesArray[1]['text']))
        if(whoseTurn == 0):
            gameFields = gameFields_temp
        # if it is player 1 turn then invert the board
        # (the algorithm only knows how to play from one side)
        else:
            for i in range(7,14):
                gameFields.append(gameFields_temp[i])
            for i in range(0,7):
                gameFields.append(gameFields_temp[i])
        return gameFields

    def move(self, gameFields, choice):
        whoseTurn = 0
        if choice > 5:
            whoseTurn = 1

        startingIndex = choice + 1
        i = choice + 1
        value = gameFields[choice]
        gameFields[choice] = 0

        # increment correct fields
        while(i < choice+1+value):

            # skip the base of the opponent
            if(whoseTurn == 0 and startingIndex != 13):
                gameFields[startingIndex] += 1
            elif(whoseTurn == 1 and startingIndex != 6):
                gameFields[startingIndex] += 1
            else:
                if(whoseTurn == 0):
                    startingIndex = 0
                    gameFields[startingIndex] += 1
                else:
                    startingIndex += 1
                    gameFields[startingIndex] += 1
            i += 1
            startingIndex += 1

            oppositeIndex = 13 - startingIndex
            # check if a current player gets to make another move
            if(i == choice+1+value and ((whoseTurn == 0 and startingIndex-1 == 6) or (whoseTurn == 1 and startingIndex-1 == 13))):
                continue
            # check if a "steal" occures
            elif(i == choice+1+value and gameFields[oppositeIndex] != 0 and gameFields[startingIndex-1]-1 == 0 and((whoseTurn == 0 and startingIndex-1 < 6) or (whoseTurn == 1 and startingIndex-1 > 6 and startingIndex-1 < 13))):
                if(whoseTurn == 0):
                    gameFields[6] += gameFields[oppositeIndex] + 1
                    gameFields[startingIndex-1] = 0
                    gameFields[oppositeIndex] = 0
                else :
                    gameFields[13] += gameFields[oppositeIndex] + 1
                    gameFields[startingIndex-1] = 0
                    gameFields[oppositeIndex] = 0
                whoseTurn = -1 * whoseTurn + 1
            elif(i == choice+1+value):
                whoseTurn = -1 * whoseTurn + 1

            # reset counting of field increment
            if(startingIndex == 14):
                startingIndex = 0

            # calculate game field if the end-game was reached (not sure if it works correctly)
            if(gameFields[0] == 0 and gameFields[1] == 0 and gameFields[2] == 0 and gameFields[3] == 0 and gameFields[4] == 0 and gameFields[5] == 0):
                gameFields[13] = gameFields[13] + gameFields[7] + gameFields[8] + gameFields[9] + gameFields[10] + gameFields[11] + gameFields[12]
                for i in range(7, 13):
                    gameFields[i] = 0
                break

            elif(gameFields[7] == 0 and gameFields[8] == 0 and gameFields[9] == 0 and gameFields[10] == 0 and gameFields[11] == 0 and gameFields[12] == 0):
                gameFields[6] = gameFields[6] + gameFields[0] + gameFields[1] + gameFields[2] + gameFields[3] + gameFields[4] + gameFields[5]
                for i in range(0, 6):
                    gameFields[i] = 0
                break

        return gameFields, whoseTurn

    def findBestMove(self, gameFields, whoseTurn, searchtreeDepth, numberOfAnalyzedStates, alpha, beta):
        v = 0
        noOfAvailableMoves = 6
        numberOfAnalyzedStates[0] += 1
        moveScore = []
        startingField = 0
        endingField = 6
        temp_gameFields = gameFields[:]
        whoseTurnAtCurrentDepth = whoseTurn

        if (whoseTurn == 1):
            startingField = 7
            endingField = 13
            v = beta
        else :
            v = alpha

        gameEnd = self.checkForGameEnd(temp_gameFields)
        # terminate at this depth
        if(searchtreeDepth == self.maxTreeDepth or gameEnd != 0):
            if (gameEnd == 1):
                return temp_gameFields[6] - temp_gameFields[13] + sum(temp_gameFields[7:12])
            elif (gameEnd == 2):
                return temp_gameFields[6] - temp_gameFields[13] - sum(temp_gameFields[0:5])
            else:
                return temp_gameFields[6] - temp_gameFields[13]
        else:
            # try out each possible move
            for i in range(startingField, endingField):
                temp_gameFields = gameFields[:]

                # check for pruning
                if(whoseTurnAtCurrentDepth == 0 and v > beta):
                    break
                elif whoseTurnAtCurrentDepth == 1 and v < alpha :
                    break

                if(temp_gameFields[i] == 0):
                    moveScore.append(temp_gameFields[6] - temp_gameFields[13])
                    continue
                else:
                    # calculate the state resulting from current move
                    temp_gameFields, whoseTurn = self.move(temp_gameFields, i)

                    # call the function recursively (advance in depth - DFS)
                    moveScore.append(self.findBestMove(temp_gameFields, whoseTurn, searchtreeDepth+1, numberOfAnalyzedStates,  alpha, beta))

                    # update alpha and beta values
                    if(whoseTurnAtCurrentDepth == 0) :
                        if( moveScore[-1] > v):
                            v = moveScore[-1]
                        alpha = max(moveScore)
                    elif (whoseTurnAtCurrentDepth == 1):
                        if (moveScore[-1] < v):
                            v = moveScore[-1]
                        beta = min(moveScore)

        # return the most optimal move
        if searchtreeDepth == 0:
            moveScore = np.asarray(moveScore)
            # using random tie-breaking
            maxScore = np.random.choice(np.flatnonzero(moveScore == moveScore.max()))
            # choosing the first argument that has max value
            while(gameFields[maxScore] == 0):
                # if a field with 0 pebbles was chosen, choose another time
                moveScore[maxScore] = -100
                maxScore = np.random.choice(np.flatnonzero(moveScore == moveScore.max()))
            return maxScore

        # return score in case of a max node
        if(whoseTurnAtCurrentDepth == 0):
            if not moveScore:
                return 50
            else:
                return max(moveScore)

        # return score in case of a min node
        if(whoseTurnAtCurrentDepth == 1):
            if not moveScore:
                return -50
            else:
                return min(moveScore)

    def makeDecision(self, smallFieldsArray, basesArray, whoseTurn):
        searchtreeDepth = 0
        # extract an array of fields from the current state
        gameFields = self.extractGameState(smallFieldsArray, basesArray, whoseTurn)
        whoseTurn = 0

        # analyzed states counter
        numberOfAnalyzedStates = []
        numberOfAnalyzedStates.append(0)
        #  pruning
        alpha = -50
        beta = 50

        # call the function finding the most optimal move
        choice = self.findBestMove(gameFields, whoseTurn, searchtreeDepth, numberOfAnalyzedStates, alpha, beta)
        return choice

    def checkForGameEnd(self, gameFields):
        playerOne = True
        playerTwo = True

        for i in range(0, 6):
            if gameFields[i] > 0:
                playerOne = False
        if (playerOne):
            return 1

        for i in range(7, 13):
            if gameFields[i] > 0:
                playerTwo = False
        if (playerTwo):
            return 2

        return 0

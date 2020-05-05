import sys
import json
import heapq
import collections

'''_BLACK_START_SQUARES = [(0,7), (1,7),   (3,7), (4,7),   (6,7), (7,7),
                        (0,6), (0,6),   (3,6), (4,6),   (6,6), (7,6)]'''
'''_WHITE_START_SQUARES = [(0,1), (0,1),   (3,1), (4,1),   (6,1), (7,1),
                        (0,1), (0,1),   (3,0), (4,0),   (6,0), (7,0)]'''

_BLACK_START_SQUARES = [(3,7),(4,7)]
_WHITE_START_SQUARES = [(1,1),(6,1)]


testBlack = [(3,7),(4,7)]
testWhite = [(1,1),(6,1)]

class SquareBoard:
    def __init__ (self,horizon,vertical,black,white):
        self.horizon = horizon
        self.vertical =  vertical
        self.opponenttokens = black
        self.owntokens = white

    def onTheBoard(self,position):
        (x,y) = position
        return 0 <= x < self.horizon and 0 <= y < self.vertical

    def occupiedByBlack(self,position):
        return position not in self.opponenttokens

    def occupiedByWhite(self,position):
        return position not in self.owntokens

    def validMove(self,position,stack,colour):
        (x,y) = position
        #validmove = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
        directions = [-1,1]
        validmove = [(-1,-1)]
        #print(list(validmove))

        while stack > 0:
            for direction in directions:
                validmove.append((x + direction*stack, y))
                validmove.append((x, y + direction*stack))
            stack = stack - 1

        validmove = filter(self.onTheBoard,validmove)
        if colour:
            validmove = filter(self.occupiedByBlack,validmove)
        else:
            validmove = filter(self.occupiedByWhite,validmove)


        # If move = (-1,-1) ,it means bomb
        temp = list(validmove).copy()
        temp.append((-1,-1))
        return temp


    def gameOver(self):
        if(len(self.opponenttokens) == 0 or len(self.owntokens) == 0 ):
            return True
        else:
            return False


def detectStack(list):
    if len(set(list)) == len(list):
        return False
    else:
        return True


def createDic(list):
    dictStack = {}

    for coor in list:
        if dictStack.__contains__(coor):
            dictStack[coor] += 1
        else:
            dictStack[coor] = 1

    return dictStack


def getDuplicateIndex(list,coor ):
    temp = []
    index = 0

    for element in list:
        if element == coor:
            temp.append(index)
        index += 1
    return temp

def getinformat(boardgame,positionList,colour):
    dictionary = {}

    for coor in positionList:
        if colour:
            dictionary[coor] = boardgame.owntokens.count(coor)
        else:
            dictionary[coor] = boardgame.opponenttokens.count(coor)

    list = []

    for key in dictionary.keys():
        temp = 0
        while(temp < dictionary[key]):

            list.append(key)

            temp += 1

    return list


def recoverFormat(input):
    new = list(set(input)).copy()
    return new

def main():

    boardgame = SquareBoard(8,8, _BLACK_START_SQUARES.copy(),_WHITE_START_SQUARES.copy())

    alphaBeta(testWhite, testBlack,boardgame)






def alphaBeta(white,black,boardgame):

    alpha = -1000
    beta = 1000

    #boardgame = SquareBoard(8,8,black.copy(),white.copy())
    Player = True

    #Make sure depth == maxdepth
    depth = 3
    maxdepth = 3

    #print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")


    print("start\n")
    startmove = (-1,-1)

    # All possible move inside
    #   Movemomen
    possibleMovement = {}

    # The best value
    value = alphaBetaCore(boardgame,depth,alpha,beta,Player,startmove,possibleMovement,white,black,maxdepth)


    print("finish\n")
    print(f"A-B result is {value}")
    print(f"THE MOVEMENT is {possibleMovement}")



def alphaBetaCore(boardgame,depth,alpha,beta,Player,move,possibleMovement,Owntokens,Opponentokens,maxdepth):


    #Test only return
    if depth == 0:


        return len(list(set(getBoomResult(getboomArea(move),boardgame.opponenttokens))))\
         - len(list(set(getBoomResult(getboomArea(move),boardgame.owntokens))))


    if Player:
        Owntokens = getinformat(boardgame,Owntokens,True)
        maxvalue = -1000


        #Stack part if doesnt work please delete this if
        if detectStack(Owntokens):

            dictStack = createDic(Owntokens)
            # Key is the position of stacks
            for key in dictStack.keys():
                if dictStack[key] > 1:

                    temp = dictStack[key]
                    stackdeep = dictStack[key]

                    while (stackdeep > 0):

                        for move in boardgame.validMove(key,temp,True):
                            if(not boardgame.onTheBoard(move)):

                                tempsquarelist = Owntokens.copy()
                                tempsquarelistB = Opponentokens.copy()
                                owntokensBefore = boardgame.owntokens.copy()
                                opponenttokenBefore = boardgame.opponenttokens.copy()


                                tempsquare = tempsquarelist[maxindex]


                                newOwntokens, newOpponentokens = updateboomresult(tempsquare,Owntokens.copy(),Opponentokens.copy())
                                boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,newOpponentokens,maxdepth)
                                maxvalue = max(maxvalue,value)


                                #Store the possible movement
                                if depth == maxdepth and value >= maxvalue:
                                        possibleMovement[("Bomb",tempsquare)] = value


                                alpha = max(alpha,maxvalue)

                                if beta <= alpha:
                                    # Undo the movment
                                    Owntokens = tempsquarelist
                                    Opponentokens = tempsquarelistB
                                    boardgame.owntokens = owntokensBefore
                                    boardgame.opponenttokens = opponenttokenBefore
                                    break


                                Owntokens = tempsquarelist
                                Opponentokens = tempsquarelistB
                                boardgame.owntokens = owntokensBefore
                                boardgame.opponenttokens = opponenttokenBefore
                                stackdeep = 0


                            else:


                                tempsquareList = Owntokens.copy()
                                tempsquare = key


                                indexOwntokens = getDuplicateIndex(tempsquareList,key)[:stackdeep]
                                for index in indexOwntokens:
                                   Owntokens[index] = move

                                boardindex = getDuplicateIndex(boardgame.owntokens,key)[:stackdeep]
                                for index in boardindex:
                                    boardgame.owntokens[index] = move

                                newOwntokens = recoverFormat(Owntokens)
                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,Opponentokens,maxdepth)
                                maxvalue = max(maxvalue,value)

                                #Store the possible movement
                                if depth == maxdepth and value >= maxvalue:
                                    if boardgame.onTheBoard(move):
                                        possibleMovement[("MOVE",stackdeep,tempsquare,move)] = value


                                alpha = max(alpha,maxvalue)


                                if beta <= alpha:
                                    # Undo the movment
                                    for index in indexOwntokens:
                                        Owntokens[index] = key
                                    for index in boardindex:
                                        boardgame.owntokens[index] = key
                                    break

                                for index in indexOwntokens:
                                    Owntokens[index] = key

                                for index in boardindex:
                                    boardgame.owntokens[index] = key

                        stackdeep -= 1

        # No stack part
        maxindex = 0


        #Check the owntoken required no stack
        for square in Owntokens:

            maxindex2 = 0


            for move in boardgame.validMove(square,1,True):

                #Copy the white in the tempsquare
                if(not boardgame.onTheBoard(move)):

                    tempsquarelist = Owntokens.copy()
                    tempsquarelistB = Opponentokens.copy()
                    owntokensBefore = boardgame.owntokens.copy()
                    opponenttokenBefore = boardgame.opponenttokens.copy()


                    tempsquare = tempsquarelist[maxindex]


                    newOwntokens, newOpponentokens = updateboomresult(tempsquare,Owntokens.copy(),Opponentokens.copy())
                    boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,newOpponentokens,maxdepth)
                    maxvalue = max(maxvalue,value)

                    if depth == maxdepth and value >= maxvalue:
                            possibleMovement[("Bomb",tempsquare)] = value
                    alpha = max(alpha,maxvalue)
                    if beta <= alpha:
                        # Undo the movment
                        Owntokens = tempsquarelist
                        Opponentokens = tempsquarelistB
                        boardgame.owntokens = owntokensBefore
                        boardgame.opponenttokens = opponenttokenBefore
                        break


                    Owntokens = tempsquarelist
                    Opponentokens = tempsquarelistB
                    boardgame.owntokens = owntokensBefore
                    boardgame.opponenttokens = opponenttokenBefore

                else:


                    tempsquarelist = Owntokens.copy()
                    tempsquare = tempsquarelist[maxindex]


                    #Update White
                    Owntokens[maxindex]= move

                    #Find the moved owntokens in the board
                    tempOwni = boardgame.owntokens.index(tempsquare)
                    boardgame.owntokens[tempOwni] = move



                    newOwntokens = recoverFormat(Owntokens)
                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,Opponentokens,maxdepth)

                    if depth == maxdepth and value >= maxvalue:
                        if boardgame.onTheBoard(move):
                            possibleMovement[("MOVE",1,tempsquare,move)] = value

                    maxvalue = max(maxvalue,value)



                    alpha = max(alpha,maxvalue)


                    if beta <= alpha:
                        # Undo the movment
                        Owntokens[maxindex]= tempsquare
                        boardgame.owntokens[tempOwni] = tempsquare
                        break


                    # Undo the movment
                    Owntokens[maxindex]= tempsquare
                    boardgame.owntokens[tempOwni] = tempsquare

                maxindex2 = maxindex2 + 1


            maxindex = maxindex + 1

        return maxvalue

    else:


        Opponentokens = getinformat(boardgame,Opponentokens,False)

        minvalue = +1000


        #Stack part if doesnt work please delete this if
        if detectStack(Opponentokens):

            dictStack = createDic(Opponentokens)
            # Key is the position of stacks
            for key in dictStack.keys():
                if dictStack[key] > 1:
                    temp = dictStack[key]


                    stackdeep = dictStack[key]
                    while (stackdeep > 0):


                        for move in boardgame.validMove(key,temp,False):


                            if(not boardgame.onTheBoard(move)):

                                tempsquarelist = Owntokens.copy()
                                tempsquarelistB = Opponentokens.copy()
                                owntokensBefore = boardgame.owntokens.copy()
                                opponenttokenBefore = boardgame.opponenttokens.copy()


                                tempsquare = tempsquarelist[minindex]


                                newOwntokens, newOpponentokens = updateboomresult(tempsquare,Owntokens.copy(),Opponentokens.copy())
                                boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,newOpponentokens,maxdepth)
                                minvalue = min(minvalue,value)
                                beta = min(beta,minvalue)

                                if beta <= alpha:
                                    # Undo the movment
                                    Owntokens = tempsquarelist
                                    Opponentokens = tempsquarelistB
                                    boardgame.owntokens = owntokensBefore
                                    boardgame.opponenttokens = opponenttokenBefore
                                    break

                                Owntokens = tempsquarelist
                                Opponentokens = tempsquarelistB
                                boardgame.owntokens = owntokensBefore
                                boardgame.opponenttokens = opponenttokenBefore
                                stackdeep = 0

                            else:

                                tempsquareList = Opponentokens.copy()
                                tempsquare = key


                                indexOpponentokens = getDuplicateIndex(tempsquareList,key)[:stackdeep]

                                for index in indexOpponentokens:
                                   Opponentokens[index] = move

                                boardindex = getDuplicateIndex(boardgame.opponenttokens,key)[:stackdeep]


                                for index in boardindex:
                                    boardgame.opponenttokens[index] = move


                                newOpponentokens = recoverFormat(Opponentokens)
                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,Owntokens,newOpponentokens,maxdepth)
                                minvalue = min(minvalue,value)
                                beta = min(beta,minvalue)


                                if beta <= alpha:
                                    # Undo the movment
                                    for index in indexOpponentokens:
                                        Opponentokens[index] = key
                                    for index in boardindex:
                                        boardgame.opponenttokens[index] = key
                                    break

                                for index in indexOpponentokens:
                                    Opponentokens[index] = key

                                for index in boardindex:
                                    boardgame.opponenttokens[index] = key

                        stackdeep -= 1

        minindex = 0
        for square in Opponentokens:

            minindex2 = 0

            for move in boardgame.validMove(square,1,False):

                if(not boardgame.onTheBoard(move)):

                    tempsquarelist = Owntokens.copy()
                    tempsquarelistB = Opponentokens.copy()
                    owntokensBefore = boardgame.owntokens.copy()
                    opponenttokenBefore = boardgame.opponenttokens.copy()


                    tempsquare = tempsquarelist[minindex]


                    newOwntokens, newOpponentokens = updateboomresult(tempsquare,Owntokens.copy(),Opponentokens.copy())
                    boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,newOwntokens,newOpponentokens,maxdepth)
                    minvalue = min(minvalue,value)
                    beta = min(beta,minvalue)

                    if beta <= alpha:
                        # Undo the movment
                        Owntokens = tempsquarelist
                        Opponentokens = tempsquarelistB
                        boardgame.owntokens = owntokensBefore
                        boardgame.opponenttokens = opponenttokenBefore
                        break

                    Owntokens = tempsquarelist
                    Opponentokens = tempsquarelistB
                    boardgame.owntokens = owntokensBefore
                    boardgame.opponenttokens = opponenttokenBefore

                else:

                    #Copy the black in the tempsquare
                    tempsquarelist = Opponentokens.copy()
                    tempsquare = tempsquarelist[minindex]


                    #Update black
                    Opponentokens[minindex]= move

                    #Find the moved owntokens in the board
                    tempOppi = boardgame.opponenttokens.index(tempsquare)
                    boardgame.opponenttokens[tempOppi] = move

                    newOpponentokens = recoverFormat(Opponentokens)
                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,possibleMovement,Owntokens,newOpponentokens,maxdepth)
                    minvalue = min(minvalue,value)


                    beta = min(beta,minvalue)

                    if beta <= alpha:
                        # Undo the movment
                        Opponentokens[minindex]= tempsquare
                        boardgame.opponenttokens[tempOppi] = tempsquare
                        break
                    # Undo the movment
                    Opponentokens[minindex]= tempsquare
                    boardgame.opponenttokens[tempOppi] = tempsquare
                minindex2 = minindex2 + 1
            minindex = minindex + 1

        return minvalue



def getSumToken(token):
    sumnumber=0
    for i in token:
            sumnumber+=i[0]
    return sumnumber
def getCoor(token):
    coor=[]
    for i in token:
        for x in range (i[0]):
            coor.append((i[1],i[2]))
    return coor

def isEmpty(cor,coor):
    if (cor in coor):
        return False
    else:
        return True

def CoorIsValid(coor):
    if (coor[0]>=0 and coor[0]<=7):
        if (coor[1]>=0 and coor[1]<=7):
            return True
    return False

def getGoalArea(coor):
    goalArea=set()
    for i in coor:
        allgoal=getboomArea(i)
        for tmpgoal in allgoal:
            if(isEmpty(tmpgoal,coor)):
                goalArea.add(tmpgoal)
    return goalArea

def getboomArea(coor):
    x=coor[0]
    y=coor[1]
    result=[]
    ls=[(x-1,y-1),(x-1,y),(x-1,y+1),(x,y-1),(x,y+1),(x+1,y-1),(x+1,y),(x+1,y+1)]
    for i in ls:
        if(CoorIsValid(i)):
            result.append(i)
    return result

def getBoomResult(boomArea,black):
    boomtoken=[i for i in black if i in boomArea]
    if(len(boomtoken)!=0):
        tmpblack=[i for i in black if i not in boomArea]
        for i in boomtoken:
            boomtoken=boomtoken+getBoomResult(getboomArea(i),tmpblack)
        return boomtoken
    else:
        return []

def getGoal(black):
    goalArea=getGoalArea(black)
    result={}
    for point in goalArea:
        boomArea=getboomArea(point)
        result[point]=list(set(getBoomResult(boomArea,black)))
    return result


def updateboomresult(coor,owntokens,opponenttokens):
    alltokens=owntokens+opponenttokens
    tmpowntokens=owntokens.copy()
    tmpopponenttokens=opponenttokens.copy()
    boomArea=getboomArea(coor)
    result=list(set(getBoomResult(boomArea,alltokens)))
    for owntoken in owntokens:
        if(owntoken in result):
            tmpowntokens.remove(owntoken)
    for opponenttoken in opponenttokens:
        if(opponenttoken in result):
            tmpopponenttokens.remove(opponenttoken)
    return tmpowntokens,tmpopponenttokens

if __name__ == '__main__':
    main();

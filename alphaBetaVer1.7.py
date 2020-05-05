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
    #testwhite = [(1,0),(0,1),(0,1),(0,1),(1,0),(0,0)]

    boardgame = SquareBoard(8,8, _BLACK_START_SQUARES.copy(),_WHITE_START_SQUARES.copy())


    #tempList = getinformat(boardgame,testWhite,True)

    #if detectStack(tempList):


    #print(f"afterconvertion {tempList}")
    #boardgame = SquareBoard(8,8,_BLACK_START_SQUARES.copy(),testwhite.copy())

    #white = [(1,0),(1,0),(0,1),(0,1),(0,1)]
    alphaBeta(testWhite, testBlack,boardgame)


    # realwhite can be replaced by any required tokenlist





def alphaBeta(white,black,boardgame):

    alpha = -1000
    beta = 1000

    #boardgame = SquareBoard(8,8,black.copy(),white.copy())
    Player = True

    depth = 3
    maxdepth = 3

    print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")


    print("start\n")
    startmove = (-1,-1)

    # All possible move inside
    #   Movemomen
    possibleMovement = {}

    # The best value
    value = alphaBetaCore(boardgame,depth,alpha,beta,Player,startmove,possibleMovement,white,black,maxdepth)
    #print(printList)

    print("finish\n")
    print(f"A-B result is {value}")
    print(f"THE MOVEMENT is {possibleMovement}")


''' Assume the white or black just pass possitions which is unknown the stack
    Ex : Chess board: white = [(1,1),(1,1),(1,2)]
        check inputwhite [(1,1)]
     1. Change to All shown form
        Ex: take [(1,1)]
            read from [(1,1),(1,1)]
     2. Do the judge ment
     3. Update the value
     4. From
        '''
def alphaBetaCore(boardgame,depth,alpha,beta,Player,move,printList,white,black,maxdepth):
    #Test only return
    print(f"Now at deep {depth}\n -----")


    # Need add the game end flag
    if depth == 0:

        #return len(getGoal(boardgame.opponenttokens))
        return len(list(set(getBoomResult(getboomArea(move),boardgame.opponenttokens))))\
         - len(list(set(getBoomResult(getboomArea(move),boardgame.owntokens))))


    if Player:
        white = getinformat(boardgame,white,True)
        maxvalue = -1000


        #Stack part if doesnt work please delete this if
        if detectStack(white):

            dictStack = createDic(white)
            # Key is the position of stacks
            for key in dictStack.keys():
                if dictStack[key] > 1:
                    temp = dictStack[key]
                    print(f" Now processing stack on{key}, the stack is number is{temp}")
                    #print("_____________\n")
                    stackdeep = dictStack[key]
                    while (stackdeep > 0):
                        print(f"current stackdeep is {stackdeep}")
                        for move in boardgame.validMove(key,temp,True):
                            if(not boardgame.onTheBoard(move)):
                                print("############")
                                tempsquarelist = white.copy()
                                tempsquarelistB = black.copy()
                                owntokensBefore = boardgame.owntokens.copy()
                                opponenttokenBefore = boardgame.opponenttokens.copy()


                                tempsquare = tempsquarelist[maxindex]


                                newwhite, newblack = updateboomresult(tempsquare,white.copy(),black.copy())
                                boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,newblack,maxdepth)
                                maxvalue = max(maxvalue,value)

                                if depth == maxdepth and value >= maxvalue:
                                        printList[("Bomb",tempsquare)] = value
                                alpha = max(alpha,maxvalue)
                                if beta <= alpha:
                                    # Undo the movment
                                    white = tempsquarelist
                                    black = tempsquarelistB
                                    boardgame.owntokens = owntokensBefore
                                    boardgame.opponenttokens = opponenttokenBefore
                                    break


                                white = tempsquarelist
                                black = tempsquarelistB
                                boardgame.owntokens = owntokensBefore
                                boardgame.opponenttokens = opponenttokenBefore
                                stackdeep = 0
                            else:

                                print("_____________\n")
                                tempsquareList = white.copy()
                                tempsquare = key

                                print(f"the white is {white}")
                                indexwhite = getDuplicateIndex(tempsquareList,key)[:stackdeep]
                                #print(f"white index is {indexwhite}")
                                for index in indexwhite:
                                   white[index] = move
                                print(f"the white is upgraded to {white}")
                                print(f"the white on board is {boardgame.owntokens}")
                                boardindex = getDuplicateIndex(boardgame.owntokens,key)[:stackdeep]

                                #print(f"board white index is {boardindex}")
                                for index in boardindex:
                                    boardgame.owntokens[index] = move
                                #print(f"the white on board is upgraded to {boardgame.owntokens}")
                                #print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")
                                #print("_____________\n")
                                newwhite = recoverFormat(white)
                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,black,maxdepth)
                                maxvalue = max(maxvalue,value)

                                if depth == maxdepth and value >= maxvalue:
                                    if boardgame.onTheBoard(move):
                                        printList[("MOVE",stackdeep,tempsquare,move)] = value
                                alpha = max(alpha,maxvalue)
                                #printList.append(move)

                                if beta <= alpha:
                                    # Undo the movment
                                    for index in indexwhite:
                                        white[index] = key
                                    for index in boardindex:
                                        boardgame.owntokens[index] = key
                                    break
                                #print("done upgrade now do recover\n")
                                #print("************")
                                #print(f"the white was upgraded to {realwhite}")
                                for index in indexwhite:
                                    white[index] = key
                                #print(f"the white is recovered to {realwhite}")
                                #print(f"the white on board was upgraded to {boardgame.owntokens}")
                                for index in boardindex:
                                    boardgame.owntokens[index] = key
                                #print(f"the white on board is recovered to {boardgame.owntokens}")
                        stackdeep -= 1

        # No stack part
        maxindex = 0


        #Check the owntoken required no stack
        for square in white:

            maxindex2 = 0
            print(f"check white token {square},currentdepth is {depth}")

            for move in boardgame.validMove(square,1,True):

                #Copy the white in the tempsquare
                if(not boardgame.onTheBoard(move)):
                    print("############")
                    tempsquarelist = white.copy()
                    tempsquarelistB = black.copy()
                    owntokensBefore = boardgame.owntokens.copy()
                    opponenttokenBefore = boardgame.opponenttokens.copy()


                    tempsquare = tempsquarelist[maxindex]


                    newwhite, newblack = updateboomresult(tempsquare,white.copy(),black.copy())
                    boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,newblack,maxdepth)
                    maxvalue = max(maxvalue,value)

                    if depth == maxdepth and value >= maxvalue:
                            printList[("Bomb",tempsquare)] = value
                    alpha = max(alpha,maxvalue)
                    if beta <= alpha:
                        # Undo the movment
                        white = tempsquarelist
                        black = tempsquarelistB
                        boardgame.owntokens = owntokensBefore
                        boardgame.opponenttokens = opponenttokenBefore
                        break


                    white = tempsquarelist
                    black = tempsquarelistB
                    boardgame.owntokens = owntokensBefore
                    boardgame.opponenttokens = opponenttokenBefore

                else:


                    tempsquarelist = white.copy()
                    tempsquare = tempsquarelist[maxindex]
                    print(f"Owntokens at {tempsquarelist},move to{move}, go {maxindex2}. depth is {depth}")

                    #Update White
                    white[maxindex]= move
                    #print(f"printout white {white}")
                    #Find the moved owntokens in the board
                    tempOwni = boardgame.owntokens.index(tempsquare)
                    boardgame.owntokens[tempOwni] = move

                    #print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")
                    #printList.append((Player, tempsquare))
                    #temp = len(printList)
                    #print(f"At the Layer route could be {printList}")
                    newwhite = recoverFormat(white)
                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,black,maxdepth)
                    #printList = printList[:temp-1]
                    #print(f"After back to the Layer route could be {printList}")
                    if depth == maxdepth and value >= maxvalue:
                        if boardgame.onTheBoard(move):
                            printList[("MOVE",1,tempsquare,move)] = value

                    maxvalue = max(maxvalue,value)



                    alpha = max(alpha,maxvalue)
                    #printList.append(move)

                    if beta <= alpha:
                        # Undo the movment
                        white[maxindex]= tempsquare
                        boardgame.owntokens[tempOwni] = tempsquare
                        break


                    # Undo the movment
                    white[maxindex]= tempsquare
                    boardgame.owntokens[tempOwni] = tempsquare

                maxindex2 = maxindex2 + 1


            maxindex = maxindex + 1

        return maxvalue

    else:


        black = getinformat(boardgame,black,False)

        minvalue = +1000


        #Stack part if doesnt work please delete this if
        if detectStack(black):

            dictStack = createDic(black)
            # Key is the position of stacks
            for key in dictStack.keys():
                if dictStack[key] > 1:
                    temp = dictStack[key]
                    print(f" Now processing stack on{key}, the stack is number is{temp},currentdepth is {depth}")
                    print("_____________\n")

                    stackdeep = dictStack[key]
                    while (stackdeep > 0):
                        #print(f"current stackdeep is {stackdeep}")

                        for move in boardgame.validMove(key,temp,False):
                            #print("_____________\n")

                            if(not boardgame.onTheBoard(move)):
                                print("############")
                                tempsquarelist = white.copy()
                                tempsquarelistB = black.copy()
                                owntokensBefore = boardgame.owntokens.copy()
                                opponenttokenBefore = boardgame.opponenttokens.copy()


                                tempsquare = tempsquarelist[minindex]


                                newwhite, newblack = updateboomresult(tempsquare,white.copy(),black.copy())
                                boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,newblack,maxdepth)
                                minvalue = min(minvalue,value)
                                beta = min(beta,minvalue)
                                #printList.append(move)
                                if beta <= alpha:
                                    # Undo the movment
                                    white = tempsquarelist
                                    black = tempsquarelistB
                                    boardgame.owntokens = owntokensBefore
                                    boardgame.opponenttokens = opponenttokenBefore
                                    break

                                white = tempsquarelist
                                black = tempsquarelistB
                                boardgame.owntokens = owntokensBefore
                                boardgame.opponenttokens = opponenttokenBefore
                                stackdeep = 0

                            else:

                                tempsquareList = black.copy()
                                tempsquare = key

                                print(f"the black is {black}")
                                indexblack = getDuplicateIndex(tempsquareList,key)[:stackdeep]
                                #print(f"white index is {indexwhite}")
                                for index in indexblack:
                                   black[index] = move
                                print(f"the black is upgraded to {black}")
                                print(f"the black on board is {boardgame.opponenttokens}")
                                boardindex = getDuplicateIndex(boardgame.opponenttokens,key)[:stackdeep]

                                #print(f"board white index is {boardindex}")
                                for index in boardindex:
                                    boardgame.opponenttokens[index] = move
                                #print(f"the black on board is upgraded to {boardgame.opponenttokens}")

                                #print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")
                                #print("_____________\n")

                                newblack = recoverFormat(black)
                                value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,white,newblack,maxdepth)
                                minvalue = min(minvalue,value)
                                beta = min(beta,minvalue)
                                #printList.append(move)

                                if beta <= alpha:
                                    # Undo the movment
                                    for index in indexblack:
                                        black[index] = key
                                    for index in boardindex:
                                        boardgame.opponenttokens[index] = key
                                    break
                                #print("done upgrade now do recover\n")
                                #print("************")
                                #print(f"the white was upgraded to {realwhite}")
                                for index in indexblack:
                                    black[index] = key
                                #print(f"the white is recovered to {realwhite}")
                                #print(f"the white on board was upgraded to {boardgame.owntokens}")
                                for index in boardindex:
                                    boardgame.opponenttokens[index] = key
                                #print(f"the white on board is recovered to {boardgame.owntokens}")
                        stackdeep -= 1

        minindex = 0
        for square in black:

            minindex2 = 0
            print(f"check black token {square},currentdepth is {depth}")
            for move in boardgame.validMove(square,1,False):

                if(not boardgame.onTheBoard(move)):
                    print("############")
                    tempsquarelist = white.copy()
                    tempsquarelistB = black.copy()
                    owntokensBefore = boardgame.owntokens.copy()
                    opponenttokenBefore = boardgame.opponenttokens.copy()


                    tempsquare = tempsquarelist[minindex]


                    newwhite, newblack = updateboomresult(tempsquare,white.copy(),black.copy())
                    boardgame.owntokens, boardgame.opponenttokens = updateboomresult(tempsquare,owntokensBefore.copy(),opponenttokenBefore.copy())

                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,newwhite,newblack,maxdepth)
                    minvalue = min(minvalue,value)
                    beta = min(beta,minvalue)
                    #printList.append(move)
                    if beta <= alpha:
                        # Undo the movment
                        white = tempsquarelist
                        black = tempsquarelistB
                        boardgame.owntokens = owntokensBefore
                        boardgame.opponenttokens = opponenttokenBefore
                        break

                    white = tempsquarelist
                    black = tempsquarelistB
                    boardgame.owntokens = owntokensBefore
                    boardgame.opponenttokens = opponenttokenBefore

                else:
                    #print(f"the current {square} can go {boardgame.validMove(square,1,False)}")
                    #Copy the black in the tempsquare
                    tempsquarelist = black.copy()
                    tempsquare = tempsquarelist[minindex]

                    print(f"Opponentokens at {tempsquarelist},move to{move}, go {minindex2}. depth is {depth}")
                    #Update black
                    black[minindex]= move
                    print(f"printout black {black}")
                    #Find the moved owntokens in the board
                    tempOppi = boardgame.opponenttokens.index(tempsquare)
                    boardgame.opponenttokens[tempOppi] = move


                    print(f"printout chess board: black is {boardgame.opponenttokens}, white is {boardgame.owntokens}")
                    newblack = recoverFormat(black)
                    value =  alphaBetaCore(boardgame,depth-1,alpha,beta,not Player,move,printList,white,newblack,maxdepth)
                    minvalue = min(minvalue,value)


                    beta = min(beta,minvalue)
                    #printList.append(move)
                    if beta <= alpha:
                        # Undo the movment
                        black[minindex]= tempsquare
                        boardgame.opponenttokens[tempOppi] = tempsquare
                        break
                    # Undo the movment
                    black[minindex]= tempsquare
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

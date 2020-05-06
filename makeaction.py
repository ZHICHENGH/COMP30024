class SquareBoard:
    def __init__ (self,owntokens,opponenttokens):
        self.opponenttokens = opponenttokens
        self.owntokens = owntokens
def CoorIsValid(coor):
    if (coor[0]>=0 and coor[0]<=7):
        if (coor[1]>=0 and coor[1]<=7):
            return True
    return False
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
def getBoomResult(boomArea,aimtokens):
    boomtoken=[i for i in aimtokens if i in boomArea]
    if(len(boomtoken)!=0):
        tmptokens=[i for i in aimtokens if i not in boomArea]
        for i in boomtoken:
            boomtoken=boomtoken+getBoomResult(getboomArea(i),tmptokens)
        return boomtoken
    else:
        return []
def getGoal(aimtokens):
    goalArea=getGoalArea(aimtokens)
    result={}
    for point in goalArea:
        boomArea=getboomArea(point)
        result[point]=list(set(getBoomResult(boomArea,aimtokens)))
    return result

def geteva(owntokens,opponenttokens):
    alltokens=owntokens+opponenttokens
    initeva={}
    tmpresult={}
    for i in range(0,8):
        for j in range(0,8):
            point=(i,j)
            boomArea=getboomArea(point)
            tmpresult[point]=list(set(getBoomResult(boomArea,alltokens)))
            evavalue=0
            for coor in tmpresult[point]:
                evavalue+=(opponenttokens.count(coor)-owntokens.count(coor))
            if(isEmpty(point,alltokens) and evavalue!=0):
                if(evavalue<0):
                    evavalue+=1
                else:
                    evavalue-=1
            initeva[point]=evavalue
    return initeva

def getdistance(owntoken,goal,owntokens):
    stack=owntokens.count(owntoken)
    dis1=abs(owntoken[0]-goal[0])
    dis2=abs(owntoken[1]-goal[1])
    if(dis1%stack!=0):
        dis1=(dis1/stack)+1
    else:
        dis1=dis1/stack
    if(dis2%stack!=0):
        dis2=(dis2/stack)+1
    else:
        dis2=dis2/stack
    return dis1+dis2
def gettokengoalcomb(owntokens,opponenttokens):
    initeva=geteva(owntokens,opponenttokens)
    tokengoalcomb=[]
    alltokens=owntokens+opponenttokens
    for goalpoint in initeva.keys():
        if(initeva[goalpoint]>=0):
            tmptokens=owntokens
        else:
            tmptokens=opponenttokens
        for tmptoken in tmptokens:
                distance=getdistance(tmptoken,goalpoint,tmptokens)
                if(initeva[goalpoint]!=0):
                    tokengoalcomb.append([goalpoint,tmptoken,distance,initeva[goalpoint]])
    tokengoalcomb=sorted(tokengoalcomb,key=lambda x:(x[2],x[3]))
    return tokengoalcomb


def getchoosentokens(k,owntokens,opponenttokens):
    alltokens=opponenttokens+owntokens
    tokengoalcomb=gettokengoalcomb(owntokens,opponenttokens)
    chosentokens=set()
    minvalue=0
    maxvalue=0
    for comb in tokengoalcomb:
        if(tokengoalcomb[0][2]==comb[2]):
            if(comb[3]>=maxvalue):
                maxvalue=comb[3]
            if(comb[3]<minvalue):
                minvalue=comb[3]
        else:
            break
    if(maxvalue>=abs(minvalue)):
        decidevalue=maxvalue
    else:
        decidevalue=minvalue
    for comb in tokengoalcomb:
        if(tokengoalcomb[0][2]==comb[2]):
            if(decidevalue==comb[3]):
                if(decidevalue>=0):
                    chosentokens.add(comb[1])
                else:
                    boomArea=getboomArea(comb[0])
                    tmpresult=list(set(getBoomResult(boomArea,alltokens)))
                    for tmptoken in tmpresult:
                        if tmptoken in owntokens:
                            chosentokens.add(tmptoken)
        else:
            break
    '''if(len(chosentokens)==0):
        maxvalue=0
        stepnum=3
        while(len(chosentokens)==0):
            for comb in tokengoalcomb:
                if((comb[3]>=1) and comb[2]<=stepnum):
                    if(comb[3]>=0):
                        chosentokens.add(comb[1])
                    else:
                        boomArea=getboomArea(comb[0])
                        tmpresult=list(set(getBoomResult(boomArea,alltokens)))
                        for tmptoken in tmpresult:
                             if tmptoken in owntokens:
                                 chosentokens.add(tmptoken)
            stepnum+=1'''
    return list(chosentokens)

def makeevaluation(movement,coor,owntokens,opponenttokens):
    alltokens=opponenttokens+owntokens
    evavalue=0
    if(movement==1):
        boomArea=getboomArea(coor)
        tmplist=list(set(getBoomResult(boomArea,alltokens)))
        for coor in tmplist:
            evavalue+=(opponenttokens.count(coor)-owntokens.count(coor))
    else:
        tokengoalcombs=gettokengoalcomb(owntokens,opponenttokens)
        mostvaluable=[]
        mostdan=[]
        for comb in tokengoalcombs:
            if(mostvaluable!=[] and mostdan!=[]):
                break
            if((abs(comb[3])>=1)):
                if(comb[3]>=0):
                    if(mostvaluable==[]):
                        mostvaluable=comb
                else:
                    if(mostdan==[]):
                        mostdan=comb
        evavalue=(1.0*mostvaluable[3])/mostvaluable[2]+(1.0*mostdan[3])/mostdan[2]
    return evavalue





def getinitGoal(owntokens,opponenttokens):
    goaldic=getGoal(opponenttokens)
    initgoals=[]
    for goal in goaldic.keys():
        for owntoken in owntokens:
            distance=abs(owntoken[0]-goal[0])+abs(owntoken[1]-goal[1])
            initgoals.append([goal,owntoken,distance,len(goaldic[goal])])
        
def getaveragedistance(k,whites,goalcoor):
    distances=[]
    totaldistance=0
    for coor in whites:
        distances.append(abs(coor[0]-goalcoor[0])+abs(coor[1]-goalcoor[1]))
    distances=sorted(distances)
    for i in range(0,k):
        totaldistance+=distances[i]
    return totaldistance/k

def getsupportgoal(k,whites,blacks):
    goaldic=getGoal(blacks)
    maxvalue=0
    for goalpoint in goaldic.keys():
        if(maxvalue<len(goaldic[goalpoint])):
            maxvalue=len(goaldic[goalpoint])
    mindistance=99999
    for goalpoint in goaldic.keys():
        if(len(goaldic[goalpoint])==maxvalue):
            distance=getaveragedistance(k,whites,goalpoint)
            if(mindistance>distance):
                mindistance=distance
                result=goalpoint
    return result

def alphaBeta(white,black,boardgame):
    alpha = -1000
    beta = 1000
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


def GameOver(owntokens,opponenttokens):
    if(len(owntokens)==0 or len(opponenttokens)==0):
       return True
    return False
def getpossiblemovement(coor,boardgame):
    stacknumber=boardgame.owntokens.count(coor)
    possiblegoal=[]
    directions=[-1,1]
    result=[]
    for i in range(1,stacknumber+1):
        for direction in directions:
                possiblegoal.append((coor[0]+direction*i, coor[1]))
                possiblegoal.append((coor[0],coor[1]+direction*i))
    possiblegoal= filter(CoorIsValid,possiblegoal)
    tmppossiblegoal=possiblegoal.copy()
    for goal in possiblegoal:
        if goal in boardgame.opponenttokens:
            tmppossiblegoal.remove(goal)
    possiblegoal=tmppossiblegoal.copy()
    for goal in possiblegoal:
        owntokens=boardgame.owntokens.copy()
        for i in range(0,stacknumber):
                owntokens.remove(coor)
                owntokens.append(goal)
                newboardgame=(owntokens.copy(),boardgame.opponenttokens)
                result.append(newboardgame)
    return result
def alphaBetaCore(boardgame,movement,depth,alpha,beta,Player,coor,owntokens,opponenttokens,maxdepth,chosenowntokens,chosenopponenttokens):
    #bottom of the tree
    if (depth==maxdepth or GameOver(owntokens,opponenttokens)):
        if(movement==1):
            return makeevaluation(1,coor,owntokens,opponenttokens)
        else:
            return makeevaluation(0,coor,owntokens,opponenttokens)
    possibleMovement=getpossiblemovement(coor,owntokens,opponenttokens)


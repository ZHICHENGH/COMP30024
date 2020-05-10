class SquareBoard:
    def __init__ (self,owntokens,opponenttokens):
        self.opponenttokens = opponenttokens.copy()
        self.owntokens = owntokens.copy()
        self.movementrecord=[]
    def copy (self):
        opponenttokens=self.opponenttokens.copy()
        owntokens = self.owntokens.copy()
        newboardgame=SquareBoard(owntokens,opponenttokens)
        return newboardgame
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
def geteva(owntokens,opponenttokens):
    alltokens=owntokens+opponenttokens
    initeva={}
    tmpresult={}
    for i in range(0,8):
        for j in range(0,8):
            point=(i,j)
            #if(isEmpty(point,alltokens)):
            evavalue=makeboomeva(point,owntokens,opponenttokens)
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
        if(isEmpty(goalpoint,alltokens)):
            if(initeva[goalpoint]>0):
                tmptokens=owntokens
            elif(initeva[goalpoint]<0):
                tmptokens=opponenttokens
            elif(initeva[goalpoint]==0):
                tmptokens=owntokens+opponenttokens
            for tmptoken in tmptokens:
                    if(initeva[goalpoint]!=0):
                        distance=getdistance(tmptoken,goalpoint,tmptokens)
                        tokengoalcomb.append([goalpoint,tmptoken,distance,initeva[goalpoint]])
        else:
            if(initeva[goalpoint]>0 and (goalpoint in owntokens)):
                tokengoalcomb.append([goalpoint,goalpoint,0,initeva[goalpoint]])
            if(initeva[goalpoint]<0 and (goalpoint in opponenttokens)):
                tokengoalcomb.append([goalpoint,goalpoint,0,initeva[goalpoint]])
    tokengoalcomb=sorted(tokengoalcomb,key=lambda x:(x[2],-abs(x[3])))
    return removerepe(tokengoalcomb)


def getchoosentokens(boardgame):
    alltokens=boardgame.opponenttokens+boardgame.owntokens
    tokengoalcomb=gettokengoalcomb(boardgame.owntokens,boardgame.opponenttokens)
    chosentokens=set()
    minvalue=0
    maxvalue=0
    mindist=0
    maxdist=0
    #boom tokens
    '''for token in boardgame.owntokens:
        area=getboomArea(token)
        result=getBoomResult(area,alltokens)
        if(makeboomeva(token,boardgame.owntokens,boardgame.opponenttokens)>=1):
            chosentokens.add(token)
    if(len(chosentokens)!=0):
        return list(chosentokens)'''
    for comb in tokengoalcomb:
        if(minvalue==0):
            if(comb[3]<0):
                minvalue=comb[3]
                mindist=comb[2]
        if(maxvalue==0):
            if(comb[3]>0):
                maxvalue=comb[3]
                maxdist=comb[2]
        if(maxvalue!=0 and minvalue!=0):
            break
    '''if(maxvalue>=abs(minvalue)):
        decidevalue=maxvalue
    else:
        decidevalue=minvalue'''
    for comb in tokengoalcomb:
        if(comb[2]<=max(maxdist,mindist)):
            if(maxvalue==comb[3] and maxdist==comb[2]):
                chosentokens.add(comb[1])
            if(minvalue==comb[3] and mindist==comb[2]):
                boomArea=getboomArea(comb[0])
                tmpresult=getBoomResult(boomArea,alltokens)
                tmpresult.append(comb[0])
                tmpresult=list(set(tmpresult))
                for tmptoken in tmpresult:
                    if tmptoken in boardgame.owntokens:
                        chosentokens.add(tmptoken)
        else:
            break
    if(minvalue==0):
        newboardgame=SquareBoard(boardgame.opponenttokens,boardgame.owntokens)
        chosentokens.add(getclosedtokens(newboardgame)[2])
    if(maxvalue==0):
        chosentokens.add(getclosedtokens(boardgame)[1])        
    return list(chosentokens)


def getclosedtokens(boardgame):
    owntokens=boardgame.owntokens
    opponentokens=boardgame.opponenttokens
    comblist=[]
    for owntoken in boardgame.owntokens:
        for opponenttoken in boardgame.opponenttokens:
            comblist.append([getdistance(owntoken,opponenttoken,owntokens),owntoken,opponenttoken])
            comblist=sorted(comblist,key=lambda x:x[0])
    return comblist[0]


def updateboomresult(coor,boardgame):
    alltokens=boardgame.owntokens+boardgame.opponenttokens
    tmpowntokens=boardgame.owntokens.copy()
    tmpopponenttokens=boardgame.opponenttokens.copy()
    boomArea=getboomArea(coor)
    result=getBoomResult(boomArea,alltokens)
    result.append(coor)
    result=list(set(result))
    for owntoken in boardgame.owntokens:
        if(owntoken in result):
            tmpowntokens.remove(owntoken)
    for opponenttoken in boardgame.opponenttokens:
        if(opponenttoken in result):
            tmpopponenttokens.remove(opponenttoken)
    return tmpowntokens,tmpopponenttokens
def makeboomeva(coor,owntokens,opponenttokens):
    alltokens=opponenttokens+owntokens
    evavalue=0
    boomArea=getboomArea(coor)
    tmplist=getBoomResult(boomArea,alltokens)
    tmplist.append(coor)
    tmplist=list(set(tmplist))
    for coor in tmplist:
        evavalue+=(opponenttokens.count(coor)-owntokens.count(coor))
    return evavalue


def makemovementeva(movement,Player):
    boardgame=movement[0]
    owntokens=boardgame.owntokens
    opponenttokens=boardgame.opponenttokens
    #print(owntokens,opponenttokens)
    alltokens=opponenttokens+owntokens
    evavalue=0
    if(0==1):
        return
    else:
        coor=movement[1][3]
        if(coor in owntokens):
            if(makeboomeva(coor,owntokens,opponenttokens)>=1):
                evavalue=makeboomeva(coor,owntokens,opponenttokens)
                evavalue=evavalue+len(owntokens)-len(opponenttokens)
                evavalue=(1.0*evavalue)/10
                return evavalue
        else:
            if(makeboomeva(coor,owntokens,opponenttokens)<=-1):
                evavalue=makeboomeva(coor,opponenttokens,owntokens)
                evavalue=evavalue+len(owntokens)-len(opponenttokens)
                evavalue=(1.0*evavalue)/10
                return evavalue
        
        tokengoalcombs=gettokengoalcomb(owntokens,opponenttokens)
        mostvaluable=[]
        mostdan=[]
        for comb in tokengoalcombs:
            if(mostvaluable!=[] and mostdan!=[]):
                break
            if((abs(comb[3])>=1)):
                if(comb[3]>=0):
                    if(mostvaluable==[]):
                        if(isEmpty(comb[0],alltokens) or (comb[0] in owntokens)):
                            mostvaluable=comb     
                else:
                    if(mostdan==[]):
                        if(isEmpty(comb[0],alltokens) or (comb[0] in opponenttokens)):
                            mostdan=comb
        if(len(mostvaluable)!=0):
            if(mostvaluable[2]==0):
                tmp1=1
            else:
                tmp1=mostvaluable[2]+1
            if(len(mostdan)!=0):
                if(mostdan[2]==0):
                    tmp2=1
                else:
                    tmp2=1+mostdan[2]
                evavalue=(1.0*mostvaluable[3])/tmp1+(1.0*mostdan[3])/tmp2
            else:
                evavalue=(1.0*mostvaluable[3])/tmp1
        else:
            if(len(mostdan)!=0):
                if(mostdan[2]==0):
                    tmp2=1
                else:
                    tmp2=1+mostdan[2]
                evavalue=(1.0*mostdan[3])/tmp2
            else:
                comblist=[]
                for owntoken in boardgame.owntokens:
                    for opponenttoken in boardgame.opponenttokens:
                        comblist.append(getdistance(owntoken,opponenttoken,owntokens))
                comblist=sorted(comblist)
                evavalue=1.0/(comblist[0]+1)
    evavalue=(1.0*evavalue)/20
    evavalue=evavalue+len(owntokens)-len(opponenttokens)
    return evavalue
def alphaBeta(owntokens,opponenttokens):
    alpha = -1000
    beta = 1000
    Player = True
    depth = 1
    maxdepth=4
    boardgame=SquareBoard(owntokens,opponenttokens)
    movement=[boardgame,[]]
    value,ls=alphaBetaCore(movement,depth,alpha,beta,maxdepth,Player)
    return ls


def GameOver(owntokens,opponenttokens):
    if(len(owntokens)==0 or len(opponenttokens)==0):
       return True
    return False

def getpossiblemovement(boardgame):
    coors=getchoosentokens(boardgame.copy())
    alltokens=boardgame.owntokens+boardgame.opponenttokens
    result=[]
    directions=[-1,1]
    for coor in coors: 
        stacknumber=boardgame.owntokens.count(coor)
        possiblegoal=[]
        for i in range(1,stacknumber+1):
            for direction in directions:
                    possiblegoal.append((coor[0]+direction*i, coor[1]))
                    possiblegoal.append((coor[0],coor[1]+direction*i))
        possiblegoal= filter(CoorIsValid,possiblegoal)
        possiblegoal=list(possiblegoal)
        tmppossiblegoal=possiblegoal.copy()
        for goal in possiblegoal:
            if goal in boardgame.opponenttokens:
                tmppossiblegoal.remove(goal)
        for goal in tmppossiblegoal:
            owntokens=boardgame.owntokens.copy()
            for i in range(1,stacknumber+1):
                    owntokens.remove(coor)
                    owntokens.append(goal)
                    newboardgame=SquareBoard(owntokens.copy(),boardgame.opponenttokens)
                    tplist=boardgame.movementrecord.copy()
                    actiondescribe=("MOVE",i,coor,goal)
                    tplist.append(actiondescribe)
                    newboardgame.movementrecord=tplist
                    result.append([newboardgame,actiondescribe])
    #boom
    for point in coors:
        if(point in boardgame.owntokens):
            boomArea=getboomArea(point)
            tmplist=getBoomResult(boomArea,alltokens)
            tmplist.append(point)
            tmplist=list(set(tmplist))
            if(makeboomeva(point,boardgame.owntokens,boardgame.opponenttokens)>=0):
                actiondescribe=("BOOM",point)
                result.append([boardgame,actiondescribe])
    result.reverse()
    return result
def removerepe(inputlist):
    result=[]
    if(inputlist!=[]):
        for part in inputlist:
            if not (part in result):
                result.append(part)
    return result.copy()
def alphaBetaCore(movement,depth,alpha,beta,maxdepth,Player):
    #bottom of the tree
    boardgame=movement[0].copy()
    if (GameOver(boardgame.owntokens,boardgame.opponenttokens)):
        #if(Player==True):
        if(len(boardgame.owntokens)==0):
            return (-500,[])
        else:
            return (500,[])
    if(len(movement[1])!=0):
        if(movement[1][0]=="BOOM"):
            coor=movement[1][1]
            evavalue=(1.0*makeboomeva(coor,boardgame.owntokens,boardgame.opponenttokens))/depth
            if(evavalue==0):
                if((len(boardgame.owntokens)-len(boardgame.opponenttokens))>0):
                    evavalue=1
                else:
                    evavalue=0.15
            evavalue=evavalue+len(boardgame.owntokens)-len(boardgame.opponenttokens)
            return evavalue/depth,[]
            newowntokens,newopponenttokens=updateboomresult(coor,movement[0])
            boardgame=SquareBoard(newowntokens,newopponenttokens)
    if (depth==maxdepth):
        return (makemovementeva(movement,Player),[])
    if(Player==True):
        value=-1000
        choosenmove=[]
        possibleMovements=getpossiblemovement(boardgame)
        possibleMovements=removerepe(possibleMovements.copy())
        for possibleMovement in possibleMovements:
            tmpvalue,tmpls=alphaBetaCore(possibleMovement,depth+1,alpha,beta,maxdepth,False)
            if(tmpvalue>value):
                value=tmpvalue
                choosenmove=possibleMovement[1]
            alpha=max(alpha,value)
            if(beta<=alpha):
                break
        return value,choosenmove
    else:
        value=1000
        newowntokens=boardgame.opponenttokens.copy()
        newopponenttokens=boardgame.owntokens.copy()
        boardgame=SquareBoard(newowntokens,newopponenttokens)
        possibleMovements=getpossiblemovement(boardgame)
        possibleMovements=removerepe(possibleMovements.copy())
        for possibleMovement in possibleMovements:
            newowntokens=possibleMovement[0].opponenttokens.copy()
            newopponenttokens=possibleMovement[0].owntokens.copy()
            newboardgame=SquareBoard(newowntokens,newopponenttokens)
            possibleMovement[0]=newboardgame
            tmpvalue,fathermovement=alphaBetaCore(possibleMovement,depth+1,alpha,beta,maxdepth,True)
            value=min(tmpvalue,value)
            beta=min(beta,value)
            if(beta<=alpha):
                break
        return value,boardgame.movementrecord

def main():
    owntokens=[(0,6),(0,7),(1,6),(1,7),(3,7),(4,7),(6,6),(6,7),(7,6),(7,7),(6,2),(6,2)]
    
    opponenttokens=[(0,0),(0,1),(1,1),(1,0),(1,4),(3,3),(4,0),(4,1),(6,0),(6,1),(7,0),(7,1)]
    boardgame=SquareBoard(owntokens,opponenttokens)
    move= ('MOVE', 2, (6, 4), (6, 2))
    movement=[boardgame,move]
    print(makemovementeva(movement,True))
    #print(alphaBetaCore(movement,1,-1000,1000,4,True))

    owntokens=[(0,0),(0,1),(1,1),(1,0),(3,0),(4,0),(4,0),(4,3),(4,3),(6,0),(6,1),(7,0),(7,1)]
    opponenttokens=[(0,6),(0,7),(1,4),(1,4),(3,6),(3,7),(4,6),(4,7),(7,6),(7,7),(6,6),(6,7)]
    
    boardgame=SquareBoard(owntokens,opponenttokens)
    move= ('MOVE',2, (4, 3), (4, 5))
    movement=[boardgame,move]
    print(makemovementeva(movement,True))
    #print(alphaBetaCore(movement,1,-1000,1000,4,True))
    '''
    newowntokens=[(4,4),(4,4),(4,4),(4,4),(3,3),(3,0),(4,0),(6,0),(6,1),(7,0),(7,1)]
    newopponenttokens=[(1,1),(1,1),(3,1),(3,0),(3,0),(3,0),(4,0),(4,1),(6,0),(6,1),(7,0),(7,1)]
    newboardgame=SquareBoard(newowntokens,newopponenttokens)
    newmove=("MOVE",4,(1,4),(4,4))
    newmovement=[newboardgame,newmove]
    print(makemovementeva(newmovement,True))
    #print(alphaBetaCore(newmovement,0,-1000,1000,3,True))
    
    newowntokens=[(0,5),(0,7),(1,6),(1,7),(3,7),(4,7),(5,5),(5,5),(5,5),(6,7),(7,6),(7,7)]
    newopponenttokens=[(0,1),(0,2),(1,0),(1,1),(2,0),(4,1),(5,0),(5,0),(6,0),(6,1),(7,0),(7,1)]
    newboardgame=SquareBoard(newowntokens,newopponenttokens)
    testmove=('MOVE', 1, (5, 5), (5, 2))
    testmovement=[newboardgame,testmove]
    #print(makemovementeva(testmovement,True))
    newmovement=[newboardgame,[]]
    print(alphaBetaCore(newmovement,0,-1000,1000,3,True))'''

if __name__ == '__main__':
    main()


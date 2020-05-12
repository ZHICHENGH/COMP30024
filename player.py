import spes.makeaction 
import time
class ExamplePlayer:
    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the 
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your 
        program will play as (White or Black). The value will be one of the 
        strings "white" or "black" correspondingly.
        """
        # TODO: Set up state representation.
        self.round=0
        self.colour=colour
        self.firstmove=[]
        self.timerecord=[]
        self.timecount=0.0
        whites=[(0,0),(0,1),(1,0),(1,1),
                (3,0),(3,1),(4,0),(4,1),
                (6,0),(6,1),(7,0),(7,1)]
        blacks=[(0,7),(0,6),(1,7),(1,6),
                (3,7),(3,6),(4,7),(4,6),
                (6,7),(7,7),(6,6),(7,6)]
        if(colour=="black"):
            self.owntokens=blacks
            self.opponenttokens=whites
        else:
            self.owntokens=whites
            self.opponenttokens=blacks            
            
    def action(self):
        start = time.time()
        if(self.round<4):
            if(self.round==0):
                return ("MOVE",1,(4,0),(4,1))
            elif(self.round==1):
                if(self.firstmove[0][0]=="MOVE"):
                    x=self.firstmove[0][3][0]
                    y=self.firstmove[0][3][1]
                    return ("MOVE",1,(x,7),(x,6))
            elif(self.round==2):
                return ("MOVE",1,(3,1),(4,1))
            elif(self.round==3):
                if(self.firstmove[0][0]=="MOVE"):
                    begin=(-1,-1)
                    x=self.firstmove[0][3][0]
                    y=self.firstmove[0][3][1]
                    if((x-1,6) in self.owntokens):
                        begin=(x-1,6)
                    elif((x+1,6) in self.owntokens):
                        begin=(x+1,6)
                    return ("MOVE",1,begin,(x,6))
        result=spes.makeaction.alphaBeta(self.owntokens.copy(),self.opponenttokens.copy(),self.timecount)
        end = time.time()
        self.timecount+=(end-start)
        self.timerecord.append([(len(self.owntokens)+len(self.opponenttokens)),end-start])
        return result
        """
        This method is called at the beginning of each of your turns to request 
        a choice of action from your program.

        Based on the current state of the game, your player should select and 
        return an allowed action to play on this turn. The action must be
        represented based on the spec's instructions for representing actions.
        """
        # TODO: Decide what action to take, and return it
       


    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s 
        turns) to inform your player about the most recent action. You should 
        use this opportunity to maintain your internal representation of the 
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (White or Black). The value will be one of the strings "white" or
        "black" correspondingly.

        The parameter action is a representation of the most recent action
        conforming to the spec's instructions for representing actions.

        You may assume that action will always correspond to an allowed action 
        for the player colour (your method does not need to validate the action
        against the game rules).
        """
        # TODO: Update state representation in response to action.
        if(self.round==0):
            self.firstmove.append(action)
        self.round+=1
        if(action[0]=="BOOM"):
            coor=action[1]
            boardgame=spes.makeaction.SquareBoard(self.owntokens,self.opponenttokens)
            tmpowntokens,tmpopponenttokens=spes.makeaction.updateboomresult(coor,boardgame)
            self.owntokens=tmpowntokens
            self.opponenttokens=tmpopponenttokens
        else:
            for i in range(0,action[1]):
                if(colour==self.colour):
                    self.owntokens.remove(action[2])
                    self.owntokens.append(action[3])
                else:
                    self.opponenttokens.remove(action[2])
                    self.opponenttokens.append(action[3])
        

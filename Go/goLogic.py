

class Board():
    
    #ERRORS
    ERRinterOccupied = "ERROR : Intersection occupied." 
    ERRmovePlayerArgumentNotValid = "ERROR : Move: Player argument wasn't 1*-1."
    ERRsuicide = "ERROR : Suicidal Move"
    ERRKo = "Ko"
    ERRwrongIndex = "ERROR : Invalid coordinates."
    Success = "Move successfully made."
    #------
    
    class Intersection:
        
        def __init__(self, x, y):
            self.x = x#0;0 is top left, 0;1 just below, whereas 1;0 is to the very right
            self.y = y
            self.content = 0
            
    def __init__(self, width, height) :
        
        self.height = height
        self.width = width
        self.inters = []
        self.lastInters = None
        
        for y in range(self.height):
            for x in range(self.width):
                self.inters.append(self.Intersection(x, y))
    
    def giveIndex(self, x, y):#gives index of Square object in the inters list given x and y coords
        for count, inter in enumerate(self.inters):
            if x == inter.x and y == inter.y: return count
        return None
                              
    def move(self, x, y, player):
        
        if player != 1 and player != -1: return False, self.ERRmovePlayerArgumentNotValid
        
        for count, inter in enumerate(self.inters):
            if x == inter.x and y == inter.y:
                if inter.content == 0 :
                    if self.isMoveLegal(x, y, self.lastInters, player):
                        self.lastInters = self.inters
                        self.inters = self.captures(self.inters, x, y, player)
                        return True, self.Success
                    else: return False, self.ERRsuicide
                else: return False, self.ERRinterOccupied
        return False, self.ERRwrongIndex

    def isMoveLegal(self, x, y, lastInters, player):
        
        theoreticalInters = self.inters
        theoreticalInters[self.giveIndex(x, y)].content = player
        
        #if lastInters == theoreticalInters: return False #KO rule (simple one, per Japanese ruleset)
        if self.captures(theoreticalInters, x, y, player)[self.giveIndex(x,y)].content == 0: return False
        return True
    
    def isInterAnEdge(self, x, y):
        listOfEdges = []
        listOfEdges.append(x==0)#left
        listOfEdges.append(y==0)#top
        listOfEdges.append(x==self.width-1)#right
        listOfEdges.append(y==self.height-1)#bottom
        return listOfEdges

    def amIAnEdge(self, x, y):
        if x<0 or y<0 or x>=self.width or y >= self.height: return True
        else: return False
        
    def neighbour(self, x, y, inters, direction):#returns opposite color of inter you want to have the content of if you ask for an edge
        if direction == 'left':
            if x-1 <0: return inters[self.giveIndex(x, y)].content*-1
            else : return inters[self.giveIndex(x-1, y)].content
        elif direction == "up":
            if y-1 <0: return inters[self.giveIndex(x, y)].content*-1
            else: return inters[self.giveIndex(x, y-1)].content
        elif direction == 'right':
            if x+1 >= self.width: return inters[self.giveIndex(x, y)].content*-1
            else: return inters[self.giveIndex(x+1, y)].content
        elif direction == 'down':
            if y+1 >= self.height: return inters[self.giveIndex(x, y)].content*-1
            else: return inters[self.giveIndex(x, y+1)].content

    def captures(self, workingInters, x, y, player):
        
        def findChain(myX, myY):
            
            color = workingInters[self.giveIndex(myX,myY)].content
            if self.amIAnEdge(myX,myY): return []

            seenInters = [workingInters[self.giveIndex(myX,myY)]]
            checkedInters = []
            
            while len(seenInters) != 0:
                
                pointerX = seenInters[0].x
                pointerY = seenInters[0].y
                
                if self.neighbour(pointerX, pointerY, workingInters, "left") == color:
                    seenInters.append(workingInters[self.giveIndex(pointerX-1, pointerY)])
                if self.neighbour(pointerX, pointerY, workingInters, "up") == color:
                    seenInters.append(workingInters[self.giveIndex(pointerX, pointerY-1)])
                if self.neighbour(pointerX, pointerY, workingInters, "right") == color:
                    seenInters.append(workingInters[self.giveIndex(pointerX+1, pointerY)])
                if self.neighbour(pointerX, pointerY, workingInters, "down") == color:
                    seenInters.append(workingInters[self.giveIndex(pointerX, pointerY+1)])
            
                checkedInters.append(workingInters[self.giveIndex(pointerX,pointerY)])
                
                for seenInter in seenInters: #remove inter from seenInters if it is in checkedInters
                    for checkedInter in checkedInters:
                        if seenInter.x == checkedInter.x and seenInter.y == checkedInter.y:
                            seenInters = [i for i in seenInters if i != seenInter]
            
            return checkedInters
        
        intersToWipe = []
        
        def findLiberties(chain):
            
            chainHasAliberty = False
            for inter in chain:
                if self.neighbour(inter.x, inter.y, workingInters, "left") == 0:
                    chainHasAliberty = True
                if self.neighbour(inter.x, inter.y, workingInters, "up") == 0:
                    chainHasAliberty = True
                if self.neighbour(inter.x, inter.y, workingInters, "right") == 0:
                    chainHasAliberty = True
                if self.neighbour(inter.x, inter.y, workingInters, "down") == 0:
                    chainHasAliberty = True
            if chainHasAliberty == False:
                for inter in chain:
                    intersToWipe.append(inter)
                    
        if self.neighbour(x, y, workingInters, "left") == player*-1 and self.amIAnEdge(x-1, y) == False:
            leftChain = findChain(x-1,y) 
            findLiberties(leftChain)
        if self.neighbour(x, y, workingInters, "up") == player*-1 and self.amIAnEdge(x, y-1) == False:
            upChain = findChain(x,y-1)
            findLiberties(upChain)
        if self.neighbour(x, y, workingInters, "right") == player*-1 and self.amIAnEdge(x+1, y) == False:
            rightChain = findChain(x+1,y)
            findLiberties(rightChain)
        if self.neighbour(x, y, workingInters, "down") == player*-1 and self.amIAnEdge(x, y+1) == False:
            downChain = findChain(x,y+1)
            findLiberties(downChain)
            
        #print(len(intersToWipe))
        
        if len(intersToWipe) > 0:
            for inter in intersToWipe:
                workingInters[self.giveIndex(inter.x, inter.y)].content = 0
        else: 
            selfChain = findChain(x, y)
            intersToWipe = []
            findLiberties(selfChain)
            for inter in intersToWipe:
                workingInters[self.giveIndex(inter.x, inter.y)].content = 0
            
        return workingInters
                 
    def displayBoard(self):
        for count, content in enumerate(self.inters):
            #print(f"{content.x};{content.y}>>{content.content}", end = "     ")
            print(f"{content.content}", end = "    ")
            if count % self.width == self.width-1: print()
        
    def giveBoard(self):
        return self.inters

if __name__ == "__main__":
    b = Board(5,5)
    while True:
        inX = int(input("x : "))
        inY = int(input("y : "))
        inPlayer = int(input("p : "))

        b.move(inX, inY, inPlayer)
        b.displayBoard()

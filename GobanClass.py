from copy import deepcopy

class Goban:
    
    def __init__(self, height, width):
        
        self.height = height
        self.width = width
        self.inters = [[0 for j in range(width)] for i in range(height)]
        self.oldInters = deepcopy(self.inters)
        #TOP LEFT IS 0;0 --- Going left increases x, going down increases y. The value of inter x;y is self.inters[y][x]
    
    def consoleDisplay(self):
        for row in self.inters:
            line = ""
            for inter in row:
                if inter == 1: line += "🟣"
                elif inter == 2: line += "⚪"
                elif inter == 0: line += "＋"
            print(line)
        print()
    
    def setInter(self, x, y, value):
        self.inters[y][x] = value
        
    def move(self, x, y, player):
        
        if x < 0 or x >= self.width or y < 0 or y >= self.height: return False, "ERR: Move not on board"
        if player not in [1,2]: return False, "ERR: Player value invalid"
        if self.inters[y][x] != 0: return False, "ERR: Intersection already occupied"
        
        newInters = deepcopy(self.inters)
        newInters[y][x] = player
        
        def findNeighbours(x,y):
            neighbours = []
            if self.coordsAreInBounds(x-1, y): neighbours.append((x-1,y))
            if self.coordsAreInBounds(x, y-1): neighbours.append((x,y-1))
            if self.coordsAreInBounds(x+1, y): neighbours.append((x+1,y))
            if self.coordsAreInBounds(x, y+1): neighbours.append((x,y+1))
            return neighbours
            
        neighbours = findNeighbours(x,y)
        
        def findChain(x, y): #returns List of all stones members of the chain like this [(x,y),(x,y)(x,y)]
            player = newInters[y][x]
            friends = [[(x,y), 1]]
            newX, newY = x, y
            while True:
                neighbours = findNeighbours(newX,newY)
                for neighbour in neighbours:
                    if newInters[neighbour[1]][neighbour[0]] == player:  
                        if ([neighbour, 0] not in friends) and ([neighbour, 1] not in friends):
                            friends.append([neighbour, 0])
                if friends == []: return []
                for friend in friends:
                    isThereAZero = False
                    if friend[1] == 0:
                        newX, newY = friend[0][0], friend[0][1]
                        friend[1] = 1
                        isThereAZero = True
                        break
                if not isThereAZero: break
            return [friends[i][0] for i in range(len(friends))]
                        
                        
        
        chains = []
        for neighbour in neighbours:
            if self.inters[neighbour[1]][neighbour[0]] != player and self.inters[neighbour[1]][neighbour[0]] != 0: chains.append(findChain(neighbour[0],neighbour[1]))
        
        def interHasLiberties(x, y, inters=newInters):
            if self.coordsAreInBounds(x-1, y):
                if inters[y][x-1] == 0: return True
            if self.coordsAreInBounds(x, y-1): 
                if inters[y-1][x] == 0: return True
            if self.coordsAreInBounds(x+1, y): 
                if inters[y][x+1] == 0: return True
            if self.coordsAreInBounds(x, y+1): 
                if inters[y+1][x] == 0: return True
            return False
        
        for chain in chains:
            libertyInChain = False
            for inter in chain:
                if interHasLiberties(inter[0], inter[1]): libertyInChain = True
            if libertyInChain == False:
                for inter in chain:
                    newInters[inter[1]][inter[0]] = 0
                    
        selfChain = findChain(x,y)
        libertyInChain = False
        for inter in selfChain:
            if interHasLiberties(inter[0], inter[1]): libertyInChain = True
        if libertyInChain == False:
            return False, "ERR: Move is suicidal"
        
        if newInters == self.oldInters: return False, "ERR: Ko"
        self.oldInters = deepcopy(self.inters)
        self.inters = deepcopy(newInters)
        return True, "Success"
        
    def coordsAreInBounds(self, x, y):
        return not (x < 0 or x >= self.width or y < 0 or y >= self.height)
    
if __name__ == "__main__":
    # board = Goban(10,10)
    # board.consoleDisplay()
    # board.setInter(3,1,1)
    # print(board.move(3,1,1))
    pass 
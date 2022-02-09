from ast import While
from time import sleep
import goLogic


print("---WELCOME TO GO.PY---")
print()
while True:
    try :
        width = int(input("Enter width of board : "))
        height = int(input("Enter height of board : "))
        break
    except:
        print("Invalid input, please try again.")
        print()

board = goLogic.Board(width, height)
currentTurn = "Black"

def drawBoard():
    print("\033c", end = "")
    print(f"---{currentTurn} to play---")
    b = board.giveBoard()
    for count, inter in enumerate(b):
        if inter.content == -1:
            print('⚫', end = "")
        if inter.content == 0:
            print('〰', end = "")
        if inter.content == 1:
            print('⚪', end = "")
        if count % width == width-1: print()


while True:
    drawBoard()
    print("Input the x and y coordinates of your move, separated by a space. Top left is 0;0.")
    move = input("> ")
    move = move.split(maxsplit=1)
    try: 
        a = int(move[0]) + int(move[1])
        a = "yes"
    except:
        print("Invalid input, try again.")
        sleep(1)
        a = "no"
    if a == "yes":
        if currentTurn == "Black":
            result = board.move(int(move[0]), int(move[1]), -1)
            if result[0] == False:
                print(result[1])
                sleep(1)
            else: currentTurn = "White"
        elif currentTurn == "White":
            result = board.move(int(move[0]), int(move[1]), 1)
            if result[0] == False:
                print(result[1])
                sleep(1)
            else: currentTurn = "Black"
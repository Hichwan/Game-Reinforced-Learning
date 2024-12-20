#Game Terminal - Othello

import numpy as np
import math
import sys
import pygame

ROW_COUNT = 8
COLUMN_COUNT = 8
SQUARESIZE = 100
CHECK = [[-1,-1], [-1,0], [-1, 1], [0,-1], [0, 1], [1, 1], [1, 0], [1, -1]]

#Parent Class: Player
class Player:
    def __init__(self, name, select):
        self.name = name
        self.select = select
        self.availablemove = {}

    def add(self, move):
        self.availablemove.update({move})
        

#Child Class: Pieces
class Pieces(Player):
    def __init__(self, name, select, score):
        super().__init__(name, select)
        self.score = score

        
#Creates the board with the center pieces already filled
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    board[3][3] = 1
    board[3][4] = 2
    board[4][3] = 2
    board[4][4] = 1
    return board

def valid(board, positionx, positiony, player):
    #Checks to see if position placed down is empty, else return false
    if board[positionx][positiony] != 0:
        return False

    #Creates an opposite    
    if player.select == 1:
        opposite = 2
    else:
        opposite = 1
    #Traverse around the area and sees if there is an opposite
    for dx, dy in CHECK:
            xdirection, ydirection = positionx + dx, positiony + dy
            #Creates a bool for finding the opposite piece
            oppositeCheck = False 

            while 0 <= xdirection < ROW_COUNT and 0 <= ydirection < COLUMN_COUNT:
                if board[xdirection][ydirection] == opposite:
                    #If found an opposite piece, then turns oppositepiece to true
                    oppositeCheck = True

                #Check continues if found an opposite piece until a player piece is found
                elif board[xdirection][ydirection] == player.select and oppositeCheck:
                    return True# only sends back in the single direction if true
                
                #If neither condition is found, breaks out of the loop early and continues to check around the original piece
                else:
                    break
                
                #Increases in the given direction until found
                xdirection += dx
                ydirection += dy
                
    #if board[positionx][positiony] == 0:
    #    return True
    return False

#Places piece where user defined
def drop_piece(board, row, col, player):
    board[row][col] = player.select

    #Adds one to score to include the piece being played
    player.score += 1


#Checks around to see what can be flipped
def flip(board, row, col, player, opponent):   
    if player.select == 1:
        opposite = 2
    else:
        opposite = 1

    for dx, dy in CHECK:
            xdirection, ydirection = row + dx, col + dy
            #Creates a bool for finding the opposite piece
            oppositeCheck = False 
            templist = []
            while 0 <= xdirection < ROW_COUNT and 0 <= ydirection < COLUMN_COUNT:
                if board[xdirection][ydirection] == opposite:
                    #If found an opposite piece, then turns opposite piece to true
                    #Adds the numbers as a turple to the list templist
                    templist.append((xdirection, ydirection))
                    oppositeCheck = True
                    

                #Check continues if found an opposite piece until a player piece is found
                elif board[xdirection][ydirection] == player.select and oppositeCheck:
                    for x,y in templist:
                        #Will go through the templist 
                        board[x, y] = player.select
                        #Adds one to player and subtracts one from opponent with each piece being flipped
                        player.score += 1
                        opponent.score -= 1
                        break

                #If neither condition is found, breaks out of the loop early and continues to check around the original piece
                else:
                    templist.clear()
                    break
                
                #Increases in the given direction until found
                xdirection += dx
                ydirection += dy


#Needs to check board state to see if either the board is full or if there is no more valid moves, then triggers game over condition
def checkBoard(board):
    for i in range(ROW_COUNT):
        for j in range(COLUMN_COUNT):
            if board[i,j] == 0:
                return True
    return False


    

def main():
    #pygame.init()
    width = COLUMN_COUNT * SQUARESIZE
    height = ROW_COUNT * SQUARESIZE

    size = (width, height)
    #screen = pygame.display.set_mode(size)

    #Initialize Board Beginning
    board = create_board()
    game_over = False
    turn = 0
    

#    while not game_over:
#        for event in pygame.event.get():
#           if event.type == pygame.QUIT():
#                sys.exit()
            
#            if event.type == pygame.MOUSEBUTTONDOWN:

    #Asks for name and to choose player
    name = input("What is your name?")
    select = int(input("Choose Player 1 or Player 2"))

    #If they select player 1, then automatically makes the second user player 2
    if select == 1:
        Player_1 = Player(name, select)
        print(Player_1.name)
        print(Player_1.select)
        name = input("What is your name?")
        Player_2 = Player(name, 2)
    else:
        Player_2 = Player(name, select, 2)
        print(Player_2.name)
        print(Player_2.select)
        name = input("What is your name?")
        Player_1 = Player(name, 1, 2)

    Player_1.score = Player_2.score = 2
    
    print(board)
    while not game_over:
        if turn == 0:
            while True:
                col = int(input(f"{Player_1.name}:"))
                row = int(input(f"{Player_1.name}:"))

                if valid(board, row, col, Player_1):
                    drop_piece(board, row, col, Player_1)
                    flip(board, row, col, Player_1, Player_2)
                    break
                print("Invalid Move. Please Choose a Different Spot")
                continue
        else:
            while True:
                col = int(input(f"{Player_2.name}:"))
                row = int(input(f"{Player_2.name}:"))

                if valid(board, row, col, Player_2):
                    drop_piece(board, row, col, Player_2)
                    flip(board,  row, col, Player_2, Player_1)
                    break
                print("Invalid Move. Please Choose a Different Spot")
                continue
        print(board)
        print(Player_1.score)
        print(Player_2.score)
        #At the end, increases the turn counter, if over 2 then gets remainder via modulo 2
        turn = (turn + 1) % 2


if __name__ == "__main__":
    main()
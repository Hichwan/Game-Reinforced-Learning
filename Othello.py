#Game Terminal - Othello

import numpy as np
import math
import sys
import pygame
import random
import tensorflow as tf
from tensorflow.python.keras import layers
from collections import deque

ROW_COUNT = 8
COLUMN_COUNT = 8
SQUARESIZE = 100
CHECK = [[-1,-1], [-1,0], [-1, 1], [0,-1], [0, 1], [1, 1], [1, 0], [1, -1]]

GREEN = (9, 121, 105)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RADIUS = int(SQUARESIZE/2 - 5)


pygame.init()
width = COLUMN_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE

size = (width, height)
screen = pygame.display.set_mode(size)

#Parent Class: Player
class Player:
    def __init__(self, name, select):
        self.name = name
        self.select = select
        self.availablemove = {}
        

#Child Class: Pieces
class Pieces(Player):
    def __init__(self, name, select, score):
        super().__init__(name, select)
        self.score = score

#Reinforced Learning Agent
class LearningAgent:
    def __init__(self, player):
        self.player = player
        self.q_table = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 1.0

    def choose_action(self, state, valid_moves):
        #Using Epsilon greedy policy
        state_tuple = tuple(map(tuple, state))

        valid_move_list = list(valid_moves.keys())
        if random.uniform(0,1) < self.exploration_rate:
            return random.choice(valid_move_list)
        else:
            state_q_values = self.q_table.get(state_tuple,{})
            return max(valid_move_list, key = lambda move: state_q_values.get(move,0))
        
    def update_q_values(self, state, action, reward, next_state):
        state_tuple = tuple(map(tuple, state))
        next_state_tuple = tuple(map(tuple, next_state))

        best_next_action = max(self.q_table.get(next_state_tuple, {}).values(), default=0)

        if state_tuple not in self.q_table:
            self.q_table[state_tuple] = {}

        if action not in self.q_table[state_tuple]:
            self.q_table[state_tuple][action] = 0

        self.q_table[state_tuple][action] = (1 - self.learning_rate) * self.q_table.get(state_tuple, {}).get(action, 0) + self.learning_rate * (reward + self.discount_factor * best_next_action)
    def calculate_reward(self, game, action, player, opponent):
        if action not in player.availablemove:
            return -1

        if not checkBoard(player, opponent):
            winner = self.winner(player, opponent)
            if winner == player:
                return 10000
            elif game.winner(player) is None:
                return 0
            else:
                return -100
            
        else:
            return player.score - opponent.score


#Creates the board with the center pieces already filled
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    board[3][3] = 2
    board[3][4] = 1
    board[4][3] = 1
    board[4][4] = 2
    return board

def draw_board(board):
    for row in range(ROW_COUNT):
        for column in range(COLUMN_COUNT):
            pygame.draw.rect(screen, GREEN, (column*SQUARESIZE, row*SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.rect(screen, BLACK, (column*SQUARESIZE, row*SQUARESIZE, SQUARESIZE, SQUARESIZE),2)

            if board[row][column] == 1:
                pygame.draw.circle(screen, BLACK, (int(column*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)

            if board[row][column] == 2:
                pygame.draw.circle(screen, WHITE, (int(column*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


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

def update_all_valid_moves(board, player1, player2):
    player1.availablemove.clear()
    player2.availablemove.clear()
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if valid(board, row, col, player1):
                player1.availablemove[(row, col)] = True
            if valid(board, row, col, player2):
                player2.availablemove[(row, col)] = True


#Places piece where user defined
def drop_piece(board, row, col, player, opponent):
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
def checkBoard(player1, player2):
    if player1.score == 0 or player2.score == 0:
        return False

    if not player1.availablemove and not player2.availablemove:
        return False
    
    return True   

def winner(Player_1, Player_2):
    if Player_1.score > Player_2.score:
        return "Player 1"
    elif Player_1.score < Player_2.score:
        return "Player 2"
    else:
        return "Draw"

#AI against self?
def AItrain(agent_1,agent_2, episodes):
    for _ in range(episodes):
        board = create_board()
        game_over = False
        turn = 0


    Player_1 = Player(name = "AI PLAYER 1", select = 1)
    Player_2 = Player(name = "AI PLAYER 2", select = 2)
    Player_1.score = Player_2.score = 2


    while not game_over:
        update_all_valid_moves(board, Player_1, Player_2)

        if not checkBoard(Player_1, Player_2):
            game_over = True
            break

        if turn == 0:
            valid_moves = Player_1.availablemove
            action = agent_1.choose_action(board, valid_moves)
            drop_piece(board, *action, Player_1, Player_2)
            flip(board, *action, Player_1, Player_2)
            reward = agent_1.calculate_reward(board, action, Player_1, Player_2)
            agent_1.update_q_values(board, action, reward, board)
            turn = 1
        else:
            valid_moves = Player_2.availablemove
            action = agent_2.choose_action(board, valid_moves)
            drop_piece(board, *action, Player_2, Player_1)
            flip(board, *action, Player_2, Player_1)
            reward = agent_2.calculate_reward(board, action, Player_2, Player_1)
            agent_2.update_q_values(board, action, reward, board)
            turn = 0

        print(board)
        print(Player_1.score)
        print(Player_2.score)
    final_winner = winner(Player_1, Player_2)
    print(f"{final_winner}")



#Player versus AI
def PvA():
    board = create_board()
    game_over = False
    turn = 0

    #Asks for name and to choose player
    name = input("What is your name?")
    select = int(input("Choose Player 1 or Player 2"))
    #If they select player 1, then automatically makes the second user player 2
    if select == 1:
        Player_1 = Player(name, select)
        print(Player_1.name)
        print(Player_1.select)
        opponent = LearningAgent(player = 2)
        Player_2 = Player(name = "AI PLAYER 2", select = 2)
#    else:
 #       Player_2 = Player(name, select, 2)
  #      print(Player_2.name)
   #     print(Player_2.select)
    #    Player_1 = Player("AI PLAYER", 1)

    Player_1.score = Player_2.score = 2

    #Prints gameboard initially
    draw_board(board)
    pygame.display.update()
    print(board)
    while not game_over:
        update_all_valid_moves(board, Player_1, Player_2)
        if not checkBoard(Player_1, Player_2):
            game_over = True
            print("Game Over")
            draw_board(board)
            pygame.display.update()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                posy = event.pos[1]
                row = int(math.floor(posy/SQUARESIZE))
                if turn == 0:
                        if valid(board, row, col, Player_1):
                            drop_piece(board, row, col, Player_1, Player_2)
                            flip(board, row, col, Player_1, Player_2)
                            turn = 1
                        else:
                            print("Invalid Move. Please Choose a Different Spot")
                else:             
                    valid_moves = Player_2.availablemove
                    action = opponent.choose_action(board, valid_moves)
                    drop_piece(board, *action, Player_2, Player_1)
                    flip(board, *action, Player_2, Player_1)
                    reward = opponent.calculate_reward(board, action, Player_2, Player_1)
                    opponent.update_q_values(board, action, reward, board)
                    turn = 0

                print(board)
                print(Player_1.score)
                print(Player_2.score)
        #At the end, increases the turn counter, if over 2 then gets remainder via modulo 2
        draw_board(board)

    final_winner = winner(Player_1, Player_2)
    print(f"{final_winner}")

#Player versus Player
def PvP():
#Initialize Board Beginning
    board = create_board()
    game_over = False
    turn = 0

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
        Player_1 = Player(name, 1)

    Player_1.score = Player_2.score = 2

    #Prints gameboard initially
    draw_board(board)
    pygame.display.update()
    print(board)
    while not game_over:
        update_all_valid_moves(board, Player_1, Player_2)
        if not checkBoard(Player_1, Player_2):
            game_over = True
            print("Game Over")
            draw_board(board)
            pygame.display.update()
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))
                posy = event.pos[1]
                row = int(math.floor(posy/SQUARESIZE))
                if turn == 0:
                    if valid(board, row, col, Player_1):
                        drop_piece(board, row, col, Player_1, Player_2)
                        flip(board, row, col, Player_1, Player_2)
                        turn = 1
                    else:
                        print("Invalid Move. Please Choose a Different Spot")
                else:             
                    if valid(board, row, col, Player_2):
                        drop_piece(board, row, col, Player_2, Player_1)
                        flip(board,  row, col, Player_2, Player_1)
                        turn = 0
                    else:
                        print("Invalid Move. Please Choose a Different Spot")

                print(board)
                print(Player_1.score)
                print(Player_2.score)
        #At the end, increases the turn counter, if over 2 then gets remainder via modulo 2
        draw_board(board)

    final_winner = winner(Player_1, Player_2)
    print(f"{final_winner}")


def main(): 
    mode = input("CHOOSE GAME MOVE: 1 - PvP, 2 - AI V AI Train, 3 - AI V PLAYER")

    if mode == '1':
        PvP()

    elif mode == '2':
        agent_1 = LearningAgent(player = 1)
        agent_2 = LearningAgent(player = 2)
        AItrain(agent_1, agent_2, episodes = 1000)

    elif mode == '3':
        PvA()

if __name__ == "__main__":
    main()


''' 
    print(board)
    while not game_over:
        update_all_valid_moves(board, Player_1, Player_2)
        if not checkBoard(Player_1, Player_2):
            game_over = True
            print("Game Over")
            break
        if turn == 0:
            while True:
                col = int(input(f"{Player_1.name}:"))
                row = int(input(f"{Player_1.name}:"))

                if valid(board, row, col, Player_1):
                    drop_piece(board, row, col, Player_1, Player_2)
                    flip(board, row, col, Player_1, Player_2)
                    break
                print("Invalid Move. Please Choose a Different Spot")
                continue
        else:
            while True:
                col = int(input(f"{Player_2.name}:"))
                row = int(input(f"{Player_2.name}:"))

                if valid(board, row, col, Player_2):
                    drop_piece(board, row, col, Player_2, Player_1)
                    flip(board,  row, col, Player_2, Player_1)
                    break
                print("Invalid Move. Please Choose a Different Spot")
                continue

        print(board)
        print(Player_1.score)
        print(Player_2.score)
        #At the end, increases the turn counter, if over 2 then gets remainder via modulo 2
        turn = (turn + 1) % 2



        if event.type == pygame.MOUSEMOTION:
                
                posx, posy = event.pos[0], event.pos[1]
                if turn == 0:
                    pygame.draw.circle(screen, BLACK, (posx, posy), RADIUS)
                else:
                    pygame.draw.circle(screen, WHITE, (posx, posy), RADIUS)
                pygame.display.update()
'''  


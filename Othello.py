#Game Terminal - Ottello?

import numpy as np
import math
import sys
import pygame

ROW_COUNT = 8
COLUMN_COUNT = 8
EVEN = 0
ODD = 1
SQUARESIZE = 100

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    board[3][3] = '1'
    board[3][4] = '2'
    board[4][3] = '2'
    board[4][4] = '1'
    return board

def valid(board, position):
    for i in range(ROW_COUNT):
        if board[i][position] == 0:
            return True
    return False

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def get_next_open_row(board, col):
    for i in range(ROW_COUNT):
        if board[i][col] == 0:
            return i

def flip(board, piece):
    pass

def main():
    pygame.init()
    width = COLUMN_COUNT * SQUARESIZE
    height = ROW_COUNT * SQUARESIZE

    size = (width, height)
    screen = pygame.display.set_mode(size)
    board = create_board()
    game_over = False
    turn = 0


    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT():
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:


                '''
    print(board)
    while not game_over:
        if turn == 0:
            col = int(input("Player 1:"))
            if valid(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
        else:
            col = int(input("Player 2:"))
            if valid(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
        print(board)
        turn = (turn + 1) % 2

'''
if __name__ == "__main__":
    main()
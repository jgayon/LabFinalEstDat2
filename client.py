import pygame
import sys
import math
import socket
import pickle

# Define the colors
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# Define the board dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7

# Create the game board
def create_board():
  board = np.zeros((ROW_COUNT,COLUMN_COUNT))
  return board

# Drop a piece onto the board
def drop_piece(board, row, col, piece):
  board[row][col] = piece

# Check if a location is valid
def is_valid_location(board, col):
  return board[ROW_COUNT-1][col] == 0

# Find the next open row for a column
def get_next_open_row(board, col):
  for r in range(ROW_COUNT):
      if board[r][col] == 0:
          return r

# Check if a player has won the game
def winning_move(board, piece):
  # Check horizontal locations for win
  for c in range(COLUMN_COUNT-3):
      for r in range(ROW_COUNT):
          if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
              return True

  # Check vertical locations for win
  for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT-3):
          if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
              return True

  # Check positively sloped diaganols
  for c in range(COLUMN_COUNT-3):
      for r in range(ROW_COUNT-3):
          if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
              return True

  # Check negatively sloped diaganols
  for c in range(COLUMN_COUNT-3):
      for r in range(3, ROW_COUNT):
          if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
              return True

# Draw the game board
def draw_board(board):
  for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT):
          pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
          pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)

  for c in range(COLUMN_COUNT):
      for r in range(ROW_COUNT):		
          if board[r][c] == 1:
              pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
          elif board[r][c] == 2: 
              pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
  pygame.display.update()

# Initialize the game
board = create_board()
game_over = False
turn = 0

# Initialize Pygame
pygame.init()

# Define the screen size
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)
screen = pygame.display.set_mode(size)

# Draw the game board
draw_board(board)
pygame.display.update()

# Connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 55555))

# Game loop
while not game_over:
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          client.send(pickle.dumps(('QUIT',)))
          pygame.quit()
          sys.exit()
      if event.type == pygame.MOUSEMOTION:
          pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
          posx = event.pos[0]
          if turn == 0:
              pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
          else: 
              pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
      pygame.display.update()
      if event.type == pygame.MOUSEBUTTONDOWN:
          pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
          # Ask for Player 1 Input
          if turn == 0:
              posx = event.pos[0]
              col = int(math.floor(posx/SQUARESIZE))
              if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)
                if winning_move(board, 1):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    game_over = True
                client.send(pickle.dumps(('MOVE', row, col, 1)))
          # Ask for Player 2 Input
          else:				
              posx = event.pos[0]
              col = int(math.floor(posx/SQUARESIZE))
              if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)
                if winning_move(board, 2):
                    label = myfont.render("Player 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True
                client.send(pickle.dumps(('MOVE', row, col, 2)))

# Switch turns
if turn == 0:
  turn = 1
else:
  turn = 0

# Draw the game board
draw_board(board)
pygame.display.update()

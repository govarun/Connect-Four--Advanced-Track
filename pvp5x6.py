import random, copy, pygame
from pygame.locals import *

level = 2 

human = 1
human2 = 2

element_size = 50 # size of each element of board 

clock_speed = 30 # fps for board updation
screen_width = 640 # width of game window
screen_height = 480 # height of game window

board_width = 6 # number of columns
board_height = 5 # number of rows

x_margin = ((screen_width - board_width * element_size) // 2)
y_margin = ((screen_height - board_height * element_size) // 2)

white = (255, 255, 255)

bgcolor = (150,200,150)

pygame.init()
pygame.display.set_caption('Connect 4')
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((screen_width, screen_height))

redtoken_img = pygame.image.load('4row_red.png')
redtoken_img = pygame.transform.scale(redtoken_img, (element_size , element_size ))
blacktoken_img = pygame.image.load('4row_black.png')
blacktoken_img = pygame.transform.scale(blacktoken_img, (element_size, element_size))
element_img = pygame.image.load('4row_board.png')
element_img = pygame.transform.scale(element_img, (element_size, element_size))
arrow_img = pygame.image.load('4row_arrow.png')
human_img = pygame.image.load('image 1.png')
human2_img = pygame.image.load('image 2.png')
tie_img = pygame.image.load('4row_tie.png')


redtoken_rect = pygame.Rect(element_size // 2, screen_height - (3 * element_size // 2), element_size, element_size)
blacktoken_rect = pygame.Rect(screen_width - int(3 * element_size / 2), screen_height - int(3 * element_size / 2), element_size, element_size)
win_rect = human_img.get_rect()
win_rect.center = ((screen_width // 2), (screen_height // 2))
help_rect = arrow_img.get_rect()
help_rect.left = redtoken_rect.right + 10
help_rect.centery = redtoken_rect.centery


def main():
    while True:
        game_loop()                                         



def is_valid(board, col):# checks if move is valid
    if col < 0 or col >= (board_width) or board[col][0] != None:
        return False
    return True


def is_full(board): # checks if board is full
    for x in range(board_width):
        if board[x][0] == None:
            return False
    return True


def make_board():
    board = []
    for x in range(board_width):
        board.append([None] * board_height)
    return board


def check_move(board, player, col):
    lowest = lowest_space(board, col)
    if lowest != -1:
        board[col][lowest] = player


def draw_board(board, extra_token=None):
    game_display.fill(bgcolor)

    # 
    token_rect = pygame.Rect(0, 0, element_size, element_size)
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            if board[x][y] == human:
                game_display.blit(redtoken_img, token_rect)
            elif board[x][y] == human2:
                game_display.blit(blacktoken_img, token_rect)

    # draw the token when in motion
    if extra_token != None:
        if extra_token['turn'] == human:
            game_display.blit(redtoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
        elif extra_token['turn'] == human2:
            game_display.blit(blacktoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))

    # draw board
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            game_display.blit(element_img, token_rect)

    game_display.blit(redtoken_img, redtoken_rect) # draw red token on left
    game_display.blit(blacktoken_img, blacktoken_rect) # draw black token on right 
    #connect4.buttons('Main Menu',50,50,200,50,green,bright_green,30,'Back to menu')


def human_move(board, is_first_move):
    not_dragging = True
    pos_x, pos_y = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and not_dragging and redtoken_rect.collidepoint(event.pos):# start dragging
                not_dragging = False
                pos_x, pos_y = event.pos
            elif event.type == MOUSEMOTION and not not_dragging:# update position while dragging
                pos_x, pos_y = event.pos
            elif event.type == MOUSEBUTTONUP and not not_dragging:# stop dragging
                if pos_y < y_margin and pos_x > x_margin and pos_x < screen_width - x_margin:# drop the token
                    col = int((pos_x - x_margin) / element_size)
                    if is_valid(board, col):
                        move_token(board, col, human)
                        board[col][lowest_space(board, col)] = human
                        draw_board(board)
                        pygame.display.update()
                        return
                pos_x, pos_y = None, None
                not_dragging = True
        if pos_x != None and pos_y != None:
            draw_board(board, {'x':pos_x - int(element_size / 2), 'y':pos_y - (element_size // 2), 'turn':human})
        else:
            draw_board(board)
            
        if is_first_move:
            game_display.blit(arrow_img, help_rect)# show help for first move

        pygame.display.update()
        clock.tick()

def human2_move(board):
    not_dragging = True
    pos_x, pos_y = None, None
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and not_dragging and blacktoken_rect.collidepoint(event.pos):# start dragging
                not_dragging = False
                pos_x, pos_y = event.pos
            elif event.type == MOUSEMOTION and not not_dragging:# update position while dragging
                pos_x, pos_y = event.pos
            elif event.type == MOUSEBUTTONUP and not not_dragging:# stop dragging
                if pos_y < y_margin and pos_x > x_margin and pos_x < screen_width - x_margin:# drop the token
                    col = int((pos_x - x_margin) / element_size)
                    if is_valid(board, col):
                        move_token(board, col, human2)
                        board[col][lowest_space(board, col)] = human2
                        draw_board(board)
                        pygame.display.update()
                        return
                pos_x, pos_y = None, None
                not_dragging = True
        if pos_x != None and pos_y != None:
            draw_board(board, {'x':pos_x - int(element_size / 2), 'y':pos_y - (element_size // 2), 'turn':human2})
        else:
            draw_board(board)
            


        pygame.display.update()
        clock.tick()



def move_token(board, col, player):
    pos_x = x_margin + col * element_size
    pos_y = y_margin - element_size
    speed = 5

    lowestNoneSpace = lowest_space(board, col)

    while True:
        pos_y += speed
        if ((pos_y - y_margin) / element_size) >= lowestNoneSpace:
            return
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':player})
        pygame.display.update()
        clock.tick()


def lowest_space(board, col):# gives the lowest empty row number of specified column 
    for y in range(board_height-1, -1, -1):
        if board[col][y] == None:
            return y
    return -1

def game_loop():
    
    is_help = True
    turn = human

    board = make_board()# make an empty board

    while True: 
        if turn == human:
            human_move(board, is_help)
            if is_help:
                # no help needed after first move has been played
                is_help = False
            if is_win(board, human):
                win_img = human_img
                break
            turn = human2 
        else:
            human2_move(board)
        
            if is_win(board, human2):
                win_img = human2_img
                break
            turn = human 

        if is_full(board):# tie situation
        
            win_img = tie_img
            break

    while True:
        draw_board(board)# display the board till user clicks on screen or exits
        game_display.blit(win_img, win_rect)
        pygame.display.update()
        clock.tick()
        for event in pygame.event.get(): 
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONUP:
                return
    is_help = False




def is_win(board, player):# check if any current board situation leads to winning for any player
    for x in range(board_width - 3):
        for y in range(board_height):
            if board[x][y] == board[x+1][y] == board[x+2][y] == board[x+3][y] == player:
                return True
    
    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] == board[x][y+1] == board[x][y+2] == board[x][y+3] == player:
                return True
    
    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == board[x+1][y-1] == board[x+2][y-2] == board[x+3][y-3] == player:
                return True
    
    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == board[x+1][y+1] == board[x+2][y+2] == board[x+3][y+3] == player:
                return True
    return False


if __name__ == '__main__':
    main()

import random, copy, pygame
from pygame.locals import *

level = 2 

human = 1
computer = 2

element_size = 50 # size of each element of board 

clock_speed = 30 # fps for board updation
screen_width = 640 # width of game window
screen_height = 580 # height of game window

board_width = 8  # number of columns
board_height = 7 # number of rows

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
computer_img = pygame.image.load('image 2.png')
tie_img = pygame.image.load('4row_tie.png')

human_img = pygame.transform.smoothscale(human_img, (340, 80))
computer_img = pygame.transform.smoothscale(computer_img, (340, 80))
tie_img = pygame.transform.smoothscale(tie_img, (100, 80))

redtoken_rect = pygame.Rect(element_size // 2, screen_height - (3 * element_size // 2), element_size, element_size)
blacktoken_rect = pygame.Rect(screen_width - int(3 * element_size / 2), screen_height - int(3 * element_size / 2), element_size, element_size)
win_rect = human_img.get_rect()
win_rect.center = ((screen_width // 2), (screen_height // 10))
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

def draw_board_with_two_extra_tokens(board, extra_token=None, extra_token2=None):
    game_display.fill(bgcolor)

    # draw tokens
    token_rect = pygame.Rect(0, 0, element_size, element_size)
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            if board[x][y] == human:
                game_display.blit(redtoken_img, token_rect)
            elif board[x][y] == computer:
                game_display.blit(blacktoken_img, token_rect)

    # draw the extra token
    if extra_token != None:
        if extra_token['color'] == human:
            game_display.blit(redtoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
        elif extra_token['color'] == computer:
            game_display.blit(blacktoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
    if extra_token2 != None:
        if extra_token2['color'] == human:
            game_display.blit(redtoken_img, (extra_token2['x'], extra_token2['y'], element_size, element_size))
        elif extra_token2['color'] == computer:
            game_display.blit(blacktoken_img, (extra_token2['x'], extra_token2['y'], element_size, element_size))

    # draw board over the tokens
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            game_display.blit(element_img, token_rect)

    # draw the red and black tokens off to the side
    game_display.blit(redtoken_img, redtoken_rect) # red on the left
    game_display.blit(blacktoken_img, blacktoken_rect) # black on the right


def draw_board(board, extra_token=None):
    game_display.fill(bgcolor)

    # 
    token_rect = pygame.Rect(0, 0, element_size, element_size)
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            if board[x][y] == human:
                game_display.blit(redtoken_img, token_rect)
            elif board[x][y] == computer:
                game_display.blit(blacktoken_img, token_rect)

    # draw the token when in motion
    if extra_token != None:
        if extra_token['turn'] == human:
            game_display.blit(redtoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))
        elif extra_token['turn'] == computer:
            game_display.blit(blacktoken_img, (extra_token['x'], extra_token['y'], element_size, element_size))

    # draw board
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            game_display.blit(element_img, token_rect)

    game_display.blit(redtoken_img, redtoken_rect) # draw red token on left
    game_display.blit(blacktoken_img, blacktoken_rect) # draw black token on right 



def human_move(board, is_first_move):
    not_dragging = True
    pos_x, pos_y = None, None
    lx,ly = 0,0 #PS
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
                lx,ly =  animate_probable_position(board, lx, int((pos_x - x_margin) / element_size), color) #PS
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
        if pos_x != None and pos_y != None and lx>=x_margin and lx<=x_margin+(board_width*element_size): #PS
            draw_board_with_two_extra_tokens(board, {'x':lx, 'y':ly, 'color':human}, {'x':pos_x - int(element_size / 2), 'y':pos_y - int(element_size / 2), 'color':human}) #PS
        elif pos_x != None and pos_y != None:
            draw_board(board, {'x':pos_x - int(element_size / 2), 'y':pos_y - (element_size // 2), 'turn':human})
        else:
            draw_board(board)
            
        if is_first_move:
            game_display.blit(arrow_img, help_rect)# show help for first move

        pygame.display.update()
        clock.tick()


def animate_probable_position(board, last_x, col, color):
    if col<0 or col>7:
        return 0, 100
    lowestEmptySpace = lowest_space(board, col)
    new_x = (col*element_size)+x_margin
    new_y = y_margin+(lowestEmptySpace*element_size)
    return new_x,new_y

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

def computer_move(board):
    possible_moves_arr = possible_moves(board, computer, level)
    best_score = -1
    for i in range(board_width):# get the best score based on heuristics
        if possible_moves_arr[i] > best_score and is_valid(board, i):
            best_score = possible_moves_arr[i]
    best_scores_arr = []
    for i in range(len(possible_moves_arr)):
        if possible_moves_arr[i] == best_score and is_valid(board, i):
            best_scores_arr.append(i)# get the first move encountered with this best score 
            break
    if len(best_scores_arr) > 0:
        return best_scores_arr[0]
    else:
        for x in range(board_width):
            if board[x][0] == None:
                return x


def computer_move_animation(board, col):
    pos_x = blacktoken_rect.left
    pos_y = blacktoken_rect.top
    speed = 7
    while pos_y > (y_margin - element_size):# move token up
        pos_y -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':computer})
        pygame.display.update()
        clock.tick()
    pos_y = y_margin - element_size# move token sideways
    speed = 6
    while pos_x > (x_margin + col * element_size):
        pos_x -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'turn':computer})
        pygame.display.update()
        clock.tick()
    # drop the token
    move_token(board, col, computer)




def possible_moves(board, player, depth):
    if depth == 0 or is_full(board):
        return [0] * board_width

    if player == human:
        opponent = computer
    else:
        opponent = human

    possible_moves_arr = [0] * board_width
    for moves in range(board_width):
        copy_board = copy.deepcopy(board)
        if not is_valid(copy_board, moves):
            continue
        check_move(copy_board, player, moves)
        if is_win(copy_board, player):
            possible_moves_arr[moves] = 1.0 # score the winning move
        else: 
            if is_full(copy_board):
                possible_moves_arr[moves] = 0.0
            else:
                for opponent_moves in range(board_width):
                    copy_board2 = copy.deepcopy(copy_board)
                    if not is_valid(copy_board2, opponent_moves):
                        continue
                    check_move(copy_board2, opponent, opponent_moves)
                    if is_win(copy_board2, opponent):# score the losing move
                        possible_moves_arr[moves] = -1.0
                    else:
                        points_arr = possible_moves(copy_board2, player, depth - 1)
                        possible_moves_arr[moves] += (sum(points_arr) / board_width) / board_width# calculate the heuristics based on board depth
    return possible_moves_arr


def lowest_space(board, col):# gives the lowest empty row number of specified column 
    for y in range(board_height-1, -1, -1):
        if board[col][y] == None:
            return y
    return -1

def game_loop():
    
    is_help = True
    if random.randint(0, 1) == 1:# choose who plays the first move
        turn = computer
    else:
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
            turn = computer 
        else:
            col = computer_move(board)
            computer_move_animation(board, col)
            check_move(board, computer, col)
            if is_win(board, computer):
                win_img = computer_img
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

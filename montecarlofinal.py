import random, copy, pygame
from pygame.locals import *

board_width = 7  # how many spaces wide the board is
board_height = 6 # how many spaces tall the board is


level = 2 # how many moves to look ahead. (>2 is usually too much)

element_size = 50 # size of the tokens and individual board spaces in pixels

clock_speed = 30 # frames per second to update the screen
screen_width = 640 # width of the program's window, in pixels
screen_height = 480 # height in pixels

x_margin = int((screen_width - board_width * element_size) / 2)
y_margin = int((screen_height - board_height * element_size) / 2)

white = (255, 255, 255)

bgcolor = (150,200,150)

human = 1
computer = 2

no_of_games = 1000    #for monte carlo    
depth_for_montecarlo = 8    #for monte carlo



pygame.init()
clock = pygame.time.Clock()
game_display = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Four in a Row')

redtoken_rect = pygame.Rect((element_size // 2), screen_height - (3 * element_size // 2), element_size, element_size)
blacktoken_rect = pygame.Rect(screen_width - int(3 * element_size / 2), screen_height - int(3 * element_size / 2), element_size, element_size)
redtoken_img = pygame.image.load('4row_red.png')
redtoken_img = pygame.transform.smoothscale(redtoken_img, (element_size , element_size ))
blacktoken_img = pygame.image.load('4row_black.png')
blacktoken_img = pygame.transform.smoothscale(blacktoken_img, (element_size, element_size))
element_img = pygame.image.load('4row_board.png')
element_img = pygame.transform.smoothscale(element_img, (element_size, element_size))

human_winner_img = pygame.image.load('image 1.png')
human_winner_img = pygame.transform.smoothscale(human_winner_img, (340, 80))

computer_winner_img = pygame.image.load('image 2.png')
computer_winner_img = pygame.transform.smoothscale(computer_winner_img, (340, 80))

tie_img = pygame.image.load('4row_tie.png')
tie_img = pygame.transform.smoothscale(tie_img, (100, 80))
winner_rect = human_winner_img.get_rect()
winner_rect.center = (screen_width // 2, screen_height // 10)

help_img = pygame.image.load('4row_arrow.png')
help_rect = help_img.get_rect()
help_rect.left = redtoken_rect.right + 10
help_rect.centery = redtoken_rect.centery

def main():
    while True:
        game_play()



def game_play():
                
        
    if random.randint(0, 1) == 0:
        turn = computer
    else:
        turn = human
    
    help_show = True
    # Set up a blank board data structure.
    board = new_board()

    while True: # main game loop
        if turn == human:
            # Human player's turn.
            human_move(board, help_show)
            if help_show:
                # turn off help arrow after the first move
                help_show = False
            if is_win(board, human):
                win_img = human_winner_img
                break
            turn = computer # switch to other player's turn
        else:
            # Computer player's turn.
            col = montecarlomove(board)
            computer_animate_effect(board, col)
            check_move(board, computer, col)
            if is_win(board, computer):
                win_img = computer_winner_img
                break
            turn = human # switch to other player's turn

        if is_full(board):
            # A completely filled board means it's a tie.
            win_img = tie_img
            break

    while True:
        # Keep looping until player clicks the mouse or quits.
        draw_board(board)
        game_display.blit(win_img, winner_rect)
        pygame.display.update()
        clock.tick()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONUP:
                return
    help_show = False

    
    
def montecarlomove(board):		##this is the monte carlo function
	possible_moves = [0] * board_width

	board1 = copy.deepcopy(board)  	#to keep the original state of board

	for evalcol in range(board_width):
		
		if lowest_space(board1, evalcol) == -1:
			possible_moves[evalcol] = -100000
			continue

		else:
			lowestrow = lowest_space(board1, evalcol)
			board1[evalcol][lowestrow] = 2
			#board2 = copy.deepcopy(board)
			if currentmove_win(2 , board1, evalcol, lowestrow):  ##if the comp wins after this move
				possible_moves[evalcol] = 100000
				continue

			sum1 = 0
			board2 = copy.deepcopy(board1)	#storing the state of board after one move
			
			for games in range(no_of_games):
				stage = 0
				
				for stage in range(depth_for_montecarlo):
					if is_full(board2):
						break
					
					else:
						if stage%2 == 1:
							
							
							currcol = random.randint(0, board_width-1)
							currrow = lowest_space(board2, currcol)
							while currrow == -1:		#### Check if board gets full
								currcol = random.randint(0, board_width-1)
								currrow = lowest_space(board2, currcol)
							board2[currcol][currrow] = 2

							if currentmove_win(2 , board2, currcol, currrow):  ##
								sum1 += 1*(depth_for_montecarlo - stage)
								break

						else:
							
							
							currcol = random.randint(0, board_width-1)
							currrow = lowest_space(board2, currcol)
							while currrow == -1:		#### Check if board gets full
								currcol = random.randint(0,board_width-1)
								currrow = lowest_space(board2, currcol)
							board2[currcol][currrow] = 1

							if currentmove_win(1, board2, currcol, currrow):  ##
								sum1 -= 1*(depth_for_montecarlo - stage)
								break
		
				
				board2 = copy.deepcopy(board1)
		possible_moves[evalcol] = sum1
		board1 = copy.deepcopy(board)

	maxcol = 0
	maxvalue = possible_moves[maxcol] 

	for col in range(board_width):
		if maxvalue < possible_moves[col]:
			maxvalue = possible_moves[col]
			maxcol = col
	board = copy.deepcopy(board1)
	return maxcol

def currentmove_win(player, board, col, row):
	#code for checking horizontal connections
	if col+3 < board_width:
		if board[col][row] == board[col+1][row] == board[col+2][row] == board[col+3][row] == player:
			return True
	if col-3 >= 0:
		if board[col][row] == board[col-1][row] == board[col-2][row] == board[col-3][row] == player:
			return True
	# code for checking vertical connections
	if row+3 < board_height:
		if board[col][row] == board[col][row+1] == board[col][row+2] == board[col][row+3] == player:		
			return True
	if row-3 >= 0:
		if board[col][row] == board[col][row-1] == board[col][row-2] == board[col][row-3] == player:
			return True
	# code for checking diagonal connections
	
	if row+3 < board_height and col+3 < board_width:
		if board[col][row] == board[col+1][row+1] == board[col+2][row+2] == board[col+3][row+3] == player:		
			return True
	if row+3 < board_height and col-3 >= 0:
		if board[col][row] == board[col-1][row+1] == board[col-2][row+2] == board[col-3][row+3] == player:		
			return True
	if row-3 >= 0 and col+3 < board_width:
		if board[col][row] == board[col+1][row-1] == board[col+2][row-2] == board[col+3][row-3] == player:		
			return True
	if row-3 >= 0 and col-3 >= 0:
		if board[col][row] == board[col-1][row-1] == board[col-2][row-2] == board[col-3][row-3] == player:		
			return True
	return False
    
    
def check_move(board, player, col):
    lowest = lowest_space(board, col)
    if lowest != -1:
        board[col][lowest] = player


def draw_board(board, extra_token=None):
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

    # draw board over the tokens
    for x in range(board_width):
        for y in range(board_height):
            token_rect.topleft = (x_margin + (x * element_size), y_margin + (y * element_size))
            game_display.blit(element_img, token_rect)

    # draw the red and black tokens off to the side
    game_display.blit(redtoken_img, redtoken_rect) # red on the left
    game_display.blit(blacktoken_img, blacktoken_rect)

##PS
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


def new_board():
    board = []
    for x in range(board_width):
        board.append([None] * board_height)
    return board


def human_move(board, first_move):
    not_dragging = True
    pos_x, pos_y = None, None
    lx,ly = 0,0 #PS
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and not_dragging and redtoken_rect.collidepoint(event.pos):
                # start of dragging on red token pile.
                not_dragging = False
                pos_x, pos_y = event.pos
            elif event.type == MOUSEMOTION and not not_dragging:
                # update the position of the red token being dragged
                pos_x, pos_y = event.pos
                lx,ly =  animate_probable_position(board, lx, int((pos_x - x_margin) / element_size), color) #PS
            elif event.type == MOUSEBUTTONUP and not not_dragging:
                # let go of the token being dragged
                if pos_y < y_margin and pos_x > x_margin and pos_x < screen_width - x_margin:
                    # let go at the top of the screen.
                    col = int((pos_x - x_margin) / element_size)
                    if isValidMove(board, col):
                        animate_drop_effect(board, col, human)
                        board[col][lowest_space(board, col)] = human
                        draw_board(board)
                        pygame.display.update()
                        return
                pos_x, pos_y = None, None
                not_dragging = True
        if pos_x != None and pos_y != None and lx>=x_margin and lx<x_margin+(board_width*element_size): #PS
            draw_board_with_two_extra_tokens(board, {'x':lx, 'y':ly, 'color':human}, {'x':pos_x - int(element_size / 2), 'y':pos_y - int(element_size / 2), 'color':human}) #PS
        elif pos_x != None and pos_y != None:
            draw_board(board, {'x':pos_x - int(element_size / 2), 'y':pos_y - int(element_size / 2), 'color':human})
        else:
            draw_board(board)
            
        if first_move:
            # Show the help arrow for the player's first move.
            game_display.blit(help_img, help_rect)

        pygame.display.update()
        clock.tick()
##

##PS
def animate_probable_position(board, last_x, col, color):
    if col<0 or col>6:
        return 0, 100
    lowestEmptySpace = lowest_space(board, col)
    new_x = (col*element_size)+x_margin
    new_y = y_margin+(lowestEmptySpace*element_size)
    return new_x,new_y

def animate_drop_effect(board, col, color):
    pos_x = x_margin + col * element_size
    pos_y = y_margin - element_size
    speed = 3.0

    lowestEmptySpace = lowest_space(board, col)

    while True:
        pos_y += int(speed)
        if ((pos_y - y_margin) // element_size) >= lowestEmptySpace:
            return
        draw_board(board, {'x':pos_x, 'y':pos_y, 'color':color})
        pygame.display.update()
        clock.tick()


def computer_animate_effect(board, col):
    pos_x = blacktoken_rect.left
    pos_y = blacktoken_rect.top
    speed = 8
    # moving the black tile up
    while pos_y > (y_margin - element_size):
        pos_y -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'color':computer})
        pygame.display.update()
        clock.tick()
    # moving the black tile over
    pos_y = y_margin - element_size
    speed = 7
    while pos_x > (x_margin + col * element_size):
        pos_x -= speed
        draw_board(board, {'x':pos_x, 'y':pos_y, 'color':computer})
        pygame.display.update()
        clock.tick()
    # dropping the black tile
    animate_drop_effect(board, col, computer)


def make_computer_move(board):
    potentialMoves = minimax(board, computer, level)
    # get the best fitness from the potential moves
    bestMoveFitness = -1
    for i in range(board_width):
        if potentialMoves[i] > bestMoveFitness and isValidMove(board, i):
            bestMoveFitness = potentialMoves[i]
    # find all potential moves that have this best fitness
    bestMoves = []
    for i in range(len(potentialMoves)):
        if potentialMoves[i] == bestMoveFitness and isValidMove(board, i):
            bestMoves.append(i)
    return random.choice(bestMoves)


def minimax(board, tile, lookAhead):
    if lookAhead == 0 or is_full(board):
        return [0] * board_width

    if tile == human:
        enemyTile = computer
    else:
        enemyTile = human

    # Figure out the best move to make.
    potentialMoves = [0] * board_width
    for firstMove in range(board_width):
        dupeBoard = copy.deepcopy(board)
        if not isValidMove(dupeBoard, firstMove):
            continue
        check_move(dupeBoard, tile, firstMove)
        if is_win(dupeBoard, tile):
            # a winning move automatically gets a perfect fitness
            potentialMoves[firstMove] = 1
            break # don't bother calculating other moves
        else:
            # do other player's counter moves and determine best one
            if is_full(dupeBoard):
                potentialMoves[firstMove] = 0
            else:
                for counterMove in range(board_width):
                    dupeBoard2 = copy.deepcopy(dupeBoard)
                    if not isValidMove(dupeBoard2, counterMove):
                        continue
                    check_move(dupeBoard2, enemyTile, counterMove)
                    if is_win(dupeBoard2, enemyTile):
                        # a losing move automatically gets the worst fitness
                        potentialMoves[firstMove] = -1
                        break
                    else:
                        # do the recursive call to minimax()
                        results = minimax(dupeBoard2, tile, lookAhead - 1)
                        potentialMoves[firstMove] += (sum(results) / board_width) / board_width
    return potentialMoves


def lowest_space(board, col):
    # Return the row number of the lowest empty row in the given col.
    for y in range(board_height-1, -1, -1):
        if board[col][y] == None:
            return y
    return -1


def isValidMove(board, col):
    # Returns True if there is an empty space in the given col.
    # Otherwise returns False.
    if col < 0 or col >= (board_width) or board[col][0] != None:
        return False
    return True


def is_full(board):
    # Returns True if there are no empty spaces anywhere on the board.
    for x in range(board_width):
        for y in range(board_height):
            if board[x][y] == None:
                return False
    return True


def is_win(board, tile):
    # check horizontal spaces
    for x in range(board_width - 3):
        for y in range(board_height):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    # check vertical spaces
    for x in range(board_width):
        for y in range(board_height - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    # check / diagonal spaces
    for x in range(board_width - 3):
        for y in range(3, board_height):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True
    # check \ diagonal spaces
    for x in range(board_width - 3):
        for y in range(board_height - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False


if __name__ == '__main__':
    main()

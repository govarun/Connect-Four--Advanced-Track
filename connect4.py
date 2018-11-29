import pygame, time, random
import cvp6x7, pvp5x6, pvp6x7, pvp7x8, cvp7x8, cvp5x6

pygame.init()
display_width = 800
display_height = 600
board_width = 5
board_height = 5
gameDisplay = pygame.display.set_mode((display_width,display_height))
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
blue = (0,0,200)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)
yellow = (244,252,25)
bright_yellow = (179,183,69)


pygame.display.set_caption('Connect4')
clock = pygame.time.Clock()
img = pygame.image.load('connect_4.png')
#boardelement = pygame.image.load('boardelement2.png')
#boardelement = pygame.transform.scale(boardelement,(100,100))
#backgroundimg = pygame.image.load('backimg.png')
#backgroundimg = pygame.transform.scale(backgroundimg,(800,600))


def text_objects(text,font,color):#function to get a rectangle to hold text 
    textSurface = font.render(text,True,color)
    return textSurface,textSurface.get_rect()


def buttons(msg,xcoo,ycoo,w,h,ac,ic,font_size,action = None,board_size = None):#for displaying any button
#Here last parameter represents action to be taken when button
#is pressed and first parameter is the text to be displayed on the button
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if xcoo < mouse[0] < xcoo + w and ycoo < mouse[1] < ycoo + h:
        pygame.draw.rect(gameDisplay, ac, (xcoo,ycoo,w,h))
        if click[0] == 1 and action == 'Play':
            board_choice()
            #game starts after this call when user presses mouse left click
        elif click[0] == 1 and action == 'Quit':#game quit
            pygame.quit()
            quit() 
        elif click[0] == 1 and action == 'Back to menu':
            intro_game()
        elif click[0] == 1 and action == '1 Player' and board_size == 6:
            cvp6x7.main()
        elif click[0] == 1 and action == '1 Player' and board_size == 7:
            cvp7x8.main()
        elif click[0] == 1 and action == '1 Player' and board_size == 5:
            cvp5x6.main()
        
        elif click[0] == 1 and action == '2 Player' and board_size == 6:
            pvp6x7.main()
        elif click[0] == 1 and action == '2 Player' and board_size == 5:
            pvp5x6.main()
        elif click[0] == 1 and action == '2 Player' and board_size == 7:
            pvp7x8.main()
        
        elif click[0] == 1 and action =='BackMenu':
            intro_game()
        elif click[0] == 1 and action=='6 X 7':
            game_choice(6)
            
        elif click[0] == 1 and action == '5 X 6':
            game_choice(5)
        elif click[0] == 1 and action == '7 X 8':
            game_choice(7)
        elif click[0] == 1 and action=='6 X 7ai':
            game_choice(6)
        elif click[0] == 1 and action == '5 X 6ai':
            game_choice(5)
        elif click[0] == 1 and action == '7 X 8ai':
            game_choice(7)
    else:
        pygame.draw.rect(gameDisplay, ic,(xcoo,ycoo,w,h))

    smalltext = pygame.font.Font('freesansbold.ttf',font_size)
    textSurf, textRect = text_objects(msg,smalltext,blue)
    textRect.center = ((xcoo+(w/2)),(ycoo+(h/2)))
    gameDisplay.blit(textSurf,textRect)

def intro_img(x,y,imgname):#to display image
    gameDisplay.blit(imgname,(x,y))

def board_choice():
    gameDisplay.fill(white)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_name = pygame.font.Font('freesansbold.ttf',55)
        TextSurf,TextRect = text_objects('Choose the Board Size',text_name,blue)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf , TextRect)
        
        
        buttons('7 X 8',50,350,200,50,green,bright_green,30,'7 X 8')
        buttons('6 X 7',300,350,200,50,green,bright_green,30,'6 X 7')
        buttons('5 X 6',550,350,200,50,green,bright_green,30,'5 X 6')
        buttons('Main Menu',50,50,200,50,green,bright_green,30,'Back to menu')
        
        pygame.display.update()
        clock.tick(30)
        
def intro_game():#intro page of game
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        
        intro_img(250,0,img)#displaying image at top center
        
        text_name = pygame.font.Font('freesansbold.ttf',115)
        TextSurf,TextRect = text_objects('Connect4',text_name,blue)

        TextRect.center = ((display_width/2),(display_height/2))#position where text has to be displayed
        gameDisplay.blit(TextSurf , TextRect)
        buttons('Connect',150,450,200,50,green,bright_green,30,'Play')#for displaying buttons of play and quit 
        buttons('Quit',550,450,200,50,red,bright_red,30,'Quit')
        #Here last parameter represents action to be taken when button
        #is pressed and first parameter is the text to be displayed on the button
        pygame.display.update()
        clock.tick(30)

def board_choice_ai():
    gameDisplay.fill(white)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_name = pygame.font.Font('freesansbold.ttf',55)
        TextSurf,TextRect = text_objects('Choose the Board Size',text_name,blue)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf , TextRect)

        
        buttons('7 X 8',50,350,200,50,green,bright_green,30,'7 X 8ai')
        buttons('6 X 7',300,350,200,50,green,bright_green,30,'6 X 7ai')
        buttons('5 X 6',550,350,200,50,green,bright_green,30,'5 X 6ai')
        #buttons('Main Menu',50,50,200,50,green,bright_green,30,'Back to menu')

        pygame.display.update()
        clock.tick(30)
        
def game_choice(board_size):
    #gameDisplay.fill(white)
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        text_name = pygame.font.Font('freesansbold.ttf',55)
        TextSurf, TextRect = text_objects('Choose your Game Style',text_name,blue)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        buttons('1 Player',150,450,200,50,green,bright_green,30,'1 Player',board_size)
        buttons('2 Player',550,450,200,50,green,bright_green,30,'2 Player',board_size)
        buttons('Main Menu',50,50,200,50,green,bright_green,30,'Back to menu')
        pygame.display.update()
        clock.tick(30)
        

        


    
        
intro_game()#call to game intro page  
pygame.quit()
quit()

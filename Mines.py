# peak software #
# based from https://www.youtube.com/watch?v=94ylCzrVY90 #


import pygame
from math import floor, comb
from random import randint
import os
from screeninfo import get_monitors

# For the ability to move the start position of the window, mainly for personal use
monitors = get_monitors()
monitor = monitors[1]
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x+200},{monitor.y+200}"

# Initialize pygame
pygame.init()


# Game Constants
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
timer = pygame.time.Clock()



# Game calculations for colours, screen size, box size and font
BLACK = (0,0,0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
smallfont = pygame.font.SysFont('Arial', 20)
scaling = 0.8
SIZEW = floor((WIDTH / 5) * scaling)
SIZEH = floor((HEIGHT / 5) * scaling)

# Game Variables
bet = 0
mult = 1
money = 1000
money_made = 0


# Main Game Function
def game_func():
    global money, money_made, money_made


    # Set the whole screen to black once the game is reset  
    screen.fill("black")
    # Start Button Coords
    start_button = pygame.Rect(WIDTH - 100, HEIGHT/2 - 100, 70, 50)
 
    # More Game Variables
    run = True
    bet = -1

    safe_count = 0
    accept = False
    start = False
    cashouting = False


    # Getting the amount of mines
    while not accept:
        mines = int(input("how many mines? (1-24): "))
        if mines > 24 or mines < 1:
            print("try again")
        else:
            accept = True

    # Getting the wager
    while bet <= 0 or bet > money:
        bet = int(input(f"How much you wanna bet? you have £{money}: ")) 


    # The game in a 2D array
    game = [[2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2],
            [2,2,2,2,2]]


    # Creating the random Mines Based from the "mines" variable
    count = 0
    while count <= mines-1:
        x = randint(0,4)
        y = randint(0,4)
        if game[y][x] != 3:
            game[y][x] = 3
            
        else:
            count -= 1
        count+=1

    # To prevent you clicking on the same tile over and over again
    game_rep = game
    game_rep2 = game

    # Main Game Loop
    while run:
        timer.tick(FPS)

        # Checking the events that have happened
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()


            # Check if left mouse button is pressed
            if ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse = pygame.mouse.get_pos()


                # Taking the bet money away
                if (WIDTH - 100 <= mouse[0] <= WIDTH - 30 and HEIGHT/2 - 100 <= mouse[1] <= HEIGHT/2 - 50) and not start and not cashouting:
                    money -= bet
                    start = True
                
                # Giving the Money to the user
                if (WIDTH - 100 <= mouse[0] <= WIDTH - 30) and (HEIGHT/2 - 150 <= mouse[1] <= HEIGHT/2 - 100) and cashouting:
                    money += money_made
                    pygame.draw.rect(screen, BLACK, (WIDTH/2, HEIGHT-50, 100, 50))
                    total_money = smallfont.render(f"£{money}", True, WHITE)
                    screen.blit(total_money, (WIDTH/2, HEIGHT-50))

                    for i in range(5):
                        for j in range(5):
                                
                            if game_rep2[i][j] == 2:
                                pygame.draw.rect(screen, WHITE, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))
                                    
                            elif game_rep2[i][j] == 3 or game_rep2[i][j] == False:
                                pygame.draw.rect(screen, RED, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))

                    pygame.display.update()
                    pygame.time.wait(100)
                    game_func()
                    

                # Calculating the square clicked on then applying a colour
                if (mouse[0] <= WIDTH * scaling and mouse[1] <= HEIGHT * scaling) and start:
                    
                    X_Square = floor(mouse[0] / SIZEW)
                    Y_Square = floor(mouse[1] / SIZEH)


                    # Mine
                    if game[Y_Square][X_Square] == 3 and game_rep[Y_Square][X_Square] != False:
                        game_rep[Y_Square][X_Square] = False
                        #pygame.draw.rect(screen, RED, (X_Square*SIZEW, Y_Square*SIZEH, SIZEW, SIZEH))
                        cashouting = True
                        start = False
                        money_made = 0

                        for i in range(5):
                            for j in range(5):
                                
                                if game_rep2[i][j] == 2:
                                    pygame.draw.rect(screen, WHITE, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))
                                    
                                elif game_rep2[i][j] == 3 or game_rep2[i][j] == False:
                                    pygame.draw.rect(screen, RED, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))

                        pygame.display.update()
                        pygame.time.wait(100)
                        game_func()


                    # Safe Tile
                    elif game[Y_Square][X_Square] == 2 and game_rep[Y_Square][X_Square] != True:
                        game_rep[Y_Square][X_Square] = True
                        cashouting = True
                        start = True
                        safe_count += 1
                        
                        pygame.draw.rect(screen, WHITE, (X_Square*SIZEW, Y_Square*SIZEH, SIZEW, SIZEH))
                        



        # Money made (Green button on top to the right)
        prob = comb(25 - mines, safe_count) / comb(25, safe_count)
        
        if safe_count >= 1:
            # Calculation for the multiplier to add to the money
            mult = round(0.97 * (1/(prob)), 2)
        else:
            mult = 0
        money_made = (bet*mult)

        pygame.draw.rect(screen, GREEN, (WIDTH - 100, HEIGHT/2 - 150, 70, 50))
        cash = smallfont.render(f"{money_made}", True, BLACK)
        screen.blit(cash, (WIDTH - 100, HEIGHT/2 - 150))


        #Start Button
        pygame.draw.rect(screen, GREEN, start_button)
        if not start and not cashouting:
            pygame.draw.rect(screen, GREEN, start_button)
            start_text = smallfont.render("start", True, BLACK)
            screen.blit(start_text, (WIDTH - 100, HEIGHT/2 - 100))
        else:
            pygame.draw.rect(screen, BLACK, start_button)



        # Tjhe bars on the screen
        for i in range(6):
            pygame.draw.line(screen, GREY, (SIZEH*i, 0), (SIZEH*i, HEIGHT-(SIZEH+33)))
            pygame.draw.line(screen, GREY, (0, SIZEW*i), (WIDTH-(SIZEW+33), SIZEW*i))
                


        # Money at bottom of screen
        total_money = smallfont.render(f"£{money}", True, WHITE)
        screen.blit(total_money, (WIDTH/2, HEIGHT-50))


        probability = smallfont.render(f"{round(prob*100, 2)}%", True, WHITE)
        screen.blit(probability, (WIDTH/2 - 100, HEIGHT-50))

        total_mines = smallfont.render(f"{mines} mines", True, WHITE)
        screen.blit(total_mines, (WIDTH/2, HEIGHT - 100))

        mult_text = smallfont.render(f"{mult}x", True, WHITE)
        screen.blit(mult_text, (WIDTH/2 + 150, HEIGHT-50))
        if randint(1, 25) == 1:
            pygame.draw.rect(screen, BLACK, (0, HEIGHT-70, WIDTH, 50))

        pygame.display.flip()


game_func()
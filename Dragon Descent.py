# Dragon Tower #

# https://stakecommunity.com/topic/51591-dragon-tower-multiplier/

import pygame
from random import randint
import os
from screeninfo import get_monitors
from math import floor
from copy import deepcopy

monitors = get_monitors()
monitor = monitors[1]
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x+200},{monitor.y+200}"


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
timer = pygame.time.Clock()

pygame.display.set_caption("Dragon Descent")

BLACK = (0,0,0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
smallfont = pygame.font.SysFont('Arial', 20)

mult = 1 #(base multiplier**level) * .98
money_made = 0


# easy base = 4/3 -> 4 tiles 1 bad
# mid = 3/2 -> 3 tiles 1 bad
# hard = 2 ->  2 tiles 1 bad
# expert  = 3 -> 3 tiles 2 bad
# master = 4 -> 4 tiles 3 bad


easy = [[2,2,2,2],  # 1
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        ]

medium = [[2,2,2],  # 2
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        ]

hard = [[2,2],  # 3
        [2,2],
        [2,2],
        [2,2],
        [2,2],
        [2,2],
        [2,2],
        [2,2],
        [2,2],
        ]

expert = [[2,2,2],  # 4
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        [2,2,2],
        ]


master = [[2,2,2,2],   # 5
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        [2,2,2,2],
        ]




game_choice = [easy, medium, hard, expert,  master]

money = 1000


def create_board(game, mode):
    count = 0
    for i in range(9):
        count = 0
        length = len(game[0]) - 1
        if mode <= 3:
            game[i][randint(0,length)] = 3   
        else:
            while count < mode-2:
                random_int = randint(0,length)
                if game[i][random_int] != 3:
                    game[i][random_int] = 3 
                else:
                    count -= 1
                count += 1
    return game


def game_func():
    global mode, money, money_made
    screen.fill(BLACK)
    mode = 0
    bet = -1
    run = True
    end = False
    
    while mode <= 0 or mode > 24:
        mode = int(input("1-easy, 2-medium, 3-hard, 4-expert, 5-master"))

    game = deepcopy(game_choice[mode-1])
    
    while bet <= 0 or bet > money:
        bet = float(input(f"how much will you bet? you have £{money}: "))

    create_board(game, mode)

    
    level = 0

    MAX_WIDTH = 600
    MAX_HEIGHT = 805
    SIZEH = floor(MAX_HEIGHT/9)
    SIZEW = floor(MAX_WIDTH/len(game[0]))
    
    base_mult = mode**2 - 2*mode + 9
    if base_mult == 17:
        base_mult += 1
    
    base_mult = base_mult/6




    money -= bet

    while run:
        timer.tick(FPS)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not end:



                mouse = pygame.mouse.get_pos()


                if mouse[0] <= 600:
                    SQUAREX = floor(mouse[0] / SIZEW)
                    SQUAREY = floor(mouse[1] / SIZEH)

                    if game[SQUAREY][SQUAREX] == 2 and SQUAREY == level:
                        pygame.draw.rect(screen, WHITE, (SQUAREX*SIZEW, SQUAREY*SIZEH, SIZEW, SIZEH))
                        level += 1
                    
                    elif game[SQUAREY][SQUAREX] == 3 and SQUAREY == level:
                        pygame.draw.rect(screen, RED, (SQUAREX*SIZEW, SQUAREY*SIZEH, SIZEW, SIZEH))
                        pygame.display.update()
                        end = True
                        #level += 1
                    
                if (650 <= mouse[0] <= 725) and (HEIGHT/2 - 50 <= mouse[1] <= HEIGHT/2) and money_made > 0:
                    money += money_made
                    end = True
                    
            if end:
                print(end)
                for i in range(9):
                    for j in range(len(game[0])):
                        if game[i][j] == 2:
                            pygame.draw.rect(screen, WHITE, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))
                        else:
                            pygame.draw.rect(screen, RED, (j*SIZEW, i*SIZEH, SIZEW, SIZEH))
                
                pygame.time.wait(300)
                pygame.display.update()
                game_func()

            if level >= 9:
                mult = round((base_mult**(level)) * 0.98, 2)
                money_made = bet * mult
                money += money_made
                
                pygame.draw.rect(screen, BLACK, (601, 0, 300, HEIGHT))
                total_money = smallfont.render(f"£{money}", True, WHITE)
                screen.blit(total_money, (650, 0))
                end = True



        if level != 0:
            mult = round((base_mult**(level)) * 0.98, 2)
        else:
            mult = 0


        money_made = bet * mult

        
        for i in range(9):
            for j in range(len(game[0])+1):
                pygame.draw.line(screen, GREY, (SIZEW*j, 0), (SIZEW*j, HEIGHT))
                pygame.draw.line(screen, GREY, (0, SIZEH*i), (MAX_WIDTH, SIZEH*i))


        pygame.draw.rect(screen, GREEN, (650, HEIGHT/2 - 50,75, 50))
        cashout = smallfont.render(f"£{round(money_made, 2)}", True, BLACK)
        screen.blit(cashout, (650, HEIGHT/2 - 50))

        total_money = smallfont.render(f"£{round(money, 2)}", True, WHITE)
        screen.blit(total_money, (650, 0))
        
        if randint(1, 25) == 1:
            pygame.draw.rect(screen, BLACK, (601, 0, 300, HEIGHT))




        pygame.display.flip()


game_func()
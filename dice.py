# Dice

import pygame
from math import floor, comb
from random import randint
import os
from screeninfo import get_monitors


monitors = get_monitors()
monitor = monitors[1]
os.environ['SDL_VIDEO_WINDOW_POS'] = f"{monitor.x+200},{monitor.y+200}"


pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
timer = pygame.time.Clock()

BLACK = (0,0,0)
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
smallfont = pygame.font.SysFont('Arial', 20)


# 99/prob of win
# or 100/prob of win * 0.99

money = 1000
winCount = 0
lossCount = 0
def game_func():
    global money, winCount, lossCount
    run = True
    x = 0
    OFFSET = 80
    bar_length = ((WIDTH - OFFSET) / 100)
    win_chance = -1
    bet = -1
    while win_chance <= 0 or win_chance >= 100:
        win_chance = float(input("What chance do you want to have at winning? "))
        mult = 99/win_chance    
    
    
    while bet <= 0 or bet > money:
        bet = float(input(f"how much do you want to bet? (you have £{money}): "))


    while run:
        timer.tick(FPS)
        screen.fill(BLACK)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run = False
                pygame.quit()
                
            if ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse = pygame.mouse.get_pos()

                if (WIDTH/2 <= mouse[0] <= WIDTH/2 + 70) and (100 <= mouse[1] <= 150) and bet <= money:
                    x = randint(0, 10000) / 100
                    money -= bet
                    if x <= win_chance:
                        winCount += 1
                        money += bet*mult
                    else:
                        lossCount += 1
                
                if (100 <= mouse[0] <= 250) and (HEIGHT - 75 <= mouse[1] <= HEIGHT + 75):
                    win_chance = 0
                    while win_chance <= 0 or win_chance >= 100:
                        win_chance = float(input("What chance do you want to have at winning? "))
                        mult = 99/win_chance    
                
                if (WIDTH - 100 <= mouse[0] <= WIDTH - 15) and (HEIGHT - 75 <= mouse[1] <= HEIGHT - 25):
                    bet = -1
                    while bet <= 0 or bet > money:
                        bet = float(input(f"how much do you want to bet? (you have £{money}): "))
        

        pygame.draw.rect(screen, WHITE, (OFFSET/2, HEIGHT/2, bar_length*x, 50))
        
        roll = smallfont.render(f"{x}", True, WHITE)
        screen.blit(roll, (bar_length*x, HEIGHT/2 - 30))

        total_money = smallfont.render(f"£{round(money, 2)}", True, WHITE)
        screen.blit(total_money, (WIDTH/2, 50))
        
        # roll button
        pygame.draw.rect(screen, GREEN, (WIDTH/2, 100, 70, 50))
        roll_text = smallfont.render(f"roll", True, BLUE)
        screen.blit(roll_text, (WIDTH/2 + 17, 100))
        
        
        # Button to change win_chance
        pygame.draw.rect(screen, GREEN, (100, HEIGHT - 75, 150, 30))
        NewChance = smallfont.render("new roll chance?", True, BLUE)
        screen.blit(NewChance, (100, HEIGHT - 75))
        
        # Button to chance bet
        pygame.draw.rect(screen, GREEN, (WIDTH - 100, HEIGHT - 75, 85, 50))
        NewBet = smallfont.render("New bet?", True, BLUE)
        screen.blit(NewBet, (WIDTH-100, HEIGHT-75))
        
        # statistics
        money_to_make = smallfont.render(f"+£{bet*mult}", True, WHITE)
        screen.blit(money_to_make, (20, HEIGHT - 20))
        
        win_count = smallfont.render(f"{winCount}", True, WHITE)
        screen.blit(win_count, (WIDTH/2 - 70, 100))

        loss_count = smallfont.render(f"{lossCount}", True, WHITE)
        screen.blit(loss_count, (WIDTH/2 - 110, 100))
        
        net_profit = round(money-1000, 2)
        if net_profit >= 0:
            netProfit = smallfont.render(f"+£{net_profit} this session", True, WHITE)
        else:
            netProfit = smallfont.render(f"-£{abs(net_profit)} this session", True, WHITE)
        
        screen.blit(netProfit, (200, HEIGHT - 20))    
        
            
        pygame.display.flip()


game_func()
import pygame
import random
import math
import tkinter as tk
from tkinter import messagebox
from Classes import Characters
import sys

def Start_Game(numOfSkeleton):
    
    pygame.init()

    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sword Fight")
    background_image = pygame.image.load("floor_black.jpg")
    Box=pygame.image.load("Box.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(background_image, (0, 0))
    player = Characters.Player("pablo.png", 100, 100, 100, 0.1)
    img=""
    if numOfSkeleton==1:
        img="last enemy.png"
        screen.blit(Box, (800, 10))
        BoxImage = pygame.image.load('Box.png') 
        Boximage_rect = BoxImage.get_rect(topleft=(400,0))
        screen.blit(BoxImage,Boximage_rect)
    else:
        img="normal enemy.png"
        

    yellow_objects = []
    for _ in range(numOfSkeleton):
        yellow_object = Characters.YellowObject(img, 80, random.randint(500, 700), random.randint(100, 500), 0.1)
        yellow_objects.append(yellow_object)

    
    font = pygame.font.Font(None, 36)
    timer_start = pygame.time.get_ticks()
    timer_seconds = 0
    
    # Main loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Display a dialog box asking the user if they want to exit the game
                root = tk.Tk()
                root.withdraw()
                response = messagebox.askyesno("Exit", "Do you want to exit the game?")
                if response:
                    running = False  # Terminate the game loop when the user chooses to exit
                    pygame.quit()    # Quit Pygame before exiting
                    sys.exit()
                    
        
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        
       
        for yellow_object in yellow_objects:
            yellow_object.sense_and_move(player)
            yellow_object.move()

           
            if yellow_object.hit(player):
                player.health -= 10
                if player.health <= 0:
                    print("Player is dead!")
                   

            
            if keys[pygame.K_SPACE]:
                if player.hit(yellow_object.line_end_point):
                    yellow_object.health -= 10
                    if yellow_object.health <= 0:
                        yellow_objects.remove(yellow_object)
                        print("Yellow object is dead!")

       
        screen.blit(background_image, (0, 0))
        
        
        player.draw(screen)
        for yellow_object in yellow_objects:
            yellow_object.draw(screen)
            
            if player.distance_to(yellow_object) < 100:
                pygame.draw.line(screen, (255, 0, 0), player.center(), yellow_object.center(), 5)

        
        timer_seconds = (pygame.time.get_ticks() - timer_start) // 1000
        timer_text = font.render(f"Time: {timer_seconds}", True, (255, 255, 255))
        screen.blit(timer_text, (10, 10))
        
        
        for i in range(player.health // 25):
            pygame.draw.circle(screen, (255, 0, 0), (30 + 25 * i, SCREEN_HEIGHT - 30), 10)

        # Update the display
        pygame.display.flip()

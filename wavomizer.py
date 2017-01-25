from wavomizer.main import Main
import pygame
import cProfile

pygame.init()
game = Main()
#cProfile.run('game.main_loop()')
game.main_loop()

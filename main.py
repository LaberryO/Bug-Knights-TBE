import os, pygame, sys, time, random;
import pygame.locals;

from Resource import Entity
from Resource import Exception
from Resource import System

class Game:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        pygame.init()
        pygame.display.set_caption("Bug Knights TB Edition")

        self.clock = pygame.time.Clock()
        screen_instance = System.Screen(1600, 800)
        self.display = pygame.display.set_mode(screen_instance.size)

        self.inGame = True

        self.prevTime = time.time()

    def reset(self):
        pass
        
    def title(self):
        pass

    def update(self, deltaTime):
        pass

    def run(self):
        while self.inGame:
            now = time.time()
            deltaTime = now - self.prevTime
            self.prevTime = now
            
            self.display.fill(System.Color.white)
            self.update(deltaTime)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()

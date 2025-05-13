import os, pygame, sys, time, random;
import pygame.locals;

from Resource import Entity
from Resource import Exception
from Resource import System

class Game:
    def __init__(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        pygame.display.set_caption("Bug Knights 3")

        self.clock = pygame.time.Clock()
        self.screen = System.Screen(1600, 800)
        self.display = pygame.display.set_mode(self.screen.size)

        self.inGame = True
        self.defaultFont = pygame.font.Font("Resource/Font/GowunDodum-Regular.ttf", 24)
        self.titleFont = pygame.font.Font("Resource/Font/GowunDodum-Regular.ttf", 48)

        self.prevTime = time.time()

    def reset(self):
        pass

    def createButtons(self, buttonTexts, mousePos, x, y, facing):
        buttons = []

        for i, text in enumerate(buttonTexts):
            btnRect = pygame.Rect(0, 0, 250, 60)
            if facing == "vertical":
                btnRect.center = (x, y + i * 80)
            elif facing == "horizontal":
                btnRect.center = (x + i * 80, y)

            mousePos = pygame.mouse.get_pos()

            isHover = btnRect.collidepoint(mousePos)
            bgColor = System.Color.gray if isHover else System.Color.white
            textColor = System.Color.white if isHover else System.Color.black

            btnSurface = self.defaultFont.render(text, True, textColor)
            buttons.append((btnSurface, btnRect, text, bgColor))

        return buttons;
        
    def title(self):
        from Resource.Data import title_data
        self.display.fill(System.Color.white)

        mousePos = pygame.mouse.get_pos();

        titleText = self.titleFont.render(title_data.titleTexts, True, System.Color.black)
        self.display.blit(titleText, (self.screen.centerX - titleText.get_width() // 2, self.screen.centerY // 2 - titleText.get_height() // 2))

        buttonTexts = title_data.buttonTexts
        buttons = self.createButtons(buttonTexts, mousePos, self.screen.centerX, self.screen.height - self.screen.centerY // 2, "horizontal")
        
        for surface, rect, _, bgColor in buttons:
            pygame.draw.rect(self.display, bgColor, rect, border_radius=10)
            pygame.draw.rect(self.display, System.Color.black, rect, 3, border_radius=10)

            self.screen.blit(surface, (
                rect.centerx - surface.get_width() // 2,
                rect.centery - surface.get_height() // 2
            ))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False

    def calculateDeltaTime(self):
        now = time.time()
        deltaTime = now - self.prevTime
        self.prevTime = now
        return deltaTime
    
    def game(self):
        pass

    def gameOver(self):
        pass

    def run(self):
        while self.inGame:
            self.state = "title"
            deltaTime = self.calculateDeltaTime()
            
            if self.state == "title":
                self.title()
            elif self.state == "game":
                self.game()
            elif self.state == "gameOver":
                self.gameOver()

            pygame.display.update()

    def update(self, deltaTime):
        pass

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

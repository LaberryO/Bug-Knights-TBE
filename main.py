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
        btnWidth = 250
        btnHeight = 60
        spacing = 20  # 버튼 간격

        totalWidth = len(buttonTexts) * btnWidth + (len(buttonTexts) - 1) * spacing
        totalHeight = len(buttonTexts) * btnHeight + (len(buttonTexts) - 1) * spacing

        if facing == "horizontal":
            startX = x - (totalWidth // 2)
            for i, text in enumerate(buttonTexts):
                btnRect = pygame.Rect(startX + i * (btnWidth + spacing), y - btnHeight // 2, btnWidth, btnHeight)
                isHover = btnRect.collidepoint(mousePos)
                bgColor = System.Color.gray if isHover else System.Color.white
                textColor = System.Color.white if isHover else System.Color.black

                btnSurface = self.defaultFont.render(text, True, textColor)
                button = {
                    "id": i,                # 버튼 고유값 (인덱스)
                    "rect": btnRect,        # 버튼 위치와 크기
                    "text": text,           # 버튼 텍스트
                    "bgColor": bgColor,     # 버튼 배경색
                    "textColor": textColor, # 버튼 텍스트 색상
                    "surface": btnSurface   # 버튼 렌더링 표면
                }
                buttons.append(button)

        elif facing == "vertical":
            startY = y - (totalHeight // 2)
            for i, text in enumerate(buttonTexts):
                btnRect = pygame.Rect(x - btnWidth // 2, startY + i * (btnHeight + spacing), btnWidth, btnHeight)
                isHover = btnRect.collidepoint(mousePos)
                bgColor = System.Color.gray if isHover else System.Color.white
                textColor = System.Color.white if isHover else System.Color.black

                btnSurface = self.defaultFont.render(text, True, textColor)
                button = {
                    "id": i,                # 버튼 고유값 (인덱스)
                    "rect": btnRect,        # 버튼 위치와 크기
                    "text": text,           # 버튼 텍스트
                    "bgColor": bgColor,     # 버튼 배경색
                    "textColor": textColor, # 버튼 텍스트 색상
                    "surface": btnSurface   # 버튼 렌더링 표면
                }
                buttons.append(button)

        return buttons

    def title(self):
        from Resource.Data import title_data
        self.display.fill(System.Color.white)

        mousePos = pygame.mouse.get_pos();

        titleText = self.titleFont.render(title_data.titleTexts, True, System.Color.black)
        self.display.blit(titleText, (self.screen.centerX - titleText.get_width() // 2, self.screen.centerY // 2 - titleText.get_height() // 2))

        buttonTexts = title_data.buttonTexts
        buttons = self.createButtons(
            buttonTexts, 
            mousePos, 
            self.screen.centerX, 
            self.screen.height - self.screen.centerY // 2, 
            "horizontal"
        )
        
        for button in buttons:
            rect = button["rect"]
            bgColor = button["bgColor"]
            surface = button["surface"]

            # 버튼 배경 그리기
            pygame.draw.rect(self.display, bgColor, rect, border_radius=10)
            # 버튼 테두리 그리기 (검정색)
            pygame.draw.rect(self.display, System.Color.black, rect, 3, border_radius=10)

            # 텍스트 렌더링
            self.display.blit(
                surface, 
                (
                    rect.centerx - surface.get_width() // 2,
                    rect.centery - surface.get_height() // 2
                )
            )
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        match button["id"]:
                            case 0:
                                self.state = "game"
                            case 1:
                                self.state = "gameInfo"
                            case 2:
                                print("quit")
                                self.state = "quit"

    def calculateDeltaTime(self):
        now = time.time()
        deltaTime = now - self.prevTime
        self.prevTime = now
        return deltaTime
    
    def game(self):
        pass

    def gameOver(self):
        pass

    def gameInfo(self):
        pass

    def run(self):
        self.state = "title"
        while self.inGame:
            self.deltaTime = self.calculateDeltaTime()
            
            if self.state == "title":
                self.title()
            elif self.state == "game":
                self.game()
            elif self.state == "gameOver":
                self.gameOver()
            elif self.state == "gameInfo":
                self.gameInfo()
            elif self.state == "quit":
                break

            pygame.display.update()

    def update(self):
        pass

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

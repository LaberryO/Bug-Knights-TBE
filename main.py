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

        self.images = {}
        self.monsters = {}

        self.turn = "player_turn"
        self.stage = ""

    def reset(self):
        self.monsters = {}
        self.monsters["fboss"] = Entity.Fboss(self.screen, self.images)
        self.monsters["slime"] = Entity.Slime(self.screen, self.images)
        self.player = Entity.Player(self.screen, self.images)
        self.display = pygame.display.set_mode(self.screen.size)

    def createButtons(self, buttonTexts, mousePos, x, y, facing, maxPerRow):
        buttons = []
        btnWidth = int(self.screen.width * 0.15625)
        btnHeight = int(self.screen.height * 0.06666)
        spacing = 20  # 버튼 간격

        if facing == "horizontal":
            rows = (len(buttonTexts) + maxPerRow - 1) // maxPerRow  # 필요한 줄 수
            totalHeight = rows * btnHeight + (rows - 1) * spacing
            startY = y - (totalHeight // 2)

            for i, text in enumerate(buttonTexts):
                row = i // maxPerRow
                col = i % maxPerRow

                totalWidth = maxPerRow * btnWidth + (maxPerRow - 1) * spacing
                startX = x - (totalWidth // 2)

                btnX = startX + col * (btnWidth + spacing)
                btnY = startY + row * (btnHeight + spacing)

                btnRect = pygame.Rect(btnX, btnY, btnWidth, btnHeight)
                isHover = btnRect.collidepoint(mousePos)
                bgColor = System.Color.gray if isHover else System.Color.white
                textColor = System.Color.white if isHover else System.Color.black

                btnSurface = self.defaultFont.render(text, True, textColor)
                button = {
                    "id": i,
                    "rect": btnRect,
                    "text": text,
                    "bgColor": bgColor,
                    "textColor": textColor,
                    "surface": btnSurface
                }
                buttons.append(button)

        elif facing == "vertical":
            totalHeight = len(buttonTexts) * btnHeight + (len(buttonTexts) - 1) * spacing
            startY = y - (totalHeight // 2)

            for i, text in enumerate(buttonTexts):
                btnY = startY + i * (btnHeight + spacing)
                btnRect = pygame.Rect(x - btnWidth // 2, btnY, btnWidth, btnHeight)
                isHover = btnRect.collidepoint(mousePos)
                bgColor = System.Color.gray if isHover else System.Color.white
                textColor = System.Color.white if isHover else System.Color.black

                btnSurface = self.defaultFont.render(text, True, textColor)
                button = {
                    "id": i,
                    "rect": btnRect,
                    "text": text,
                    "bgColor": bgColor,
                    "textColor": textColor,
                    "surface": btnSurface
                }
                buttons.append(button)

        return buttons


    def title(self):
        from Resource.Data import title_data
        self.display.fill(System.Color.white)

        mousePos = pygame.mouse.get_pos()
        image = self.images["title_0"]
        titleText = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.display.blit(titleText, (self.screen.centerX - titleText.get_width() // 2, self.screen.centerY // 2 - titleText.get_height() // 2))

        buttonTexts = title_data.buttonTexts
        buttons = self.createButtons(
            buttonTexts, 
            mousePos, 
            self.screen.centerX, 
            self.screen.height - self.screen.centerY // 2, 
            "horizontal",
            4
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
                                self.state = "gameSettings"
                            case 3:
                                self.state = "quit"

    def calculateDeltaTime(self):
        now = time.time()
        deltaTime = now - self.prevTime
        self.prevTime = now
        return deltaTime
    
    def gameSettings(self):
        from Resource.Data import settings_data
        self.display.fill(System.Color.white)

        mousePos = pygame.mouse.get_pos()
        image = self.images["settings_0"]
        imageSurface = pygame.transform.scale(image, (self.display.get_width(), self.display.get_height()))
        self.display.blit(imageSurface, (0, 0))

        buttonTexts = settings_data.buttonTexts
        buttons = self.createButtons(
            buttonTexts, 
            mousePos, 
            self.screen.centerX, 
            self.screen.centerY, 
            "horizontal",
            4
        )
        
        for button in buttons:
            rect = button["rect"]
            bgColor = button["bgColor"]
            surface = button["surface"]

            if button["id"] == 3:
                bgColor = System.Color.redorange

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
                                self.screen.width = 1920
                                self.screen.height = 1080
                                self.reset()
                            case 1:
                                self.screen.width = 1600
                                self.screen.height = 900
                                self.reset()
                            case 2:
                                self.screen.width = 1280
                                self.screen.height = 720
                                self.reset()
                            case 3:
                                self.state = "title"
    
    def game(self):
        self.handleEvents()

        if self.stage == "fboss":
            background = "bossbackground_0"
            monster = "fboss"
        else:
            background = "background_0"
            monster = "slime"


        self.display.blit(pygame.transform.scale(self.images[background], self.screen.size), (0, 0))
        self.update(self.deltaTime)
        self.player.draw(self.display, self.deltaTime)
        self.monsters[monster].draw(self.display, self.deltaTime)

        pygame.display.update()

    def update(self, deltaTime):
        pass

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False
                pygame.quit()
                sys.exit()

    def gameOver(self):
        pass

    def gameInfo(self):
        pass

    def run(self):
        self.load()

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
            elif self.state == "gameSettings":
                self.gameSettings()
            elif self.state == "quit":
                break

            pygame.display.update()

    def load(self):
        folder_path = "Resource/Images"
        for filename in os.listdir(folder_path):
            self.loadingScreen()
            if filename.lower().endswith(".png"):
                image_path = os.path.join(folder_path, filename)
                filename = filename.split(".")[0]
                try:
                    image = pygame.image.load(image_path)
                    self.images[filename] = image
                    print(f"Image Load Complete: {filename}")
                except pygame.error:
                    print(f"Image Load Failed: {filename}")
            time.sleep(0.02)
        self.reset()

    def loadingScreen(self):
        self.display.fill(System.Color.white)
        loadText = self.titleFont.render("Loading...", True, System.Color.black)
        self.display.blit(loadText, (self.screen.centerX - loadText.get_width() // 2, self.screen.centerY - loadText.get_height() // 2))

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()

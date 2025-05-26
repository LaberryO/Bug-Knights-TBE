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
        self.fullscreen = False

        self.inGame = True
        self.defaultFont = pygame.font.Font("Resource/Font/GowunDodum-Regular.ttf", 24)
        self.titleFont = pygame.font.Font("Resource/Font/GowunDodum-Regular.ttf", 48)

        self.prevTime = time.time()

        self.images = {}
        self.monsters = {}
        self.effects = []

        self.turn = "player_turn"
        self.stage = ""

    def reset(self):
        self.monsters = {}
        self.monsters["fboss"] = Entity.Fboss(self.screen, self.images)
        self.monsters["slime"] = Entity.Slime(self.screen, self.images)
        self.player = Entity.Player(self.screen, self.images)
        if self.fullscreen:
            self.display = pygame.display.set_mode(self.screen.size, pygame.FULLSCREEN)
        else:
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
    
    def gameMenu(self):
        from Resource.Data import menu_data
        # 반투명 배경
        alphaSurface = pygame.Surface(self.screen.size, pygame.SRCALPHA)
        alphaSurface.fill((0, 0, 0, 128))
        self.display.blit(alphaSurface, (0, 0))

        running = True
        while running:
            mousePos = pygame.mouse.get_pos()
            buttonTexts = menu_data.buttonTexts
            buttons = self.createButtons(
                buttonTexts,
                mousePos,
                self.screen.centerX,
                self.screen.centerY,
                "vertical",
                1
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
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button["rect"].collidepoint(event.pos):
                            match button["id"]:
                                case 0:
                                    running = False
                                case 1:
                                    self.state = "title"
                                    running = False
                                case 2:
                                    self.state = "quit"
                                    running = False
            
            pygame.display.flip()
    
    def gameSettings(self):
        from Resource.Data import settings_data
        # Monitor Size
        import tkinter as tk
        root = tk.Tk()
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
            elif button["id"] == 4:
                if self.fullscreen:
                    bgColor = System.Color.green
                else:
                    bgColor = System.Color.red

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
                            case 4:
                                if not self.fullscreen:
                                    self.screen.width = root.winfo_screenwidth()
                                    self.screen.height = root.winfo_screenheight()
                                    self.fullscreen = not self.fullscreen
                                else:
                                    self.fullscreen = not self.fullscreen
                                    self.reset()
                                    self.screen.width = 1600
                                    self.screen.height = 900
                                self.reset()
    
    def game(self):
        from Resource.Data import game_data
        from Resource.Data import fight_data
        mousePos = pygame.mouse.get_pos()
        buttons = self.createButtons(
            game_data.buttonTexts, 
            mousePos,
            self.screen.centerX,
            self.screen.centerY + self.screen.centerY // 2,
            "horizontal",
            4
        )

        self.handleEvents()

        if self.stage == "fboss":
            background = "bossbackground_0"
            monster = "fboss"
        else:
            background = "background_0"
            monster = "slime"

        # Background
        self.display.blit(pygame.transform.scale(self.images[background], self.screen.size), (0, 0))

        # Render
        self.player.draw(self.display, self.deltaTime)
        self.monsters[monster].draw(self.display, self.deltaTime)
        healthText = self.defaultFont.render(f"Player: {self.player.health}/100, {monster}: {self.monsters[monster].health}/100", True, System.Color.green)
        self.display.blit(healthText, (self.screen.centerX // 2, self.screen.centerY))

        # Effect
        frameWidth = 64
        frameHeight = 64

        def tintSurface(surface, color):
            tinted = surface.copy()
            tinted.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)  # 기존 색 제거
            tinted.fill(color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)  # 색상 추가
            return tinted

        EFFECT_FRAMES = {
            "slash": [
                tintSurface(self.images["skill_effect_slash"].subsurface(pygame.Rect(i * frameWidth, 0, frameWidth, frameHeight)), System.Color.red) for i in range(4)
            ],
            "pierce": [
                tintSurface(self.images["skill_effect_pierce"].subsurface(pygame.Rect(i * frameWidth, 0, frameWidth, frameHeight)), System.Color.red) for i in range(5)
            ],
            "smash": [
                tintSurface(self.images["skill_effect_smash"].subsurface(pygame.Rect(i * frameWidth, 0, frameWidth, frameHeight)), System.Color.red) for i in range(3)
            ],
        }

        for effect in self.effects:
            effect.update()

        self.effects = [e for e in self.effects if not e.finished]

        for effect in self.effects:
            effect.draw(self.display)

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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        match button["id"]:
                            case 0:
                                self.player.attack(self.monsters[monster], fight_data.attackType[0])
                                self.effects.append(System.Effect(self.monsters[monster].x, self.monsters[monster].y, EFFECT_FRAMES["slash"]))
                            case 1:
                                self.player.attack(self.monsters[monster], fight_data.attackType[1])
                                self.effects.append(System.Effect(self.monsters[monster].x, self.monsters[monster].y, EFFECT_FRAMES["pierce"]))
                            case 2:
                                self.player.attack(self.monsters[monster], fight_data.attackType[2])
                                self.effects.append(System.Effect(self.monsters[monster].x, self.monsters[monster].y, EFFECT_FRAMES["smash"]))

        pygame.display.update()

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.inGame = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.gameMenu()

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

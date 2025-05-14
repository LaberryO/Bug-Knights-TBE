import pygame

class Monster:
    def __init__(self, screen, images):
        self.width = 200
        self.height = 200
        self.x = screen.centerX + screen.centerX // 3
        self.y = screen.centerY // 2
        self.health = 100
        
        self.matchFile = ""
        self.images = {key: value for key, value in images.items() if key.startswith(self.matchFile)}

        self.currentFrame = 0
        self.frameTime = 0.0 # 누적 시간 저장
        self.frameInterval = 0.16 # 초 기준

    def draw(self, display, deltaTime):
        self.frameTime += deltaTime
        if self.frameTime >= self.frameInterval:
            self.frameTime = 0
            self.currentFrame = (self.currentFrame + 1) % len(self.images)
        display.blit(pygame.transform.scale(self.images[f"{self.matchFile}{self.currentFrame}"], (self.width, self.height)), (self.x - self.width // 2, self.y - self.height // 2))

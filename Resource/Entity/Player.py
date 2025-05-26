from Resource.Data import player_data
from Resource.Data import fight_data
import pygame, random

class Player:
    def __init__(self, screen, images):
        self.width = player_data.size
        self.height = player_data.size
        self.x = screen.centerX - screen.centerX // 3
        self.y = screen.centerY // 2 - 25
        self.health = 100
        self.armorType = fight_data.armorType[0]

        self.images = {key: value for key, value in images.items() if key.startswith("standing")}

        self.currentFrame = 0
        self.frameTime = 0.0 # 누적 시간 저장
        self.frameInterval = 0.16 # 초 기준

    def draw(self, display, deltaTime):
        self.frameTime += deltaTime
        if self.frameTime >= self.frameInterval:
            self.frameTime = 0
            self.currentFrame = (self.currentFrame + 1) % len(self.images)
        display.blit(pygame.transform.scale(self.images[f"standing_{self.currentFrame}"], (self.width, self.height)), (self.x - self.width // 2, self.y - self.height // 2))

    def attack(self, target, type):
        print("Player's Attack")
        damage = random.randint(9, 15)
        if type == fight_data.attackType[0]:
            if target.armorType == fight_data.armorType[0]:
                damage -= damage // 3
        elif type == fight_data.attackType[1]:
            if target.armorType == fight_data.armorType[1]:
                damage -= damage // 3      
        elif type == fight_data.attackType[2]:
            if target.armorType == fight_data.armorType[2]:
                damage -= damage // 3
        target.health -= damage
from .Monster import Monster
from Resource.Data import fight_data
import random

class Fboss(Monster):
    def __init__(self, screen, images):
        super().__init__(screen, images)
        self.matchFile = "fboss_"
        self.images = {key: value for key, value in images.items() if key.startswith(self.matchFile)}
        self.armorType = fight_data.armorType[0]
    
    def draw(self, display, deltaTime):
        super().draw(display, deltaTime)

    def attack(self, target, type):
        print("Fboss's Attack")
        damage = random.randint(9, 15)
        if type == fight_data.attackType[0]:
            if target.armorType == fight_data.armorType[0]:
                damage //= 3
        elif type == fight_data.attackType[1]:
            if target.armorType == fight_data.armorType[1]:
                damage //= 3
        elif type == fight_data.attackType[2]:
            if target.armorType == fight_data.armorType[2]:
                damage //= 3
        target.health -= damage
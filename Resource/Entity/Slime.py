from .Monster import Monster
from Resource.Data import fight_data

class Slime(Monster):
    def __init__(self, screen, images):
        super().__init__(screen, images)
        self.width += 100
        self.height += 100
        self.y -= 25
        self.matchFile = "slime_"
        self.images = {key: value for key, value in images.items() if key.startswith(self.matchFile)}
        self.armorType = fight_data.armorType[2]
    
    def draw(self, display, deltaTime):
        super().draw(display, deltaTime)
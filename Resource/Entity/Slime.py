from .Monster import Monster

class Slime(Monster):
    def __init__(self, screen, images):
        super().__init__(screen, images)
        self.width += 100
        self.height += 100
        self.y -= 25
        self.matchFile = "slime_"
        self.images = {key: value for key, value in images.items() if key.startswith(self.matchFile)}
    
    def draw(self, display, deltaTime):
        super().draw(display, deltaTime)
from .Monster import Monster

class Fboss(Monster):
    def __init__(self, screen, images):
        super().__init__(screen, images)
        self.matchFile = "fboss_"
        self.images = {key: value for key, value in images.items() if key.startswith(self.matchFile)}
    
    def draw(self, display, deltaTime):
        super().draw(display, deltaTime)
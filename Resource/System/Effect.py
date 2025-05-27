import pygame

class Effect:
    def __init__(self, x, y, frames, frame_duration=12):
        self.x = x
        self.y = y
        self.frames = frames
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_duration = frame_duration
        self.finished = False

    def update(self):
        if self.finished:
            return

        self.frame_timer += 1
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0
            self.frame_index += 1
            if self.frame_index >= len(self.frames):
                self.finished = True

    def draw(self, display):
        if not self.finished:
            frame = self.frames[self.frame_index]
            w,h = frame.get_size()
            w *= 5
            h *= 5
            frame = pygame.transform.scale(frame, (int(w), int(h)))
            display.blit(frame, (self.x - w // 2, self.y - h // 3))

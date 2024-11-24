import pygame
from flappy.constants import SPRITE_PIPES
from collections import deque
import random

class Pipes:
    DISTANCE_BETWEEN = 500
    SPACE_BETWEEN = 250

    def __init__(self, window_size):
        self.pipe_image = pygame.image.load(SPRITE_PIPES)
        self.pipe_rect = self.pipe_image.get_rect()
        self.window_size = window_size
        self.pipes = deque()
        self.spawn_timer = 0
        self.spawn_interval = 40

    def pipe_velocity(self):
        return Pipes.DISTANCE_BETWEEN / self.spawn_interval

    def add_pipe_pair(self):
        top_pipe = self.pipe_rect.copy()
        top_pipe.x = self.window_size[0]
        top_pipe.y = random.randint(-800, -200)

        bottom_pipe = self.pipe_rect.copy()
        bottom_pipe.x = self.window_size[0]
        bottom_pipe.y = top_pipe.y + self.pipe_image.get_height() + Pipes.SPACE_BETWEEN

        self.pipes.append((top_pipe, bottom_pipe))

    def update(self):
        for top, bottom in self.pipes:
            top.x -= self.pipe_velocity()
            bottom.x -= self.pipe_velocity()

        if self.pipes and self.pipes[0][0].right < 0:
            self.pipes.popleft()

        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.add_pipe_pair()
            self.spawn_timer = 0

    def draw(self, screen):
        for top, bottom in self.pipes:
            screen.blit(pygame.transform.flip(self.pipe_image, False, True), top)
            screen.blit(self.pipe_image, bottom)
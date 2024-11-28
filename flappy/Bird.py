from PIL import Image, ImageSequence
from collections import namedtuple
import pygame
from flappy.constants import SPRITE_BIRD

class Bird:
    window_size = None

    IMAGE = namedtuple('image', ['frame', 'rect'])
    def __init__(self, window_size):
        Bird.window_size = window_size
        self.current_frame = 0
        self.images = Bird.__loadGIF(SPRITE_BIRD)
        self.frame_count = len(self.images)


    @staticmethod
    def __pilImageToSurface(pilImage):
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    @staticmethod
    def __loadGIF(filename):
        def make_frame(image):
            pygame_image = pygame.transform.scale(Bird.__pilImageToSurface(image), (100, 73))
            rect = pygame.transform.scale(Bird.__pilImageToSurface(image), (100, 20)).get_rect()
            rect.center = (Bird.window_size[0] // 6, Bird.window_size[1] // 2)
            return Bird.IMAGE(pygame_image, rect)

        pilImage = Image.open(filename)
        frames = []
        if pilImage.format == 'GIF' and pilImage.is_animated:
            for frame in ImageSequence.Iterator(pilImage):
                frames.append(make_frame(frame.convert('RGBA')))
        else:
            frames.append(make_frame(pilImage))
        return frames

    def move(self, pos):
        rect = self.images[self.current_frame].rect
        rect.centery = (pos - 0.5) * 1.5 * Bird.window_size[1] + Bird.window_size[1] / 2
        rect.y = max(0, min(rect.y, Bird.window_size[1] - rect.height))

    def draw(self, screen):
        screen.blit(*self.images[self.current_frame])
        self.current_frame = (self.current_frame + 1) % self.frame_count

    @property
    def rect(self):
        return self.images[self.current_frame].rect
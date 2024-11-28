from PIL import Image, ImageSequence
from collections import namedtuple
import pygame
from pygame.rect import RectType

from flappy.constants import SPRITE_BIRD

IMAGE = namedtuple('image', ['frame', 'rect'])
class Bird:
    window_size = None


    def __init__(self, window_size: tuple[int, int]):
        Bird.window_size = window_size
        self.current_frame = 0
        self.images: list[IMAGE] = Bird.__loadGIF(SPRITE_BIRD)
        self.frame_count = len(self.images)


    @staticmethod
    def __pilImageToSurface(pilImage):
        mode, size, data = pilImage.mode, pilImage.size, pilImage.tobytes()
        return pygame.image.fromstring(data, size, mode).convert_alpha()

    @staticmethod
    def __loadGIF(filename) -> list[IMAGE]:
        def make_frame(image) -> IMAGE:
            pygame_image = pygame.transform.scale(Bird.__pilImageToSurface(image), (100, 73))
            rect = pygame_image.get_rect()
            rect.center = (Bird.window_size[0] // 6, Bird.window_size[1] // 2)
            return IMAGE(pygame_image, rect)

        pil_image: Image = Image.open(filename)
        frames: list[IMAGE] = []
        if pil_image.format == 'GIF' and pil_image.is_animated:
            for frame in ImageSequence.Iterator(pil_image):
                frames.append(make_frame(frame.convert('RGBA')))
        else:
            frames.append(make_frame(pil_image))
        return frames

    def move(self, pos):
        rect = self.images[self.current_frame].rect
        rect.centery = (pos - 0.5) * 1.5 * Bird.window_size[1] + Bird.window_size[1] / 2
        rect.y = max(0, min(rect.y, Bird.window_size[1] - rect.height))

    def draw(self, screen):
        screen.blit(*self.images[self.current_frame])
        self.current_frame = (self.current_frame + 1) % self.frame_count

    @property
    def rect(self)->RectType:
        return self.images[self.current_frame].rect

    @property
    def frame(self):
        return self.images[self.current_frame].frame
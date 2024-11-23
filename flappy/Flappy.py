import time
import random
import pygame
import cv2 as cv
import mediapipe as mp
from collections import deque, namedtuple
from PIL import Image, ImageSequence


SPRITE_PIPES = "images/pipe.png"

SPRITE_BIRD = "images/pterodactyl.gif"


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
            pygame_image = pygame.transform.scale(Bird.__pilImageToSurface(image), (75, 55))
            rect = pygame_image.get_rect()
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


class FaceTracker:
    def __init__(self):
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5,
        )
        self.video_capture = cv.VideoCapture(0)

    def get_face_position(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return None, None

        frame = cv.flip(frame, 1)
        results = self.face_mesh.process(cv.cvtColor(frame, cv.COLOR_BGR2RGB))

        if results.multi_face_landmarks:
            landmark = results.multi_face_landmarks[0].landmark[94]
            return landmark.y, frame
        return None, frame

    def release(self):
        self.video_capture.release()
        cv.destroyAllWindows()


class FlappyFaceGame:
    def __init__(self):
        pygame.init()
        icon = pygame.image.load('images/pterodactyl.png')
        pygame.display.set_icon(icon)
        info_object = pygame.display.Info()
        self.face_tracker = FaceTracker()
        self.window_size = (
            info_object.current_w,
            info_object.current_h
        )
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_WIDTH,info_object.current_w)
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, info_object.current_h)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Flappy Bird with Face Tracking")

        self.bird = Bird(self.window_size)
        self.pipes = Pipes(self.window_size)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("Helvetica Bold", 40)
        self.running = True
        self.score = 0
        self.stage = 1
        self.last_stage_time = time.time()
        self.leaderboard = []
        self.logo = pygame.image.load("images/logo.png")

    def display_text(self, text, position, color=(0, 0, 0)):
        rendered_text = self.font.render(text, True, color)
        rect = rendered_text.get_rect(center=position)
        self.screen.blit(rendered_text, rect)


    def check_collisions(self):
        for top, bottom in self.pipes.pipes:
            if self.bird.rect.colliderect(top) or self.bird.rect.colliderect(bottom):
                self.running = False

    def update_score(self):
        checker = True
        for top, bottom in self.pipes.pipes:
            if top.left <= self.bird.rect.x <= top.right:
                checker = False
                if not hasattr(self, "did_update_score") or not self.did_update_score:
                    self.score += 1
                    self.did_update_score = True
            self.screen.blit(self.pipes.pipe_image, bottom)
            self.screen.blit(pygame.transform.flip(self.pipes.pipe_image, False, True), top)
        if checker:
            self.did_update_score = False

    def game_loop(self):
        self.running = True
        self.score = 0
        self.stage = 1
        self.pipes.pipes.clear()
        self.pipes.spawn_timer = 0

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()

            face_position, frame = self.face_tracker.get_face_position()

            if frame is not None:
                frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                self.screen.blit(frame_surface, (0, 0))

            if face_position is not None:
                self.bird.move(face_position)

            self.pipes.update()
            self.check_collisions()
            self.update_score()
            self.bird.draw(self.screen)
            self.pipes.draw(self.screen)

            self.display_text(f"Score: {self.score}", (100, 50))
            self.display_text(f"Stage: {self.stage}", (100, 100))

            if time.time() - self.last_stage_time > 10:
                self.stage += 1
                self.pipes.spawn_interval *= 5 / 6
                self.last_stage_time = time.time()

            pygame.display.flip()
            self.clock.tick(60)

        # Add score to leaderboard
        self.leaderboard.append(self.score)

    def cleanup(self):
        self.face_tracker.release()
        pygame.quit()

    def run(self):
        self.game_loop()
        return self.score


def run_game():
    game = FlappyFaceGame()
    try:
        score = game.run()
    finally:
        game.cleanup()
    return score

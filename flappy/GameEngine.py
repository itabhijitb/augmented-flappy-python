import time
import pygame
import cv2 as cv
from pygame import SurfaceType
from pygame.mixer import SoundType
from pygame.rect import RectType

from flappy.LoadingBar import LoadingBar
from flappy.Bird import Bird
from flappy.Pipes import Pipes
from flappy.FaceTracker import FaceTracker
from flappy.constants import (
    ICON,
    LOGO_IMAGE_PATH,
    FLYING_SOUND,
    CRASH_SOUND,
    GAME_OVER_LOGO_PATH)


class GameEngine:
    def __init__(self):
        self.loading_bar: LoadingBar = LoadingBar()
        pygame.init()
        self.loading_bar(10, "Loading assets...")
        self.crash_sound: SoundType = pygame.mixer.Sound(CRASH_SOUND)
        pygame.display.set_icon(pygame.image.load(ICON))
        info_object = pygame.display.Info()
        self.window_size = (
            info_object.current_w,
            info_object.current_h
        )
        self.logo: SurfaceType = pygame.image.load(LOGO_IMAGE_PATH)
        self.font = pygame.font.SysFont("Helvetica Bold", 30)
        scaled_width = int(self.window_size[0] * 0.25)
        scaled_height = int(self.window_size[1] * 0.25)
        self.game_over_logo = pygame.transform.scale(pygame.image.load(GAME_OVER_LOGO_PATH),
                                                     (scaled_width, scaled_height))
        self.loading_bar(20, "Setting up face tracker...")
        self.face_tracker = FaceTracker()
        self.loading_bar(50, "Determining camera resolution...")
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_WIDTH, info_object.current_w)
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, info_object.current_h)
        self.loading_bar(60, "Setting screen resolution...")
        camera_resolution = (
            self.face_tracker.video_capture.get(cv.CAP_PROP_FRAME_WIDTH),
            self.face_tracker.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT),
        )
        self.loading_bar(70, "Setting mode...")
        if self.window_size > camera_resolution:
            self.window_size = camera_resolution
            self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME)
        else:
            self.screen = pygame.display.set_mode(self.window_size)
        self.loading_bar(80, "Initializing game components...")
        pygame.display.set_caption("Flappy Bird with Face Tracking")

        self.bird = Bird(self.window_size)
        self.pipes = Pipes(self.window_size)
        self.clock = pygame.time.Clock()

        self.loading_bar(90, "Finalizing...")
        self.running = True
        self.score = 0
        self.stage = 1
        self.last_stage_time = time.time()
        self.leaderboard = []
        self.did_update_score = False

        self.start_time = time.time()  # Track game start time
        self.countdown_duration = 2 * 60  # Countdown timer: 2 minutes

    def display_text(self, text, position, color=(0, 0, 0)):
        rendered_text = self.font.render(text, True, color)
        rect = rendered_text.get_rect(center=position)
        self.screen.blit(rendered_text, rect)

    def check_collisions(self):
        def pixel_perfect_collision(rect1: RectType, rect2: RectType, surface1: SurfaceType, surface2: SurfaceType):
            """
            Check for pixel-perfect collision between two rectangles.
            rect1, rect2: pygame.Rect objects for the two rectangles.
            surface1, surface2: pygame.Surface objects for the two images.
            """
            # Create masks for each surface
            mask1 = pygame.mask.from_surface(surface1)
            mask2 = pygame.mask.from_surface(surface2)

            # Calculate the offset between the two rectangles
            offset = (rect2.x - rect1.x, rect2.y - rect1.y)

            # Check if masks overlap
            return mask1.overlap(mask2, offset) is not None

        for top, bottom in self.pipes.pipes:
            if self.bird.rect.colliderect(top) or self.bird.rect.colliderect(bottom):
                # Perform pixel-perfect collision detection
                if pixel_perfect_collision(self.bird.rect, top, self.bird.frame, self.pipes.top_image) or \
                        pixel_perfect_collision(self.bird.rect, bottom, self.bird.frame, self.pipes.bottom_image):
                    # Handle collision
                    pygame.mixer.music.stop()
                    self.crash_sound.play()
                    self.running = False
                    return

    def update_score(self):
        checker = True
        for top, bottom in self.pipes.pipes:
            if top.left <= self.bird.rect.x <= top.right:
                checker = False
                if not self.did_update_score:
                    self.score += 1
                    self.did_update_score = True
            self.screen.blit(self.pipes.bottom_image, bottom)
            self.screen.blit(pygame.transform.flip(self.pipes.bottom_image, False, True), top)
        if checker:
            self.did_update_score = False

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, int(self.countdown_duration - elapsed_time))
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = f"{minutes:02}:{seconds:02}"
        self.display_text(f"Timer: {timer_text}", (self.window_size[0] - 150, 100), (176, 20, 41))

        if remaining_time == 0:
            self.running = False

    def game_over_screen(self):
        logo_rect = self.game_over_logo.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2))
        self.screen.blit(self.game_over_logo, logo_rect)
        self.display_text(f"Score: {self.score}", (self.window_size[0] // 2, self.window_size[1] // 2 + 30),
                          (176, 20, 41))

        self.display_text("Press any key to Continue", (self.window_size[0] // 2, self.window_size[1] // 2 + 75),
                          (176, 20, 41))
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()
                    exit()
                if event.type == pygame.KEYDOWN:
                    return True  # Restart the game

    def game_loop(self):
        self.loading_bar(100, "Starting game...")
        self.running = True
        self.score = 0
        self.stage = 1
        self.pipes.pipes.clear()
        self.pipes.spawn_timer = 0
        pygame.mixer.music.load(FLYING_SOUND)
        pygame.mixer.music.play(-1)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.cleanup()
                # Handle Escape key press
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Escape key pressed. Exiting...")
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
            self.update_timer()
            self.bird.draw(self.screen)
            self.pipes.draw(self.screen)

            self.display_text(f"Score: {self.score}", (100, 50), (176, 20, 41))
            self.display_text(f"Stage: {self.stage}", (100, 100), (176, 20, 41))

            if time.time() - self.last_stage_time > 10:
                self.stage += 1
                self.pipes.spawn_interval *= 5 / 6
                self.last_stage_time = time.time()

            pygame.display.flip()
            self.clock.tick(60)

        # Add score to leaderboard
        self.leaderboard.append(self.score)
        self.game_over_screen()

    def cleanup(self):
        self.face_tracker.release()
        pygame.quit()

    def run(self):
        self.game_loop()
        return self.score


def run_game():
    game = GameEngine()
    try:
        score = game.run()
    finally:
        game.cleanup()
    return score


if __name__ == "__main__":
    run_game()

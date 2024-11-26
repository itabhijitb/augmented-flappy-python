import time
import pygame
import cv2 as cv
from flappy.util import center_window
from flappy.Bird import Bird
from flappy.Pipes import Pipes
from flappy.FaceTracker import FaceTracker
import tkinter as tk
from tkinter import ttk
from flappy.constants import (
    ICON,
    LOGO_IMAGE_PATH,
    FLYING_SOUND,
    CRASH_SOUND,
    GAME_OVER_LOGO_PATH)


class LoadingBar:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Loading Game......")

        self.root.geometry("400x150")
        center_window(self.root, 400, 150)
        # Create a progress bar
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=10)
        # Add a label
        self.message_label = tk.Label(self.root, text="Initializing.....")
        self.message_label.pack(pady=10)
        self.progress_bar["maximum"] = 100

    def __call__(self, value, message):
        self.progress_bar["value"] = value
        self.progress_bar.update()
        self.message_label.config(text=message)
        if value >= 100:
            self.message_label.config(text="Task Completed! Starting in 3 seconds...")
            self.root.after(3000, self.root.destroy)

class GameEngine:
    def __init__(self):
        self.loading_bar = LoadingBar()
        pygame.init()
        self.loading_bar(10, "Loading assets...")
        self.crash_sound = pygame.mixer.Sound(CRASH_SOUND)
        icon = pygame.image.load(ICON)
        pygame.display.set_icon(icon)
        info_object = pygame.display.Info()
        self.window_size = (
            info_object.current_w,
            info_object.current_h
        )
        self.logo = pygame.image.load(LOGO_IMAGE_PATH)
        self.font = pygame.font.SysFont("Helvetica Bold", 40)
        scaled_width = int(self.window_size[0] * 0.25)
        scaled_height = int(self.window_size[1] * 0.25)
        self.game_over_logo = pygame.transform.scale(pygame.image.load(GAME_OVER_LOGO_PATH),
                                                     (scaled_width, scaled_height))
        self.loading_bar(20, "Setting up face tracker...")
        self.face_tracker = FaceTracker()
        self.loading_bar(50, "Determining camera resolution...")
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_WIDTH,info_object.current_w)
        self.face_tracker.video_capture.set(cv.CAP_PROP_FRAME_HEIGHT, info_object.current_h)
        self.loading_bar(60, "Setting screen resolution...")
        self.window_size = (
            self.face_tracker.video_capture.get(cv.CAP_PROP_FRAME_WIDTH),
            self.face_tracker.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT),
        )
        self.loading_bar(70, "Setting mode...")
        self.screen = pygame.display.set_mode(self.window_size, pygame.NOFRAME)
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

        self.start_time = time.time()  # Track game start time
        self.countdown_duration = 2 * 60  # Countdown timer: 2 minutes



    def display_text(self, text, position, color=(0, 0, 0)):
        rendered_text = self.font.render(text, True, color)
        rect = rendered_text.get_rect(center=position)
        self.screen.blit(rendered_text, rect)


    def check_collisions(self):
        for top, bottom in self.pipes.pipes:
            if self.bird.rect.colliderect(top) or self.bird.rect.colliderect(bottom):
                pygame.mixer.music.stop()
                self.crash_sound.play()
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

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = max(0, int(self.countdown_duration - elapsed_time))
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_text = f"{minutes:02}:{seconds:02}"
        self.display_text(f"Timer: {timer_text}", (self.window_size[0] - 150, 50),(176,20,41))

        if remaining_time == 0:
            self.running = False

    def game_over_screen(self):
        logo_rect = self.game_over_logo.get_rect(center=(self.window_size[0] // 2, self.window_size[1] // 2 ))
        self.screen.blit(self.game_over_logo, logo_rect)
        self.display_text(f"Score: {self.score}", (self.window_size[0] // 2, self.window_size[1] // 2 + 50),
                          (176,20,41))

        self.display_text("Press any key to Continue", (self.window_size[0] // 2, self.window_size[1] // 2 + 150),
                          (176,20,41))
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

            self.display_text(f"Score: {self.score}", (100, 50),(176,20,41))
            self.display_text(f"Stage: {self.stage}", (100, 100),(176,20,41))

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

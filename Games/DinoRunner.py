import pygame
import random
import collections
from time import time
import traceback
import os

class DinoRunner:
    # Screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 325

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    def __init__(self, action_options):
        self.action_options = action_options
        self.screen = None
        self.high_score = 0  # Initialize high score
        self.transparent = False  # Track transparency state

        # Load high score from file
        self.high_score_file = "high_score.txt"
        self.load_high_score()

    def load_high_score(self):
        try:
            with open(self.high_score_file, "r") as file:
                self.high_score = int(file.read())
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open(self.high_score_file, "w") as file:
            file.write(str(self.high_score))

    def startRunner(self):
        try:
            # Initialize Pygame
            pygame.init()
            # Create the screen object
            self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            pygame.display.set_caption('Dino Game')

            # Create a game surface for transparency
            self.game_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)

            # Clock to control the frame rate
            clock = pygame.time.Clock()

            # Load Dino image and resize
            dino_img = pygame.image.load('Games/jonJon_binxIcon1.png')
            dino_img = pygame.transform.scale(dino_img, (50, 50))  # Resize to 50x50 pixels

            # Variables for ducking
            is_ducking = False
            dino_duck_img = pygame.transform.scale(dino_img, (50, 30))  # Resized image for ducking

            # Dino attributes
            self.dino_x = 50
            self.dino_y = self.SCREEN_HEIGHT - 100
            self.dino_y_velocity = 0
            GRAVITY = 0.8

            # Obstacle attributes
            self.obstacle_width = 20
            self.obstacle_height = 100  # Set a higher obstacle height
            self.obstacle_x = self.SCREEN_WIDTH
            self.obstacle_y = self.SCREEN_HEIGHT - self.obstacle_height
            self.obstacle_type = random.choice(["jump", "duck"])

            # Obstacle generation timing
            self.obstacle_timer = 0
            self.obstacle_interval = random.randint(90, 150)  # Random interval between 1 and 2.5 seconds

            # Score
            self.score = 0
            self.font = pygame.font.SysFont(None, 35)

            # Game loop
            running = True
            self.game_running = True
            timer_count = 0
            timer_duration = 15

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                timer_count += 1
                if self.game_running:
                    action = None

                    if timer_count > timer_duration:
                        action_counter = collections.Counter(self.action_options)
                        if action_counter:
                            most_common_action = action_counter.most_common(1)[0][0]
                            action = most_common_action
                            if action == "jump":
                                is_ducking = False
                                if self.dino_y == self.SCREEN_HEIGHT - 100:
                                    self.dino_y_velocity = -15
                                self.action_options[:] = []
                            if action == "duck":
                                is_ducking = True
                                self.action_options[:] = []
                            timer_count = 0

                    # Dino gravity and movement
                    self.dino_y_velocity += GRAVITY
                    self.dino_y += self.dino_y_velocity
                    if self.dino_y > self.SCREEN_HEIGHT - 100:
                        self.dino_y = self.SCREEN_HEIGHT - 100

                    # Obstacle movement and generation
                    self.obstacle_x -= 3
                    if self.obstacle_x + self.obstacle_width < 0:
                        self.score += 1  # Increase score only when the obstacle moves off screen
                        self.obstacle_x = self.SCREEN_WIDTH
                        self.obstacle_interval = random.randint(90, 180)  # Random interval between 1.5 and 3 seconds
                        self.obstacle_type = random.choice(["jump", "duck"])
                        self.obstacle_height = random.randint(50, 150)  # Random height for taller obstacles
                        if self.obstacle_type == "duck":
                            self.obstacle_height = 50
                        self.obstacle_y = self.SCREEN_HEIGHT - self.obstacle_height if self.obstacle_type == "jump" else self.SCREEN_HEIGHT - 150  # Adjust position for duck obstacles
                    # print("scored: ", self.score)

                    # Check for collision
                    dino_rect = pygame.Rect(self.dino_x, self.dino_y, 50, 50) if not is_ducking else pygame.Rect(self.dino_x, self.dino_y + 20, 50, 30)
                    obstacle_rect = pygame.Rect(self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height)
                    if dino_rect.colliderect(obstacle_rect):
                        if not (is_ducking and self.obstacle_type == "duck"):
                            self.game_running = False
                    # print("passed collision check")
                    
                    # Drawing everything on the game surface
                    self.game_surface.fill(self.WHITE)
                    if is_ducking:
                        self.game_surface.blit(dino_duck_img, (self.dino_x, self.dino_y + 20))  # Adjust position when ducking
                    else:
                        self.game_surface.blit(dino_img, (self.dino_x, self.dino_y))
                    # print("drew dino")
                    pygame.draw.rect(self.game_surface, self.BLACK, (self.obstacle_x, self.obstacle_y, self.obstacle_width, self.obstacle_height))

                    # Display the score and high score
                    score_text = self.font.render(f'Score: {self.score}', True, self.BLACK)
                    high_score_text = self.font.render(f'High Score: {self.high_score}', True, self.BLACK)
                    self.game_surface.blit(score_text, (10, 10))
                    self.game_surface.blit(high_score_text, (10, 50))
                    # print("displayed score and high score")

                    # Update the screen
                    self.screen.blit(self.game_surface, (0, 0))
                    pygame.display.flip()
                    clock.tick(25)
                    # print("tick")
                else:
                    # print("Game over. Restarting.")
                    running = self.game_over(clock)

        except Exception as e:
            with open("error_log.txt", "a") as f:
                f.write("Error: " + str(e) + "\n")
                f.write(traceback.format_exc() + "\n")

        finally:
            pygame.quit()

    def update_actions(self, actions):
        self.action_options.append(actions)

    def reset_game(self):
        self.dino_x = 50
        self.dino_y = self.SCREEN_HEIGHT - 100
        self.dino_y_velocity = 0
        self.is_ducking = False
        self.obstacle_x = self.SCREEN_WIDTH
        self.obstacle_type = random.choice(["jump", "duck"])
        self.obstacle_height = random.randint(50, 150)
        self.obstacle_y = self.SCREEN_HEIGHT - self.obstacle_height if self.obstacle_type == "jump" else self.SCREEN_HEIGHT - 80  # Adjust position for duck obstacles
        self.score = 0
        self.game_running = True
        self.transparent = False  # Reset transparency state
        # print("Game reset. High score: ", self.high_score)

    def game_over(self, clock):
        # Check and update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
        
        game_over_font = pygame.font.SysFont(None, 75)
        game_over_text = game_over_font.render('Game Over', True, self.BLACK)
        self.game_surface.blit(game_over_text, (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 50))
        self.screen.blit(self.game_surface, (0, 0))
        pygame.display.flip()
        
        waiting = True
        start_time = time()

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.save_high_score()
                    pygame.quit()
                    os._exit(0)
            
            action_counter = collections.Counter(self.action_options)
            if action_counter and ("restart" in action_counter or "start" in action_counter):
                waiting = False
                self.action_options[:] = []
                self.transparent = False
            elif time() - start_time > 20 and not self.transparent:
                print("Game over screen timeout. Saving high score and exiting.")
                self.transparent = True
                self.save_high_score()
                pygame.quit()
                os._exit(0)
            
            # Control the frame rate during the game over screen
            clock.tick(10)

        self.reset_game()
        return True

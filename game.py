import sys
import pygame
from car import Car
from racetrack import RaceTrack

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("2D Car Racing Game")
        self.car = Car()
        self.track = RaceTrack()  # Instantiate the RaceTrack class
        self.double_speed = False  # Flag to indicate if double speed is active

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.car.turning_left = True
                    if event.key == pygame.K_RIGHT:
                        self.car.turning_right = True
                    if event.key == pygame.K_f:
                        self.double_speed = not self.double_speed  # Toggle double speed
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.car.turning_left = False
                    if event.key == pygame.K_RIGHT:
                        self.car.turning_right = False

            if self.double_speed:
                self.car.speed = 6  # Adjust the speed as needed
            else:
                self.car.speed = 3  # Default speed

            if self.car.turning_left:
                self.car.turn_left()
            if self.car.turning_right:
                self.car.turn_right()

            self.car.move()

            # Call the collision detection function with the track segments
            self.car.does_intersect(self.track.track_segments)

            self.screen.fill((200, 200, 200))
            self.track.draw(self.screen)
            self.car.draw(self.screen)
            pygame.display.update()
            clock.tick(60)

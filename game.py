import sys
import pygame
from car import Car
import csv
from racetrack import RaceTrack
from decision_tree import BinaryClassifierModel


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("2D Car Racing Game")
        self.car = Car()
        self.track = RaceTrack()  # Instantiate the RaceTrack class
        self.double_speed = False  # Flag to indicate if double speed is active
        self.agent = BinaryClassifierModel()
        self.agent.start()

    def save_data(self, d1, d2):
        # Save data to a CSV file
        with open('distances.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in d1:
                writer.writerow(row)
        with open('actions.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            for row in d2:
                writer.writerow(row)

    def pad_list_with_average(self, input_list, desired_length):
        if len(input_list) >= desired_length:
            return input_list  # No padding needed

        # Calculate the average of the input list
        average = sum(input_list) / len(input_list)

        # Pad the list with the average value until it reaches the desired length
        while len(input_list) < desired_length:
            input_list.append(average)

        return input_list


    def run(self):
        clock = pygame.time.Clock()

        record_key_pressed = []
        record_distances = []

        while True:
            record_event = [False, False]
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
                    if event.key == pygame.K_r:
                        self.car.raycast_draw = not self.car.raycast_draw  # Toggle drawing of raycasts
                    if event.key == pygame.K_s:
                        self.save_data(record_distances, record_key_pressed)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.car.turning_left = False
                    if event.key == pygame.K_RIGHT:
                        self.car.turning_right = False

            # keys = pygame.key.get_pressed()
            # if keys[pygame.K_LEFT]:
            #     record_event[0] = True
            # if keys[pygame.K_RIGHT]:
            #     record_event[1] = True

            # record_key_pressed.append(record_event)

            # if self.double_speed:
            #     self.car.speed = 6  # Adjust the speed as needed
            # else:
            #     self.car.speed = 3  # Default speed

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

            distances = self.car.raycast(self.track.track_segments, self.screen)

            # record_distances.append(distances)

            prediction = self.agent.predict([self.pad_list_with_average(distances, 30)])
            p = prediction[0]
            left = p[0]
            right = p[1]
            if left:
                self.car.turning_left = True
            else:
                self.car.turning_left = False

            if right:
                self.car.turning_right = True
            else:
                self.car.turning_right = False

            pygame.display.update()
            clock.tick(60)

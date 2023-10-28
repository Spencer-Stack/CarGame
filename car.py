import pygame
import math
from shapely.geometry import Polygon, LineString

class Car:
    def __init__(self):
        self.x = 375
        self.y = 560
        self.speed = 3
        self.angle = 0
        self.turn_speed = 10
        self.turning_left = False
        self.turning_right = False
        self.car_polygon = Polygon([(self.x - 25, self.y - 15),
                                   (self.x + 25, self.y - 15),
                                   (self.x + 25, self.y + 15),
                                   (self.x - 25, self.y + 15)])
        self.is_intersecting = False  # Flag to track intersection

    def move(self):
        radians = math.radians(self.angle)
        dx = self.speed * math.cos(radians)
        dy = self.speed * math.sin(radians)
        self.x += dx
        self.y += dy
        self.update_car_polygon()
        self.is_intersecting = False  # Reset the flag when the car moves

    def turn_left(self):
        self.angle -= self.turn_speed
        self.update_car_polygon()
        self.is_intersecting = False  # Reset the flag when the car turns

    def turn_right(self):
        self.angle += self.turn_speed
        self.update_car_polygon()
        self.is_intersecting = False  # Reset the flag when the car turns

    def update_car_polygon(self):
        self.car_polygon = Polygon([(self.x - 25, self.y - 15),
                                   (self.x + 25, self.y - 15),
                                   (self.x + 25, self.y + 15),
                                   (self.x - 25, self.y + 15)])

    def does_intersect(self, line_segments):
        self.is_intersecting = False  # Reset the flag
        for i in range(len(line_segments)):
            start_point = line_segments[i]
            end_point = line_segments[(i + 1) % len(line_segments)]
            line = LineString([start_point, end_point])
            if self.car_polygon.intersects(line):
                self.is_intersecting = True
                break

    def draw(self, screen):
        car_width = 50
        car_length = 30
        wheel_width = 10  # Adjust this to your desired wheel width
        wheel_length = 7  # Adjust this to your desired wheel length
        wheel_distance = 2  # Distance between the car body and the wheels

        car_surface = pygame.Surface((car_width, car_length), pygame.SRCALPHA)

        # Draw the car body
        if self.is_intersecting:
            pygame.draw.rect(car_surface, (255, 0, 0), pygame.Rect(0, 0, car_width, car_length))
        else:
            pygame.draw.rect(car_surface, (0, 0, 250), pygame.Rect(0, 0, car_width, car_length))

        # Draw wheels at the four corners with the specified wheel distance
        pygame.draw.rect(car_surface, (0, 0, 0), pygame.Rect(wheel_distance, wheel_distance, wheel_width, wheel_length))
        pygame.draw.rect(car_surface, (0, 0, 0),
                         pygame.Rect(car_width - wheel_width - wheel_distance, wheel_distance, wheel_width,
                                     wheel_length))
        pygame.draw.rect(car_surface, (0, 0, 0),
                         pygame.Rect(wheel_distance, car_length - wheel_length - wheel_distance, wheel_width,
                                     wheel_length))
        pygame.draw.rect(car_surface, (0, 0, 0), pygame.Rect(car_width - wheel_width - wheel_distance,
                                                             car_length - wheel_length - wheel_distance, wheel_width,
                                                             wheel_length))

        rotated_car = pygame.transform.rotozoom(car_surface, -self.angle, 1.0)
        rotated_rect = rotated_car.get_rect(center=(self.x, self.y))
        screen.blit(rotated_car, rotated_rect)



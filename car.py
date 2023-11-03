import pygame
import math
from shapely.geometry import Polygon, LineString

class Car:
    def __init__(self):
        self.x = 300
        self.y = 700
        self.speed = 5
        self.angle = 0
        self.turn_speed = 3
        self.turning_left = False
        self.turning_right = False
        self.car_polygon = Polygon([(self.x - 25, self.y - 15),
                                   (self.x + 25, self.y - 15),
                                   (self.x + 25, self.y + 15),
                                   (self.x - 25, self.y + 15)])
        self.is_intersecting = False  # Flag to track intersection
        self.raycast_draw = True

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
        self.angle %= 360
        self.update_car_polygon()
        self.is_intersecting = False  # Reset the flag when the car turns

    def turn_right(self):
        self.angle += self.turn_speed
        self.angle %= 360
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

    # angle in radians
    def generate_line(self, p, angle):
        start_point = p
        end_point = p[0] + 1000 * math.cos(angle), p[1] + 1000 * math.sin(angle)
        return start_point, end_point

    def get_line_intersection(self, p0, p1, p2, p3):
        s1_x, s1_y = p1[0] - p0[0], p1[1] - p0[1]
        s2_x, s2_y = p3[0] - p2[0], p3[1] - p2[1]

        try:
            s = (-s1_y * (p0[0] - p2[0]) + s1_x * (p0[1] - p2[1])) / (-s2_x * s1_y + s1_x * s2_y)
            t = (s2_x * (p0[1] - p2[1]) - s2_y * (p0[0] - p2[0])) / (-s2_x * s1_y + s1_x * s2_y)
        except ZeroDivisionError:
            return None

        if 0 <= s <= 1 and 0 <= t <= 1:
            # Collision detected
            i_x = p0[0] + (t * s1_x)
            i_y = p0[1] + (t * s1_y)
            return i_x, i_y

        return None

    def line_dist(self, p0, p1):
        return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)

    def raycast(self, line_segments, screen):
        distances = []
        for n in range(30):
            b = self.angle + n * 6 - 90
            ang = b if b != 0 else b + 1
            smallest_dist = 10000
            smallest_p = None
            for segment in line_segments:
                end_seg = line_segments[(line_segments.index(segment) + 1) % len(line_segments)]
                ray_cast = self.generate_line((self.x, self.y), math.radians(ang))
                int_point = self.get_line_intersection(ray_cast[0], ray_cast[1], segment, end_seg)
                if int_point is not None:
                    dist = self.line_dist((self.x, self.y), int_point)
                    if dist < smallest_dist:
                        smallest_dist = dist
                        smallest_p = int_point

            border_line_segments = [(0, 0), (1200, 0), (1200, 800), (0, 800)]
            for segment in border_line_segments:
                end_seg = border_line_segments[(border_line_segments.index(segment) + 1) % len(border_line_segments)]
                ray_cast = self.generate_line((self.x, self.y), math.radians(ang))
                int_point = self.get_line_intersection(ray_cast[0], ray_cast[1], segment, end_seg)
                if int_point is not None:
                    dist = self.line_dist((self.x, self.y), int_point)
                    if dist < smallest_dist:
                        smallest_dist = dist
                        smallest_p = int_point

            if smallest_p is not None:
                if self.raycast_draw:
                    pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), smallest_p, 1)
                distances.append(smallest_dist)

        return distances

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



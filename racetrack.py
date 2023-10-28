import pygame

class RaceTrack:
    def __init__(self):
        self.track_segments = [
            (100, 100), (400, 100), (600, 150), (650, 300), (600, 450),
            (400, 500), (200, 450), (100, 300)
        ]
        self.closed = True  # Set to True if the track is closed (last point connects to the first)
        self.color = (0, 0, 0)  # Track color

    def draw(self, screen):
        if len(self.track_segments) < 2:
            return

        for i in range(len(self.track_segments) - 1):
            pygame.draw.line(screen, self.color, self.track_segments[i], self.track_segments[i + 1])

        if self.closed:
            pygame.draw.line(screen, self.color, self.track_segments[-1], self.track_segments[0])

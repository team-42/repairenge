import pyglet

class MusicQueue:
    INTRO = 0
    FLIGHT = 1

    def __init__(self):
        self.state = MusicQueue.INTRO
        self.intro = pyglet.media.load('resources/music/intro-2.wav')
        self.flight = pyglet.media.load('resources/music/flight.wav')

    def __iter__(self):
        return self

    def __next__(self):
        if self.state == MusicQueue.INTRO:
            self.state = MusicQueue.FLIGHT
            return self.intro
        elif self.state == MusicQueue.FLIGHT:
            return self.flight

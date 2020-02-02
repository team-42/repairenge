import pyglet

class MusicQueue:
    INTRO = 0
    FLIGHT = 1
    BOSS_INTRO = 2
    BOSS_INTRO_SHORT = 3
    BOSS_FIGHT = 4
    VICTORY = 5

    def __init__(self):
        self.state = MusicQueue.INTRO
        self.intro = pyglet.media.load('resources/music/intro-2.wav')
        self.flight = pyglet.media.load('resources/music/flight.wav')
        self.boss_intro = pyglet.media.load('resources/music/boss-intro.wav')
        self.boss_intro_short = pyglet.media.load('resources/music/boss-intro-short.wav')
        self.boss_fight = pyglet.media.load('resources/music/boss-fight-2.wav')
        self.victory = pyglet.media.load('resources/music/victory.wav')

    def __iter__(self):
        return self

    def start_boss_fight(self):
        self.state = MusicQueue.BOSS_INTRO

    def start_short_boss_fight(self):
        self.state = MusicQueue.BOSS_FIGHT

    def finished_boss_fight(self):
        self.state = MusicQueue.FLIGHT

    def play_victory(self):
        self.state = MusicQueue.VICTORY

    def play_loss(self):
        self.state = MusicQueue.BOSS_INTRO

    def __next__(self):
        if self.state == MusicQueue.INTRO:
            self.state = MusicQueue.FLIGHT
            return self.intro
        elif self.state == MusicQueue.FLIGHT:
            return self.flight
        elif self.state == MusicQueue.BOSS_INTRO:
            self.state = MusicQueue.BOSS_FIGHT
            return self.boss_intro
        elif self.state == MusicQueue.BOSS_INTRO_SHORT:
            self.state = MusicQueue.BOSS_FIGHT
            return self.boss_intro_short
        elif self.state == MusicQueue.BOSS_FIGHT:
            return self.boss_fight
        elif self.state == MusicQueue.VICTORY:
            return self.victory

    def finish(self):
        self.intro.delete()
        self.flight.delete()
        self.boss_intro.delete()
        self.boss_intro_short.delete()
        self.boss_fight.delete()

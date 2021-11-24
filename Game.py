import pygame
import sys

class Game:

    display = None

    staus = 1
    ###################
    ## Game Statuses ##
    MAIN_MENU = 1
    DRAW_MODE = 2
    PLAY_MODE = 3

    status = MAIN_MENU
    draw_status = False
    ###################

    listeners = dict()
    fonts = dict()
    songs = dict()
    
    handlers = []

    fps = 30

    def __init__(self, displaySize, fps=30):
        pygame.init()
        self.setFps(fps)
        self.clock = pygame.time.Clock()
        self.set_mode(*displaySize)

    def setFps(self, fps):
        self.fps = fps

    def set_mode(self , width, height):
        self.display = pygame.display.set_mode((width, height))

    def blit(self, surface, rect):
        self.display.blit(surface , rect)

    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)

    def add(self, handler , args=None):
        self.handlers.append({"handle" : handler, "args" : args})

    def handle(self):
        for handler in self.handlers:
            handler['handle']( *(handler.get('args') or []) )

    def play(self):
        while True:
            self.display.fill('black')
            self.handle()
            self.eventsLoop()
            self.update()

    def eventsLoop(self):
        for event in pygame.event.get():
            listeners = self.listeners.get(event.type) or []
            for listener in listeners:
                listener.handle(event)
    
    def addEventListener(self, type, listener):
        if not self.listeners.get(type):
            self.listeners[type] = []
        self.listeners[type].append(listener)

    def quit(self):
        pygame.quit()
        sys.exit(0)

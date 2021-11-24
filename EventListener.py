import pygame

class EventListener:

    handler = False
    args = []

    def __init__(self, handler,args=None):
        self.handler = handler
        self.args = args
    
    def handle(self,event):
        return self.handler(event, *(self.args or []))

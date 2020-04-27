import pygame
from pygame.locals import *

local_font_file = 'mychess/play_games/PingFang.ttc'

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (140, 220, 254)
button_color = (0, 160, 255)


class myButton:
    def __init__(self, rect: Rect, text='', font_color=black, bkgColor=white, font_size=16):
        self.__Rect = rect
        self.__text = text
        self.__bkgColor = bkgColor
        self.__w, self.__h = rect.width, rect.height
        self.__Surface = pygame.Surface([self.__w, self.__h])
        self.__Surface.fill(bkgColor)
        self.__font = pygame.font.Font(local_font_file, font_size)
        t = self.__font.render(text, True, font_color)
        t_rect = t.get_rect()
        t_rect.centerx = self.__w // 2
        t_rect.centery = self.__h // 2
        # print(t_rect)
        self.__Surface.blit(t, t_rect)

    def get_Surface(self):
        return self.__Surface

    def get_rect(self):
        return self.__Rect

    def set_rect(self, x, y):
        self.__Rect.centerx = x
        self.__Rect.centery = y

    def get_text(self):
        return self.__text

    def set_text(self, text='', font_color=black):
        self.__text = text
        t = self.__font.render(text, True, font_color)
        t_rect = t.get_rect()
        t_rect.centerx = self.__w // 2
        t_rect.centery = self.__h // 2
        self.__Surface.fill(self.__bkgColor)
        self.__Surface.blit(t, t_rect)

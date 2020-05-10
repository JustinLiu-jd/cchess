import pygame
from pygame.locals import *

local_font_file = 'mychess/play_games/PingFang.ttc'

white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
red = (200, 0, 0)
green = (0, 200, 0)
bright_red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (140, 220, 254)
button_color = (0, 160, 255)
label_color = (180, 220, 250)
record_color = (250, 247, 212)
wordLabelColor = (150, 200, 230)


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

    # 判断是否在区域内
    def isInRect(self, x, y, x_offset=0, y_offset=0):
        x -= x_offset
        y -= y_offset
        myRect = self.get_rect()
        # print(myRect.left, myRect.right, myRect.top, myRect.bottom)
        if myRect.left <= x <= myRect.right and myRect.top <= y <= myRect.bottom:
            return True
        else:
            return False


class myLabel:
    def __init__(self, rect: Rect, text=None, font_color=black, bkgColor=None, font_size=16, textList: list = None,
                 xList: list = None):
        self.__Rect = rect
        self.__text = text
        self.__bkgColor = None
        self.__w, self.__h = rect.width, rect.height
        self.__Surface = pygame.Surface([self.__w, self.__h])
        if bkgColor != None:
            self.__Surface.fill(bkgColor)
            self.__bkgColor = bkgColor
        self.__font = pygame.font.Font(local_font_file, font_size)
        if text != None:
            t = self.__font.render(text, True, font_color)
            t_rect = t.get_rect()
            t_rect.centerx = self.__w // 2
            t_rect.centery = self.__h // 2
            # print(t_rect)
            self.__Surface.blit(t, t_rect)
        elif textList != None and len(textList) == len(xList):
            for i in range(len(textList)):
                text = textList[i]
                pos = xList[i]
                t = self.__font.render(text, True, font_color)
                t_rect = t.get_rect()
                t_rect.centerx = pos
                t_rect.centery = self.__h // 2
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
        if self.__bkgColor:
            self.__Surface.fill(self.__bkgColor)
        self.__Surface.blit(t, t_rect)

    def isInRect(self, x, y):
        myRect = self.get_rect()
        # print(myRect.left, myRect.right, myRect.top, myRect.bottom)
        if myRect.left <= x <= myRect.right and myRect.top <= y <= myRect.bottom:
            return True
        else:
            return False

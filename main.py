from PIL import Image
from time import sleep
from random import randint
import os
import ctypes


class Wallpaper:
    def __init__(self, image: str, screen: tuple = (1920,1080), speed: int = 6, spin: bool = False) -> None:
        self.__image = Image.open(image)
        self.__screen = screen
        self.__speed = speed
        self.__spin = spin


        self.__degree = 0
        self.__x = randint(0,screen[0]-self.__image.size[0])
        self.__y = randint(0,screen[1]-self.__image.size[1])
        self.__vector_x = "RIGHT"
        self.__vector_y = "DOWN"

    def get_image(self) -> int:
        return self.__image

    def set_image(self, value: int) -> None:
        self.__image = value
    
    def get_coordinates(self) -> tuple:
        return self.__x, self.__y

    def set_x(self, value: int) -> None:
        self.__x = value

    def set_y(self, value: int) -> None:
        self.__d = value

    def get_speed(self) -> int:
        return self.__speed

    def set_speed(self, value: int) -> None:
        self.__speed = value

    def get_screen(self) -> tuple:
        return self.__screen

    def set_screen(self, value: tuple) -> None:
        self.__screen = value

    def get_degree(self) -> int:
        return self.__degree

    def set_degree(self, value: int) -> None:
        self.__degree = value

    def get_spin(self) -> bool:
        return self.__spin

    def set_spin(self, value: bool) -> None:
        self.__spin = value

    def move(self, background: str = None) -> tuple:
        try:
            #Rotation
            if self.__spin:
                image = self.__image.rotate(self.__degree, expand = True)
                self.__degree = (self.__degree+3)%360
            else:
                image = self.__image
            
            #X axis
            if self.__vector_x == "RIGHT":
                if self.__x+self.__speed+image.size[0]<=self.__screen[0]:
                    self.__x += self.__speed
                else:
                    self.__vector_x = "LEFT"
            else:
                if self.__x-self.__speed>=0:
                    self.__x -= self.__speed
                else:
                    self.__vector_x = "RIGHT"

            #Y axis
            if self.__vector_y == "DOWN":
                if self.__y+self.__speed+image.size[1]<=self.__screen[1]:
                    self.__y += self.__speed
                else:
                    self.__vector_y = "UP"
            else:
                if self.__y-self.__speed>=0:
                    self.__y -= self.__speed
                else:
                    self.__vector_y = "DOWN"

            #Setting Background
            if background == None:
                background = Image.new("RGB",self.__screen)
            else:
                background = Image.open(background)
                background = background.resize(self.__screen)
            
            background.paste(image, (self.__x,self.__y))
            background.save("wallpaper.png")
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("wallpaper.png"), 0)
            sleep(1/30)
        except:
            print(Exception)

if __name__ == "__main__":
    wallpaper = Wallpaper(image = str(input("Filename: ")), spin = True)
    while True:
        wallpaper.move()

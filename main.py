from PIL import Image
from time import sleep
from random import randint
import os
import ctypes

class SpaceImage:
    def __init__(self, image: Image, screen: tuple ,speed: int = 6, spin: bool = False):
        self.image = image

        self.speed = speed
        self.spin = spin

        self.degree = 0

        self.x = randint(0,screen[0]-self.image.size[0])
        self.y = randint(0,screen[1]-self.image.size[1])

        self.vector_x = "RIGHT"
        self.vector_y = "DOWN"


class SpacePaper:
    def __init__(self, screen: tuple = (1920,1080)):
        self.screen = screen
        self.images = []

    def add_image(self, filename: str, spin: bool = False) -> Image:
        image = SpaceImage(Image.open(filename), self.screen, spin = spin)
        self.images.append(image)
        return image

    def play(self) -> None:
        background = Image.new("RGB",self.screen)
        try: 
            for space_image in self.images:
                #Rotation
                if space_image.spin:
                    image = space_image.image.rotate(space_image.degree, expand = True)
                    space_image.degree = (space_image.degree+3)%360
                else:
                    image = space_image.image
            
                #X axis
                if space_image.vector_x == "RIGHT":
                    if space_image.x+space_image.speed+image.size[0]<=self.screen[0]:
                        space_image.x += space_image.speed
                    else:
                        space_image.vector_x = "LEFT"
                else:
                    if space_image.x-space_image.speed>=0:
                        space_image.x -= space_image.speed
                    else:
                        space_image.vector_x = "RIGHT"

                #Y axis
                if space_image.vector_y == "DOWN":
                    if space_image.y+space_image.speed+image.size[1]<=self.screen[1]:
                        space_image.y += space_image.speed
                    else:
                        space_image.vector_y = "UP"
                else:
                    if space_image.y-space_image.speed>=0:
                        space_image.y -= space_image.speed
                    else:
                        space_image.vector_y = "DOWN"
            
                background.paste(image, (space_image.x,space_image.y))
            background.save("wallpaper.png")
            ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath("wallpaper.png"), 0)
            sleep(1/30)
        except:
            pass

if __name__ == "__main__":
    sp = SpacePaper()
    sp.add_image("test.png", True)
    sp.add_image("test.png")
    while True:
        sp.play()
        

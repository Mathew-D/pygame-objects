#Made by: Mathew Dusome
#Adds still images and animated images
#To use images with transparency you need to use sprites.  To do this we have two main types, still and animated.
#For animated you have install pillow to make it work so:
#    pip install pillow 
# Next add the import with:
#    import objects.image as image
#Next you have to import the file then can either use it directly or extend you class with it.  To use it directly you use go:
#    object = image.still(10,20,200,100,"images/image_show.png")
#Where:
#    object --> is the name for the image
#    10 --> starting x
#    20 --> starting y
#    200 --> width
#    100 --> height
#    "images/image_show.png" --> image to show
#You can now either add it to a group and draw the group or draw the object directly.
# You must draw the image somewhere in display or your loop with:
#    object.draw(window) 

import pygame
#custom object for still images
class still(pygame.sprite.Sprite):
    def __init__(self, x, y,width,height,image_to_use):
        super().__init__()
        self.image = pygame.image.load(image_to_use)
        self.image = pygame.transform.scale(self.image, (width, height)).convert_alpha()
        self.mask  = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft=(x,y))
   
    def draw(self,window):
        window.blit(self.image,(self.rect.x, self.rect.y))



#must install
#pip install PIL
"""
from PIL import Image, ImageSequence

class animated(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, filename,update_speed):
        pygame.sprite.Sprite.__init__(self)
        self.images = self.loadGIF(filename)
        self.image =  pygame.transform.scale(self.images[0], (width, height)).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.image_index = 0
        self.timer=0
        self.update_speed = update_speed
    def draw(self,window):
        window.blit(self.image,(self.rect.x, self.rect.y))
    def update(self):
        self.timer+=10
        if self.timer >=self.update_speed:
            self.image_index += 1
           # self.image = self.images[self.image_index % len(self.images)]
            self.image =  pygame.transform.scale(self.images[self.image_index % len(self.images)], (self.rect.width, self.rect.height)).convert_alpha()
            self.timer=0
    def loadGIF(self,filename):
        pilImage = Image.open(filename)
        frames = []
        for frame in ImageSequence.Iterator(pilImage):
            frame = frame.convert('RGBA')
            pygameImage = pygame.image.fromstring(
                frame.tobytes(), frame.size, frame.mode).convert_alpha()
            frames.append(pygameImage)
        return frames

"""

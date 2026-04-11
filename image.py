#Made by: Mathew Dusome
#Adds still images and animated images with transparency support using sprites
#
#SETUP:
#For animated GIFs, install pillow:
#    pip install pillow
#
#IMPORT:
#    import objects.image as image
#
#USAGE PATTERN:
#    1. Create image object (outside main loop)
#    2. In DISPLAY LOOP: call image_obj.draw(window)
#    3. For animated images in GAME LOOP: call image_obj.update()
#
#PARAMETERS FOR still CLASS:
#    x, y          --> Starting position (top-left corner)
#    width, height --> Size to scale the image to in pixels
#    image_to_use  --> Path to the image file (e.g., "images/background.png")
#
#EXAMPLE 1: Still Image
#    background = image.still(0, 0, 800, 600, "images/background.png")
#    # In DISPLAY LOOP:
#    #   background.draw(window)
#
#PARAMETERS FOR animated CLASS:
#    x, y          --> Starting position (top-left corner)
#    width, height --> Size to scale each frame to in pixels
#    filename      --> Path to the GIF file (e.g., "images/player.gif")
#    update_speed  --> Milliseconds between frame changes (e.g., 100 = 10 FPS)
#
#EXAMPLE 2: Animated Image (GIF)
#    player_idle = image.animated(100, 200, 64, 64, "images/player_idle.gif", 100)
#    # In DISPLAY LOOP:
#    #   player_idle.draw(window)
#    # In GAME LOOP:
#    #   player_idle.update()
#
#NOTE: Always call draw() in your display loop; call update() in your game loop (animated only) 

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

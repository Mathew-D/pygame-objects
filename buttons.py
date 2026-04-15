#Made by: Mathew Dusome
#Adds 3 different button types: no_background, with_background, and with_images
#
#IMPORT:
# import objects.buttons
#
#USAGE PATTERN:
#    1. Create button object (outside main loop)
#    2. In EVENT LOOP: call button.update(pygame.mouse.get_pos(), event)
#    3. In DISPLAY LOOP: call button.draw(window)
#
#PARAMETERS FOR no_background CLASS:
#    start_x, start_y     --> Starting position (top-left corner)
#    font_name            --> System font name (e.g., 'Arial', 'Consolas') - optional
#    font_size            --> Font size in pixels (default: 16)
#    text_color           --> Text color as RGB tuple (default: black)
#    hover_color          --> Text color when hovered as RGB tuple (default: black)
#    text                 --> Text to display on button (default: empty string)
#    action               --> Optional callback function
#    download_font_name   --> Path to downloaded font file - use instead of font_name
#
#EXAMPLE 1: Button with just text (no_background) - system font
#    btn_exit = objects.buttons.no_background(0, 0, font_name="Arial", font_size=12, text_color=(235, 64, 52), hover_color=(98, 52, 235), text="Click to Exit")
#
#EXAMPLE 1b: Button with just text - downloaded font only
#    btn_exit = objects.buttons.no_background(0, 0, font_size=12, text_color=(235, 64, 52), hover_color=(98, 52, 235), text="Click to Exit", download_font_name="fonts/MyFont.ttf")
#
#PARAMETERS FOR with_background CLASS:
#    start_x, start_y     --> Starting position (top-left corner)
#    width, height        --> Button dimensions in pixels
#    font_name            --> System font name (optional)
#    font_size            --> Font size in pixels (default: 16)
#    back_color           --> Background color as RGB tuple (default: light gray)
#    text_color           --> Text color as RGB tuple (default: black)
#    hover_color          --> Text color when hovered as RGB tuple (default: black)
#    back_hover_color     --> Background color when hovered as RGB tuple (default: dark gray)
#    text                 --> Text to display on button (default: empty string)
#    action               --> Optional callback function
#    download_font_name   --> Path to downloaded font file - use instead of font_name
#
#EXAMPLE 2: Button with text and background (with_background) - system font
#    btn_start = objects.buttons.with_background(100, 50, 200, 50, font_name="Arial", font_size=16, back_color=(50,50,50), text_color=(255,255,255), hover_color=(255,200,0), back_hover_color=(70,70,70), text="Start Game")
#
#EXAMPLE 2b: Button with text and background - downloaded font only
#    btn_start = objects.buttons.with_background(100, 50, 200, 50, font_size=16, back_color=(50,50,50), text_color=(255,255,255), hover_color=(255,200,0), back_hover_color=(70,70,70), text="Start Game", download_font_name="fonts/MyFont.ttf")
#
#PARAMETERS FOR with_images CLASS:
#    start_x, start_y  --> Starting position (top-left corner)
#    width, height     --> Button dimensions in pixels
#    image_no          --> Path to default image file
#    image_hover       --> Path to hover image file
#
#EXAMPLE 3: Button with image (with_images)
#    btn_image = objects.buttons.with_images(150, 100, 80, 80, "button_default.png", "button_hover.png")
#
#USAGE IN EVENT AND DISPLAY LOOPS:
#    # In EVENT LOOP:
#    if btn_exit.update(pygame.mouse.get_pos(), event):
#        sys.exit()
#    # In DISPLAY LOOP:
#    btn_exit.draw(window)



import pygame

class no_background(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,font_name=None,font_size=16,text_color=(0,0,0),hover_color=(0,0,0),text="",action=None,download_font_name=None):
        super().__init__()
        if download_font_name:
            font_used = pygame.font.Font(download_font_name, font_size)
        elif font_name:
            font_used = pygame.font.SysFont(font_name, font_size)
        else:
            font_used = pygame.font.SysFont('arial', font_size)
        self.text_surface = font_used.render(text, True, text_color)
        self.default=self.text_surface
        self.hover_text= font_used.render(text, True, hover_color)
        self.image=self.text_surface
        self.hover = self.hover_text
        self.rect = self.image.get_rect(topleft =(start_x,start_y))
   
        self.action = action
    def update(self,pos,event):              
        if self.rect.collidepoint(pos):          
            self.image =self.hover
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.action:
                    self.action()
                else:
                    return True
            else:
                return False
        else:
            self.image =self.default
    
    def draw(self, screen):
        # Render the text surface
       screen.blit(self.image,self.rect)
class with_background(no_background):
    def __init__(self,start_x,start_y,width,height,font_name=None,font_size=16,back_color=(200,200,200),text_color=(0,0,0),hover_color=(0,0,0),back_hover_color=(150,150,150),text="",action=None,download_font_name=None):
        super().__init__(start_x,start_y,font_name,font_size,text_color,hover_color,text,action,download_font_name)
        self.text_width=self.text_surface.get_width()
        self.text_height= self.text_surface.get_height()

        self.default = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()
        self.default.fill(back_color)  
        self.default.blit(self.text_surface, (((width-self.text_width)/2), ((height-self.text_height)/2)))
       
        self.hover = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()
        self.hover.fill(back_hover_color)
        self.hover.blit(self.hover_text, (((width-self.text_width)/2), ((height-self.text_height)/2)))
       
        self.image=self.default
        self.rect = self.image.get_rect(topleft =(start_x,start_y))
               
   
       
class with_images(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,width, height, image_no, image_hover,action=None,*a_args):
        super().__init__()        
        self.img_default = pygame.image.load(image_no)
        self.img_hover = pygame.image.load(image_hover)
       
        self.img_default = pygame.transform.scale(self.img_default , (width, height)).convert_alpha()
        self.img_hover = pygame.transform.scale(self.img_hover , (width, height)).convert_alpha()
       
        self.image = self.img_default
        self.mask  = pygame.mask.from_surface(self.image)
   
        self.rect = self.image.get_rect(topleft =(start_x,start_y))
       
        self.action = action
        self.action_args = a_args

    def update(self,pos,event):              
        if self.check_mouse_collision(pos):
            self.image = self.img_hover
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
               if self.action_args:
                   self.action(*self.action_args)
               elif self.action ==None:
                   return True
               else: self.action()
            else:
                return False
        else:
            self.image =self.img_default

    def check_mouse_collision(sprite, mouse_pos):
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.image = pygame.Surface([1, 1])
        mouse_sprite.rect = mouse_sprite.image.get_rect(topleft =mouse_pos)
        return pygame.sprite.collide_mask(sprite, mouse_sprite)
    def draw(self, screen):
        # Render the text surface
       screen.blit(self.image,self.rect)

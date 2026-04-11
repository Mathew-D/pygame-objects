# Made By: Riley Czarkowski (November 4, 2024)
# Provides checkbox and radio button widgets for pygame
#
# IMPORT:
#    import objects.checkbox as checkbox
#
# USAGE PATTERN:
#    1. Create checkbox/radio button object (outside main loop)
#    2. In EVENT LOOP: call button.update(pygame.mouse.get_pos(), event)
#    3. In DISPLAY LOOP: call button.draw(window)
#
# PARAMETERS FOR check_box CLASS:
#    x, y                        --> Starting position (top-left corner)
#    size                        --> Button size in pixels (default: 30)
#    circular_button             --> Make button circular (default: False)
#    background_colour           --> Background color as RGB tuple (default: white)
#    background_hover_colour     --> Background color when hovered (default: light gray)
#    background_disabled_colour  --> Background color when disabled (default: dark gray)
#    checkmark_colour            --> Checkmark color as RGB tuple (default: black)
#    checkmark_width             --> Checkmark line width in pixels (default: 4)
#    active                      --> Initial checked state (default: False)
#    disabled                    --> Disable checkbox (default: False)
#    action                      --> Optional function to call when clicked
#    *a_args                     --> Arguments for action function
#
# EXAMPLE 1: Basic checkbox
#    check_box = checkbox.check_box(50, 50)
#    # In EVENT LOOP:
#    #   if check_box.update(pygame.mouse.get_pos(), event):
#    #       if check_box.checkmark_active:
#    #           print("Checkbox is checked")
#    # In DISPLAY LOOP:
#    #   check_box.draw(window)
#
# EXAMPLE 2: Checkbox with custom colors
#    check_box = checkbox.check_box(50, 50, size=40, background_colour=(230,230,230),
#                                  checkmark_colour=(255,0,0), checkmark_width=5)
#
# PARAMETERS FOR radio_button CLASS:
#    x, y        --> Starting position (top-left corner)
#    button_group --> ButtonGroup() object containing all radio buttons
#    Other parameters same as check_box
#
# EXAMPLE 3: Radio button group
#    radio_group = checkbox.ButtonGroup()
#    radio_1 = checkbox.radio_button(50, 100, radio_group)
#    radio_2 = checkbox.radio_button(110, 100, radio_group)
#    # In EVENT LOOP:
#    #   radio_group.update(pygame.mouse.get_pos(), event)
#    # In DISPLAY LOOP:
#    #   radio_group.draw(window)
#
# EXAMPLE 4: Button with action function
#    def on_click(name):
#        print(f"{name} was clicked")
#    check_box = checkbox.check_box(50, 50, action=on_click, "My Button")

import pygame

class ButtonGroup(pygame.sprite.Group):
    def draw(self, surface):
        for sprite in self.sprites():
            sprite.draw(surface)

class check_box(pygame.sprite.Sprite):
    def __init__(self, x, y, size=30, circular_button=False, background_colour=(255,255,255), background_hover_colour=(200,200,200), background_disabled_colour=(100,100,100),checkmark_colour=(0,0,0), checkmark_width=4, active=False, disabled=False, action=None, *a_args):
        super().__init__()
        self.size = size
        self.x = x
        self.y = y
        self.circular_button = circular_button
        self.checkmark_colour = checkmark_colour
        self.checkmark_width = checkmark_width
        self.checkmark_active =  active
        self.disabled = disabled
        self.clicked = False
        self.mouse_down = False

        self.default = pygame.Surface([size, size],pygame.SRCALPHA).convert_alpha()
        self.default.fill(background_colour)  
       
        self.hover = pygame.Surface([size, size],pygame.SRCALPHA).convert_alpha()
        self.hover.fill(background_hover_colour)
        
        self.off = pygame.Surface([size, size],pygame.SRCALPHA).convert_alpha()
        self.off.fill(background_disabled_colour)
       
        self.image = self.default
        self.rect = self.image.get_rect(topleft =(x, y))

        self.action = action
        self.action_args = a_args
        
    # This version of the update() function only updates the checkbox when the mouse is RELEASED (click and release), NOT the instant the checkbox is CLICKED
    def update(self, pos, event):
        if self.disabled:
                # If the checkbox is set disabled, set the background to the disabled background and return (don't run any of the code below)
                self.image = self.off
                return
            
        # If the user is hovering over the button OR their mouse is down (if they clicked and dragged off the button holding the mouse, we still want to run this code)
        if self.rect.collidepoint(pos) or self.mouse_down:    
            # When the user is hovering over the checkbox, set the background to the hover background
            self.image = self.hover
            
            # Returns true if left mouse click is down
            self.mouse_down = pygame.mouse.get_pressed()[0]

            # When the user left clicks on the checkbox
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True 
            # If the button was clicked and they have now released the left mouse, run this code (clicked and then RELEASED)
            if self.clicked and not self.mouse_down:
                # If no longer hovering over the button, set image back to default (if the user moved mouse off of button but kept hover active by keeping mouse down)
                if not self.rect.collidepoint(pos): 
                    self.image = self.default
                self.clicked = False
                self.mouse_down = False
                self.checkmark_active = not self.checkmark_active
                # Only run the action (if given) when the checkbox is clicked and made active
                if self.action_args and self.checkmark_active:
                    self.action(*self.action_args)
                elif self.action != None and self.checkmark_active: 
                    self.action()
                return True
            else:
                # The user did not click the checkbox so return false
                return False
        else:
            # When the user is not hovering over the checkbox, set the background to the default background
            self.image = self.default
            
    # OLD update code which will update the checkbox the INSTANT the user clicks on it        
    """    
    def update(self, pos, event):           
        if self.disabled:
            # If the checkbox is set disabled, set the background to the disabled background and return (don't run any of the code below)
            self.image = self.off
            return
        
        if self.rect.collidepoint(pos):          
            # When the user is hovering over the checkbox, set the background to the hover background
            self.image = self.hover
            
            # When the user left clicks on the checkbox
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True
                self.checkmark_active = not self.checkmark_active
                # Only run the action (if given) when the checkbox is clicked and made active
                if self.action_args and self.checkmark_active:
                    self.action(*self.action_args)
                elif self.checkmark_active and self.action != None: 
                    self.action()
                return True
            else:
                # The user did not click the checkbox so return false
                return False
        else:
            # When the user is not hovering over the checkbox, set the background to the default background
            self.image = self.default
        """
    
    def draw(self, screen):
        if self.circular_button:
            # Renders the check button (circular button)
            
            # Draws the background
            screen.blit(self.image, self.rect)
            
            # Draws a circle border around the button
            pygame.draw.circle(screen,self.checkmark_colour,(self.x+(self.size/2),self.y+(self.size/2)), self.size/2+self.checkmark_width-2, self.checkmark_width)
    
            if self.checkmark_active:
                # If the checkmark is active, draw it (a circle in this case to fit the desgin of the checkbox)
                pygame.draw.circle(screen,self.checkmark_colour,(self.x+(self.size/2),self.y+(self.size/2)), (self.size/2+self.checkmark_width)-10)
        else:    
            # Renders the check box (square button)
            
            # Draws the background
            screen.blit(self.image, self.rect)
            
            
            # Draw a rectangle around the checkmark box
            pygame.draw.line(screen,self.checkmark_colour,(self.x,self.y),(self.x+self.size,self.y), 2)
            pygame.draw.line(screen,self.checkmark_colour,(self.x,self.y),(self.x,self.y+self.size), 2)
            pygame.draw.line(screen,self.checkmark_colour,(self.x+self.size,self.y),(self.x+self.size,self.y+self.size), 2)
            pygame.draw.line(screen,self.checkmark_colour,(self.x,self.y+self.size),(self.x+self.size,self.y+self.size), 2)
                    
            if self.checkmark_active:
                # If the checkmark is active, draw it
                offset = 4
                pygame.draw.line(screen,self.checkmark_colour,(self.x+offset,self.y+(self.size/2)),(self.x+(self.size/2),self.y+self.size-offset), self.checkmark_width)
                pygame.draw.line(screen,self.checkmark_colour,(self.x+(self.size/2),self.y+self.size-offset),(self.x+self.size-offset,self.y+offset), self.checkmark_width)
            
class radio_button(check_box):
    def __init__(self, x, y, sprite_group: pygame.sprite.Group, circular_button=False, size=30, background_colour=(255,255,255), background_hover_colour=(200,200,200), background_disabled_colour=(100,100,100),checkmark_colour=(0,0,0), checkmark_width=4, active=False, disabled=False, action=None, *a_args):
        super().__init__(x, y, size, circular_button, background_colour, background_hover_colour, background_disabled_colour,checkmark_colour, checkmark_width, active, disabled, action, *a_args)
        sprite_group.add(self)
        self.sprite_group = sprite_group
        
    def update(self, pos, event):
        if super().update(pos, event):
            for btn in self.sprite_group:
                    btn.checkmark_active = False
            self.checkmark_active = True     
            return True   
        
class list_display(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 110
        self.y = 200
        self.width = 20
        self.list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,"hi","hello","noah","riley"]
        self.max_to_display = 5
        self.font = "Consolas"
        self.font_size = 20
        self.length = self.max_to_display*self.font_size
        self.text_colour = (0,0,0)
        self.clicked = False
        self.txt_iamges = []
        self.txt_rects = []
        self.new_list = []
        self.txt_img_to_blit = None
        self.txt_rect_to_blit = None
        
        self.scroll = pygame.Surface([10, self.length-(self.length/len(self.list))],pygame.SRCALPHA).convert_alpha()
        self.scroll.fill((100,100,100))
        
        self.scroll_hover = pygame.Surface([10, self.length-(self.length/len(self.list))],pygame.SRCALPHA).convert_alpha()
        self.scroll_hover.fill((150,150,150))
       
        self.image = self.scroll
        self.rect = self.image.get_rect(topleft =(self.x+self.length-10, self.y))
        
    def update(self, pos, event):
        if self.rect.collidepoint(pos) or self.clicked:
            mouse_down = pygame.mouse.get_pressed()[0]
            if not mouse_down: self.clicked = False
            self.image = self.scroll_hover
            
            if self.clicked:
                old_y = self.rect.y
                self.rect.y = old_y+pos[1]-self.start_y
                if self.rect.y < self.y:
                    self.rect.y = self.y
                elif self.rect.y > self.length-self.rect.height+self.y:
                    self.rect.y = self.length-self.rect.height+self.y
            # When the user left clicks
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.start_y = pos[1]
                self.clicked = True
        else:
            self.image = self.scroll
            
        self.txt_img_to_blit = None
        self.txt_rect_to_blit = None
        for rect in self.txt_rects:
            if rect.collidepoint(pos):
                index = self.txt_rects.index(rect)-1
                self.txt_img_to_blit = self.txt_images[index]
                self.txt_rect_to_blit = rect
                
                # When the user left clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    print(f"{self.new_list[index+1]}")
                break
        
    def draw(self, screen):
        if self.txt_rect_to_blit is not None:
            screen.blit(self.txt_img_to_blit, self.txt_rect_to_blit)
            
        screen.blit(self.image,self.rect)
        
        # Draw a rectangle around the box
        pygame.draw.line(screen,self.text_colour,(self.x,self.y),(self.x+self.length,self.y), 2)
        pygame.draw.line(screen,self.text_colour,(self.x,self.y),(self.x,self.y+self.length), 2)
        pygame.draw.line(screen,self.text_colour,(self.x+self.length,self.y),(self.x+self.length,self.y+self.length), 2)
        pygame.draw.line(screen,self.text_colour,(self.x,self.y+self.length),(self.x+self.length,self.y+self.length), 2)
        
        y = self.y
        font = pygame.font.SysFont(self.font, self.font_size)
        
        try:
            white_space = (self.length-self.rect.height)/(len(self.list)-self.max_to_display)
            offset = self.rect.y - self.y
            add = offset//white_space
        except:
            add = 0
        self.new_list = self.list[int(0+add):int(self.max_to_display+add)]
        self.txt_images = []
        self.txt_rects = []
        for option in self.new_list:
            screen.blit(font.render(f"{option}", True, self.text_colour), (self.x+2, y))
            txt_hitbox = pygame.Surface([self.length-10, self.font_size],pygame.SRCALPHA).convert_alpha()
            txt_hitbox.fill((200,200,200))
            txt_rect = txt_hitbox.get_rect(topleft =(self.x, y))
            self.txt_images.append(txt_hitbox)
            self.txt_rects.append(txt_rect)
            y += self.font_size
        
class combo_box(pygame.sprite.Sprite):
    def __init__(self, x, y, options, max_options_display=5, length=100, width=20, font="Consolas", text_colour=(0,0,0), background_colour=(255,255,255), background_hover_colour=(200,200,200), background_disabled_colour=(100,100,100), disabled=False, action=None, *a_args):
        super().__init__()
        self.length = length
        self.width = width
        self.x = x
        self.y = y
        self.options = options
        self.font = font
        self.max_options_display = max_options_display
        self.text_colour = text_colour
        self.disabled = disabled
        self.clicked = False
        self.mouse_down = False
        self.show_options = False

        self.default = pygame.Surface([self.length, self.width],pygame.SRCALPHA).convert_alpha()
        self.default.fill(background_colour)  
       
        self.hover = pygame.Surface([self.length, self.width],pygame.SRCALPHA).convert_alpha()
        self.hover.fill(background_hover_colour)
        
        self.off = pygame.Surface([self.length, self.width],pygame.SRCALPHA).convert_alpha()
        self.off.fill(background_disabled_colour)
       
        self.image = self.default
        self.rect = self.image.get_rect(topleft =(x, y))

        self.action = action
        self.action_args = a_args

    def update(self, pos, event):
        if self.disabled:
                # If the checkbox is set disabled, set the background to the disabled background and return (don't run any of the code below)
                self.image = self.off
                return
            
        # If the user is hovering over the button OR their mouse is down (if they clicked and dragged off the button holding the mouse, we still want to run this code)
        if self.rect.collidepoint(pos) or self.mouse_down:    
            # When the user is hovering over the checkbox, set the background to the hover background
            self.image = self.hover
            
            # Returns true if left mouse click is down
            self.mouse_down = pygame.mouse.get_pressed()[0]

            # When the user left clicks on the checkbox
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.clicked = True 
            # If the button was clicked and they have now released the left mouse, run this code (clicked and then RELEASED)
            if self.clicked and not self.mouse_down:
                # If no longer hovering over the button, set image back to default (if the user moved mouse off of button but kept hover active by keeping mouse down)
                if not self.rect.collidepoint(pos): 
                    self.image = self.default
                self.clicked = False
                self.mouse_down = False
                self.show_options = not self.show_options
        else:
            # When the user is not hovering over the checkbox, set the background to the default background
            self.image = self.default
            
    def draw(self, screen):
        # Draws the background
        screen.blit(self.image, self.rect)
        
        if self.show_options:
            y = self.y + self.width
            font = pygame.font.SysFont(self.font, self.width)
            for option in self.options:
                screen.blit(font.render(f"{option}", True, self.text_colour), (self.x, y))
                y += self.width
            
        # Draw a rectangle around the box
        pygame.draw.line(screen,self.text_colour,(self.x,self.y),(self.x+self.length,self.y), 2)
        pygame.draw.line(screen,self.text_colour,(self.x,self.y),(self.x,self.y+self.width), 2)
        pygame.draw.line(screen,self.text_colour,(self.x+self.length,self.y),(self.x+self.length,self.y+self.width), 2)
        pygame.draw.line(screen,self.text_colour,(self.x,self.y+self.width),(self.x+self.length,self.y+self.width), 2)

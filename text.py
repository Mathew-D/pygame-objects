#Made by: Mathew Dusome
#Updated by: Spencer Puckrin (Oct 30 2024)
#Provides text rendering and text input field functionality
#Features: multi-line text, custom input fields, character filtering, selection cursor, highlight color
#
#IMPORT:
#    import objects.text
#
#USAGE PATTERN:
#    1. Create text input object (outside main loop)
#    2. In EVENT LOOP: call txt_name.update(pygame.mouse.get_pos(), event)
#    3. In DISPLAY LOOP: call txt_name.draw(window)
#
#PARAMETERS for input object:
#    start_x, start_y    --> Position on screen (top-left)
#    width, height        --> Size of input field
#    font_name           --> Font name (e.g., 'Consolas', 'Arial')
#    font_size           --> Font size in pixels
#    text_color          --> Text color when inactive (RGB tuple)
#    back_color          --> Background color (RGB tuple)
#    text_hover_color    --> Text color when active (default: blue)
#    back_hover_color    --> Background color when active (default: light blue)
#    starting_text       --> Pre-filled text (default: empty)
#    max_length          --> Maximum characters allowed (default: 20)
#    text_offset         --> Padding inside field (default: (5,5))
#    border_colour       --> Border color (default: black)
#    char_list           --> Character filter: whitelist or blacklist
#    is_blacklist        --> If True, char_list blocks those chars; if False, allows only those chars
#
#EXAMPLE 1: Multi-line text
#    font = pygame.font.SysFont('Consolas', 24)
#    objects.text.blit_text(window, 'Line 1\nLine 2\nLine 3', (20, 20), font)
#
#EXAMPLE 2: Basic text input field
#    txt_name = objects.text.input(10, 400, 200, 40, 'Consolas', 30, (0,0,0), (255,255,255))
#    # In EVENT LOOP:
#    #   txt_name.update(pygame.mouse.get_pos(), event)
#    # In DISPLAY LOOP:
#    #   txt_name.draw(window)
#    # Read text:
#    #   inputed_text = txt_name.text
#
#EXAMPLE 3: Numbers only input
#    score_input = objects.text.input(10, 460, 200, 40, 'Consolas', 28, (0,0,0), (255,255,255),
#                                    max_length=6, char_list='0123456789')
#
#EXAMPLE 4: Letters and spaces only
#    name_input = objects.text.input(10, 510, 260, 40, 'Consolas', 28, (0,0,0), (255,255,255),
#                                   char_list='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
#
#EXAMPLE 5: Block specific characters (blacklist mode)
#    chat_input = objects.text.input(10, 560, 300, 40, 'Consolas', 28, (0,0,0), (255,255,255),
#                                   char_list='0123456789', is_blacklist=True)
#
#EXAMPLE 6: With starting text and max length
#    username_input = objects.text.input(10, 610, 260, 40, 'Consolas', 28, (0,0,0), (255,255,255),
#                                       starting_text='Player1', max_length=12)

import pygame
def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    #From https://stackoverflow.com/questions/42014195/rendering-text-with-multiple-lines-in-pygame
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.
class input(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,width,height, font_name,font_size,text_color,back_color,text_hover_color=(0, 86, 179),back_hover_color=(230, 242, 255),starting_text="",max_length=20,text_offset=(5,5),border_colour=(0,0,0),char_list="",is_blacklist=False):
        super().__init__()
        self.image = pygame.Surface([width+4, height+4],pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.writing = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()
       
        self.font_used = pygame.font.SysFont(font_name, font_size)
        self.font_size = font_size
       
        self.back_color=back_color
        self.back_hover_color=back_hover_color
        self.text_color = text_color
        self.text_hover_color = text_hover_color
        self.border_colour = border_colour
        self.text=starting_text
        self.max_length = max_length
       
        self.rect = self.image.get_rect(topleft =(start_x,start_y))
        self.is_active = False
        self.select_loc = 0
        self.blink = 0
        
        self.text_offset = text_offset

        #a whitelist for characters. is is_blacklist is true it is used as a blacklist instead.
        self.char_list = char_list
        self.is_blacklist = is_blacklist

        self.last_btn = (-1,"a")
        self.spam_delay = 0


        self.write()
    def write(self):
        self.image.fill(self.border_colour)
        if self.is_active:
            self.text_surface = self.font_used.render(self.text, True, self.text_hover_color)      
            self.writing.fill(self.back_hover_color)  
        else:
            self.text_surface = self.font_used.render(self.text, True, self.text_color)      
            self.writing.fill(self.back_color)  
        self.writing.blit(self.text_surface,self.text_offset)
        self.image.blit(self.writing, (2, 2))
        
    def update(self,pos,event):                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click is within the text input rect
            self.is_active = self.rect.collidepoint(pos)
            self.blink = 0
            if self.is_active:
                try:
                    self.select_loc = self.select_location_binary_search(0,len(self.text),pygame.mouse.get_pos()[0]-self.rect.x-self.text_offset[0])
                except:
                    self.select_loc = len(self.text)
        elif event.type == pygame.KEYDOWN and self.is_active:     
            self.key_press(event.key,event.unicode)  
        self.write() 
        
    def key_press(self,key,char):         
        #handles functonality of different possible inputs
        if key == pygame.K_BACKSPACE:
            if self.select_loc > 0:
                self.text = self.text[:self.select_loc-1]+self.text[self.select_loc:]
                self.select_loc -= 1
        elif key == pygame.K_DELETE:
            if self.select_loc < len(self.text):
                self.text = self.text[:self.select_loc]+self.text[self.select_loc+1:]
        #elif key == pygame.K_RETURN:
            #return(self.text)  # You can modify this to handle the entered text
            #self.text = ""
        elif key == pygame.K_LEFT and self.select_loc > 0:
            self.select_loc -= 1
            self.blink = 0
        elif key == pygame.K_RIGHT and self.select_loc < len(self.text):
            self.select_loc += 1
            self.blink = 0
        elif key == pygame.K_DOWN or key == pygame.K_END:
            self.select_loc = len(self.text)
        elif key == pygame.K_UP:
            self.select_loc = 0
        elif len(self.text) < self.max_length and not char == "" and (self.char_list=="" or (not (char in self.char_list)==self.is_blacklist)):
            self.text = self.text[:self.select_loc]+char+self.text[self.select_loc:] 
            self.select_loc +=1
        self.last_btn = (key,char)
        self.spam_delay = 30
        self.write() 
        
    def draw(self, screen):
        # Render the text surface
        screen.blit(self.image,self.rect)
        if self.is_active:
            if self.blink < 0:
                select_rect = self.font_used.render(self.text[:self.select_loc], False, self.text_color).get_rect()
                
                pygame.draw.rect(screen,self.text_hover_color,(self.rect.x+select_rect.width+self.text_offset[0],self.rect.y+self.text_offset[1],3,select_rect.height))
            #makes the cursor blink            
            if self.blink < -30:
                self.blink = 30
            self.blink -=1

            #holding the same button will spam press it
            if pygame.key.get_pressed()[self.last_btn[0]]:
                self.spam_delay -=1
                if self.spam_delay <= 0:
                    self.key_press(self.last_btn[0],self.last_btn[1])
                    self.spam_delay = 3
        
        
    def select_location_binary_search(self,min,max,loc):  
        #finds which character is closest to loc
            
        # Check base case
        if max >= min:

            mid = (max + min) // 2
            
            
            mid_loc = self.font_used.render(self.text[:mid], False, (0,0,0)).get_rect().width
            #print(f'Shift: {mid_loc-loc}    mid: {self.text[:mid]}      min-max:  {self.text[min:max]}')
            
            # If element is present at the middle itself
            if min == mid or max == mid or mid_loc==loc:
                next_loc = self.font_used.render(self.text[:mid+1], False, (0,0,0)).get_rect().width
                if abs(mid_loc-loc) <= abs(next_loc-loc):
                    return mid
                else:
                    return mid+1
            # If element is smaller than mid, then it can only
            # be present in left subarray
            elif loc < mid_loc:
                return self.select_location_binary_search(min, mid, loc)

            # Else the element can only be present in right subarray
            else:
                return self.select_location_binary_search(mid, max, loc)

        else:
            # Element is not present in the array
            return -1

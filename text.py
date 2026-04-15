#Made by: Mathew Dusome
#Updated by: Spencer Puckrin (Oct 30 2024)
#Provides text input field functionality
#Features: custom input fields, character filtering, selection cursor, highlight color
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
#    font_name           --> System font name (e.g., 'Consolas', 'Arial')
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
#    multiline           --> If True, enables multi-line input with automatic line wrapping
#    download_font_name  --> Path to downloaded font file (e.g., 'fonts/MyFont.ttf') - overrides font_name if provided
#
#EXAMPLE 1: Basic text input field - system font
#    txt_name = objects.text.input(10, 400, 200, 40, font_name='Consolas', font_size=30, text_color=(0,0,0), back_color=(255,255,255))
#    # In EVENT LOOP:
#    #   txt_name.update(pygame.mouse.get_pos(), event)
#    # In DISPLAY LOOP:
#    #   txt_name.draw(window)
#    # Read text:
#    #   inputed_text = txt_name.text
#
#EXAMPLE 1b: Text input with downloaded font only
#    txt_name = objects.text.input(10, 400, 200, 40, font_size=30, text_color=(0,0,0), back_color=(255,255,255),
#                                 download_font_name='fonts/MyFont.ttf')
#
#EXAMPLE 2: Numbers only input
#    score_input = objects.text.input(10, 460, 200, 40, font_name='Consolas', font_size=28, text_color=(0,0,0), back_color=(255,255,255),
#                                    max_length=6, char_list='0123456789')
#
#EXAMPLE 3: Letters and spaces only
#    name_input = objects.text.input(10, 510, 260, 40, font_name='Consolas', font_size=28, text_color=(0,0,0), back_color=(255,255,255),
#                                   char_list='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ ')
#
#EXAMPLE 4: Block specific characters (blacklist mode)
#    chat_input = objects.text.input(10, 560, 300, 40, font_name='Consolas', font_size=28, text_color=(0,0,0), back_color=(255,255,255),
#                                   char_list='0123456789', is_blacklist=True)
#
#EXAMPLE 5: With starting text and max length
#    username_input = objects.text.input(10, 610, 260, 40, font_name='Consolas', font_size=28, text_color=(0,0,0), back_color=(255,255,255),
#                                       starting_text='Player1', max_length=12)
#
#EXAMPLE 6: Multi-line wrapped input field
#    notes_input = objects.text.input(10, 660, 320, 120, font_name='Consolas', font_size=24, text_color=(0,0,0), back_color=(255,255,255),
#                                    max_length=500, multiline=True)
#
#EXAMPLE 7: Multi-line input with downloaded font
#    notes_input = objects.text.input(10, 660, 320, 120, font_size=24, text_color=(0,0,0), back_color=(255,255,255),
#                                    max_length=500, multiline=True, download_font_name='fonts/MyFont.ttf')

import pygame

class input(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,width,height,font_name=None,font_size=24,text_color=(0,0,0),back_color=(255,255,255),text_hover_color=(0, 86, 179),back_hover_color=(230, 242, 255),starting_text="",max_length=20,text_offset=(5,5),border_colour=(0,0,0),char_list="",is_blacklist=False,multiline=False,download_font_name=None):
        super().__init__()
        self.image = pygame.Surface([width+4, height+4],pygame.SRCALPHA).convert_alpha()
        self.image.fill((0, 0, 0, 0))
        self.writing = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()
       
        if download_font_name:
            self.font_used = pygame.font.Font(download_font_name, font_size)
        elif font_name:
            self.font_used = pygame.font.SysFont(font_name, font_size)
        else:
            self.font_used = pygame.font.SysFont('arial', font_size)
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
        self.multiline = multiline
        self.line_height = self.font_used.get_linesize()

        self.last_btn = (-1,"a")
        self.spam_delay = 0


        self.write()

    def _allowed_char(self, char):
        return self.char_list == "" or (not (char in self.char_list) == self.is_blacklist)

    def _insert_char(self, char):
        if len(self.text) < self.max_length and char != "" and self._allowed_char(char):
            self.text = self.text[:self.select_loc] + char + self.text[self.select_loc:]
            self.select_loc += 1

    def _get_wrapped_lines(self):
        # Keep track of source string index ranges so selection can map to wrapped lines.
        max_width = max(1, self.writing.get_width() - (self.text_offset[0] * 2))
        lines = []
        line_start = 0
        current = ""

        for i, ch in enumerate(self.text):
            if ch == "\n":
                lines.append({"text": current, "start": line_start, "end": i})
                current = ""
                line_start = i + 1
                continue

            candidate = current + ch
            if current == "" or self.font_used.size(candidate)[0] <= max_width:
                current = candidate
            else:
                lines.append({"text": current, "start": line_start, "end": i})
                line_start = i
                current = ch

        lines.append({"text": current, "start": line_start, "end": len(self.text)})

        if len(lines) == 0:
            lines = [{"text": "", "start": 0, "end": 0}]

        return lines

    def _closest_index_in_line(self, line_text, loc):
        if len(line_text) == 0 or loc <= 0:
            return 0

        if loc >= self.font_used.size(line_text)[0]:
            return len(line_text)

        low = 0
        high = len(line_text)
        while low < high:
            mid = (low + high) // 2
            if self.font_used.size(line_text[:mid])[0] < loc:
                low = mid + 1
            else:
                high = mid

        right = low
        left = max(0, right - 1)
        left_width = self.font_used.size(line_text[:left])[0]
        right_width = self.font_used.size(line_text[:right])[0]

        if abs(loc - left_width) <= abs(right_width - loc):
            return left
        return right

    def _cursor_pos_from_index(self):
        if not self.multiline:
            x = self.font_used.render(self.text[:self.select_loc], False, self.text_color).get_rect().width
            return x, 0

        lines = self._get_wrapped_lines()
        for i, line in enumerate(lines):
            if line["start"] <= self.select_loc <= line["end"]:
                offset = self.select_loc - line["start"]
                x = self.font_used.size(line["text"][:offset])[0]
                y = i * self.line_height
                return x, y

        # Fallback to end of last visual line.
        last = lines[-1]
        return self.font_used.size(last["text"])[0], (len(lines) - 1) * self.line_height

    def _select_location_multiline(self, x, y):
        lines = self._get_wrapped_lines()
        line_index = max(0, min(len(lines) - 1, y // self.line_height))
        line = lines[line_index]
        line_offset = self._closest_index_in_line(line["text"], x)
        return line["start"] + line_offset

    def _move_cursor_up(self):
        """Move cursor up one line in multiline mode, preserving horizontal position."""
        if not self.multiline:
            self.select_loc = 0
            return

        lines = self._get_wrapped_lines()
        cursor_x, cursor_y = self._cursor_pos_from_index()
        current_line = cursor_y // self.line_height

        if current_line > 0:
            new_line = current_line - 1
            line = lines[new_line]
            new_index = self._closest_index_in_line(line["text"], cursor_x)
            self.select_loc = line["start"] + new_index
        else:
            # Already on first line, move to its beginning
            self.select_loc = 0

    def _move_cursor_down(self):
        """Move cursor down one line in multiline mode, preserving horizontal position."""
        if not self.multiline:
            self.select_loc = len(self.text)
            return

        lines = self._get_wrapped_lines()
        cursor_x, cursor_y = self._cursor_pos_from_index()
        current_line = cursor_y // self.line_height

        if current_line < len(lines) - 1:
            new_line = current_line + 1
            line = lines[new_line]
            new_index = self._closest_index_in_line(line["text"], cursor_x)
            self.select_loc = line["start"] + new_index
        else:
            # Already on last line, move to its end
            self.select_loc = len(self.text)

    def write(self):
        self.image.fill(self.border_colour)
        current_text_color = self.text_hover_color if self.is_active else self.text_color
        current_back_color = self.back_hover_color if self.is_active else self.back_color

        self.writing.fill(current_back_color)

        if self.multiline:
            lines = self._get_wrapped_lines()
            for i, line in enumerate(lines):
                y = self.text_offset[1] + (i * self.line_height)
                if y + self.line_height > self.writing.get_height():
                    break
                line_surface = self.font_used.render(line["text"], True, current_text_color)
                self.writing.blit(line_surface, (self.text_offset[0], y))
        else:
            self.text_surface = self.font_used.render(self.text, True, current_text_color)
            self.writing.blit(self.text_surface, self.text_offset)

        self.image.blit(self.writing, (2, 2))
        
    def update(self,pos,event):                    
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse click is within the text input rect
            self.is_active = self.rect.collidepoint(pos)
            self.blink = 0
            if self.is_active:
                try:
                    local_x = pygame.mouse.get_pos()[0] - self.rect.x - self.text_offset[0]
                    local_y = pygame.mouse.get_pos()[1] - self.rect.y - self.text_offset[1]
                    if self.multiline:
                        self.select_loc = self._select_location_multiline(local_x, local_y)
                    else:
                        self.select_loc = self.select_location_binary_search(0, len(self.text), local_x)
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
        elif key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            if self.multiline:
                self._insert_char("\n")
        elif key == pygame.K_LEFT and self.select_loc > 0:
            self.select_loc -= 1
            self.blink = 0
        elif key == pygame.K_RIGHT and self.select_loc < len(self.text):
            self.select_loc += 1
            self.blink = 0
        elif key == pygame.K_DOWN:
            self._move_cursor_down()
            self.blink = 0
        elif key == pygame.K_UP:
            self._move_cursor_up()
            self.blink = 0
        elif key == pygame.K_END:
            self.select_loc = len(self.text)
        else:
            self._insert_char(char)
        self.last_btn = (key,char)
        self.spam_delay = 30
        self.write() 
        
    def draw(self, screen):
        # Render the text surface
        screen.blit(self.image,self.rect)
        if self.is_active:
            if self.blink < 0:
                cursor_x, cursor_y = self._cursor_pos_from_index()
                pygame.draw.rect(screen, self.text_hover_color, (self.rect.x + cursor_x + self.text_offset[0], self.rect.y + cursor_y + self.text_offset[1], 3, self.font_size))
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

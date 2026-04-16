#Made by: Mathew Dusome
#Date: Apr 15 2026
#Provides read-only label text rendering functionality
#Features: multiline labels with optional background and border
#
#IMPORT:
#    import objects.label
#
#USAGE PATTERN:
#    1. Create label object (outside main loop)
#    2. In DISPLAY LOOP: call label_name.draw(window)
#
#PARAMETERS for label object:
#    start_x, start_y    --> Position on screen (top-left)
#    width, height        --> Size of label area
#    font_name            --> System font name (e.g., 'Consolas', 'Arial')
#    font_size            --> Font size in pixels
#    text_color           --> Text color (RGB tuple)
#    back_color           --> Background color (RGB/RGBA tuple, default: transparent)
#    text                 --> Starting label text
#    text_offset          --> Padding inside label (default: (5,5))
#    border_colour        --> Border color (default: black)
#    download_font_name   --> Path to downloaded font file (overrides font_name)
#    show_border          --> Draw border around label (default: True)
#
#EXAMPLE 1: Basic read-only label
#    lbl_title = objects.label.label(20, 20, 220, 40, font_name='Consolas', font_size=28, text='Score: 0')
#    # In DISPLAY LOOP:
#    #   lbl_title.draw(window)
#
#EXAMPLE 2: Set label text during runtime
#    lbl_title.set_text('Score: 12')
#
#EXAMPLE 3: Get label text
#    current_text = lbl_title.get_text()
#
#EXAMPLE 4: Multi-line label text
#    lbl_notes = objects.label.label(20, 70, 300, 120, font_name='Consolas', font_size=24, text='Line 1\nLine 2\nLine 3')
#
#EXAMPLE 5: Label with downloaded font only
#    lbl_downloaded = objects.label.label(20, 20, 260, 48, font_size=30, text='Welcome',
#                                        download_font_name='fonts/MyFont.ttf')

import pygame

class label(pygame.sprite.Sprite):
    def __init__(self,start_x,start_y,width,height,font_name=None,font_size=24,text_color=(0,0,0),back_color=(0,0,0,0),text="",text_offset=(5,5),border_colour=(0,0,0),download_font_name=None,show_border=True):
        super().__init__()
        self.show_border = show_border

        if self.show_border:
            self.image = pygame.Surface([width+4, height+4],pygame.SRCALPHA).convert_alpha()
        else:
            self.image = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()
        self.writing = pygame.Surface([width, height],pygame.SRCALPHA).convert_alpha()

        if download_font_name:
            self.font_used = pygame.font.Font(download_font_name, font_size)
        elif font_name:
            self.font_used = pygame.font.SysFont(font_name, font_size)
        else:
            self.font_used = pygame.font.SysFont('arial', font_size)

        self.text_color = text_color
        self.back_color = back_color
        self.border_colour = border_colour
        self.text_offset = text_offset
        self.text = text
        self.line_height = self.font_used.get_linesize()

        self.rect = self.image.get_rect(topleft =(start_x,start_y))
        self.write()

    def set_text(self, text):
        self.text = str(text)
        self.write()

    def get_text(self):
        return self.text

    def _get_wrapped_lines(self):
        max_width = max(1, self.writing.get_width() - (self.text_offset[0] * 2))
        wrapped_lines = []

        for paragraph in self.text.split("\n"):
            if paragraph == "":
                wrapped_lines.append("")
                continue

            current = ""
            for word in paragraph.split(" "):
                candidate = word if current == "" else current + " " + word
                if self.font_used.size(candidate)[0] <= max_width:
                    current = candidate
                else:
                    if current != "":
                        wrapped_lines.append(current)

                    if self.font_used.size(word)[0] <= max_width:
                        current = word
                    else:
                        chunk = ""
                        for char in word:
                            next_chunk = chunk + char
                            if chunk == "" or self.font_used.size(next_chunk)[0] <= max_width:
                                chunk = next_chunk
                            else:
                                wrapped_lines.append(chunk)
                                chunk = char
                        current = chunk

            wrapped_lines.append(current)

        if len(wrapped_lines) == 0:
            wrapped_lines = [""]

        return wrapped_lines

    def write(self):
        self.image.fill((0,0,0,0))
        if self.show_border:
            pygame.draw.rect(self.image, self.border_colour, self.image.get_rect(), 2)
        self.writing.fill(self.back_color)

        lines = self._get_wrapped_lines()
        for i, line in enumerate(lines):
            y = self.text_offset[1] + (i * self.line_height)
            if y + self.line_height > self.writing.get_height():
                break
            line_surface = self.font_used.render(line, True, self.text_color)
            self.writing.blit(line_surface, (self.text_offset[0], y))

        if self.show_border:
            self.image.blit(self.writing, (2, 2))
        else:
            self.image.blit(self.writing, (0, 0))

    def draw(self, screen):
        screen.blit(self.image,self.rect)

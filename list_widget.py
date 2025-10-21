import pygame
#Made by: Mathew Dusome
#Date: Dec 8 2024
#Basic List Box and Combo Box
#Both have basic functionality and defaults
#To use the ListWidget, create a list of items and pass it to the constructor
#To use the ComboBox, create a list of items and pass it to the constructor
#Import the object with:
#       import objects.list_widget
#Make a copy of the object:
#       list_widget = objects.list_widget.ListWidget(50, 50, 300, 200,[])
#       list_widget = objects.list_widget.ListWidget(50, 50, 300, 200,list_of_items)
#Display method or while loop: 
#       list_widget.draw(window)
#For event loop: 
#       list_widget.handle_event(event) 
#If you want to update items use: 
#       list_widget.set_items(list_of_items)
#Change 2d list to 1d for easy display where result is the 2d list
#    result_string = [' '.join(map(str, t)) for t in result]
class ListWidget(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, items,font_size=36,system_font_name=None,download_font_name=None, item_height=40, margin=5,highlight_color=(255, 255, 255),text_color=(0, 0, 0),border_color=(0, 0, 0),highlight_color_bg=(100, 149, 237),background_color = (200, 200, 200)):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.items = items
        
        if not download_font_name:
            self.font=pygame.font.SysFont(system_font_name, font_size)
        else:
            self.font=pygame.font.Font(download_font_name, font_size) 
        self.item_height = item_height
        self.margin = margin
        self.selected_index = -1
        self.scroll_offset = 0
        self.visible_items_count = height // item_height
        self.highlight_color_bg = highlight_color_bg
        self.highlight_color=highlight_color
        self.text_color=text_color
        self.border_color=border_color
        # Create sprite group for items
        self.items_sprites = pygame.sprite.Group()

        # Initialize item sprites
        self._create_item_sprites()

        # Background color for the list container (fixed)
        self.background_color = background_color
        self.update_output()
    def _create_item_sprites(self):
        """Creates sprites for each item and adds them to the sprite group."""
        self.items_sprites.empty()  # Clear any previous items
        for index, item in enumerate(self.items):
            item_sprite = pygame.sprite.Sprite()
            item_sprite.image = self.font.render(f"{item}", True, (0, 0, 0))  # Use the font for the text            
            # Adjust positions relative to self.image
            y_position = index * self.item_height  # This is the y-position of the item within the list
            item_sprite.rect = item_sprite.image.get_rect(topleft=(self.margin, y_position))
            
            # Add the sprite to the group
            self.items_sprites.add(item_sprite)
    def set_items(self, items):
        self.items=items
        self._create_item_sprites()
        self._update_item_positions()
        self.update_output()
    
    def handle_event(self, event):
        """Handles events such as mouse clicks and scrolling."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = event.pos
                if self.rect.collidepoint(mouse_x, mouse_y):
                    relative_y = mouse_y - self.rect.y
                    index = (relative_y // self.item_height) + self.scroll_offset
                    if 0 <= index < len(self.items):
                        self.selected_index = index
                        self._update_item_selection()
                self.update_output()

        # ✅ Use MOUSEWHEEL for consistent scrolling
        elif event.type == pygame.MOUSEWHEEL:
            if len(self.items) > self.visible_items_count:
                self.scroll_offset = max(0, min(len(self.items) - self.visible_items_count, self.scroll_offset - event.y))
                self._update_item_positions()
                self.update_output()

    
    
    def _update_item_positions(self):
        """Update the position of each item sprite based on the scroll offset."""
        for i, item_sprite in enumerate(self.items_sprites):
            # Calculate the vertical position for each item based on its index and the scroll offset
            y_position = i * self.item_height - self.scroll_offset * self.item_height

            # Position the sprite on the image (relative to the container)
            item_sprite.rect.y = y_position


    def _update_item_selection(self):
        """Update the selection state of each item."""
        for i, item_sprite in enumerate(self.items_sprites):
            # Create a new surface for the item's background
            item_surface = pygame.Surface((self.rect.width,item_sprite.rect.height))

            if i == self.selected_index:
                # Highlighted background for selected item
                item_surface.fill(self.highlight_color_bg)  # Highlight color
                text_color = (self.highlight_color)         # Text color for highlighted items
            else:
                # Default background for unselected items
                item_surface.fill(self.background_color)    # Use the widget's background color
                text_color = self.text_color                # Default text color

            # Render text 
            text_surface = self.font.render(self.items[i], True, text_color)
            item_surface.blit(text_surface, item_surface.get_rect())

            # Update the sprite's image
            item_sprite.image = item_surface


    def update_output(self):
        self.image.fill(self.background_color)
        
        # Convert the sprite group to a list and slice to get only the visible items
        items_list = list(self.items_sprites)
        for i, item_sprite in enumerate(items_list[self.scroll_offset:self.scroll_offset + self.visible_items_count]):
            self.image.blit(item_sprite.image, item_sprite.rect)   
        pygame.draw.rect(self.image, self.border_color, pygame.Rect(0, 0, self.rect.width-1, self.rect.height-1), 2)
    def draw(self, screen):
        """Draws the list widget and its items."""
        # Draw the background for the list widget (this doesn't scroll)
        screen.blit(self.image,self.rect)
    def get_selected_item(self):
        """Returns the currently selected item or None if no selection."""
        if 0 <= self.selected_index < len(self.items):
            return self.items[self.selected_index]
        else: return None
    
class ComboBox(ListWidget):
    def __init__(self, x, y, width, height, items, font_size=36,system_font_name=None,download_font_name=None, item_height=40, margin=5,highlight_color=(255, 255, 255),text_color=(0, 0, 0),border_color=(0, 0, 0),highlight_color_bg=(100, 149, 237),background_color = (200, 200, 200)):
        # Initialize ComboBox-specific attributes first
        self.button_color = (150, 150, 150)
        self.is_expanded = False  # Tracks whether the combo box is expanded
        self.dropdown_button_width = 30  # Width of the dropdown button
        self.collapsed_height = item_height

        # Call the parent class's initializer
        super().__init__(x, y, width, height, items, font_size,system_font_name,download_font_name, item_height, margin,highlight_color,text_color,border_color,highlight_color_bg,background_color)

        # Adjust height for the collapsed state
        self.rect.height = self.collapsed_height
        self.image = pygame.Surface([self.rect.width, self.rect.height])
        
        self.update_output()
    def handle_event(self, event):
        """Handle events for the combo box, including toggling expansion."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_x, mouse_y = event.pos
            if self.rect.collidepoint(mouse_x, mouse_y):  # Click inside the combo box
                # Check if the click is on the dropdown button
                if mouse_x > self.rect.right - self.dropdown_button_width:
                    # Toggle expansion
                    self.is_expanded = not self.is_expanded
                    self.rect.height = (self.collapsed_height if not self.is_expanded
                        else self.item_height * min(self.visible_items_count, len(self.items)))
                    self.image = pygame.Surface([self.rect.width, self.rect.height])
                else:
                    # Handle selection if expanded
                    if self.is_expanded:
                        relative_y = mouse_y - self.rect.y
                        index = relative_y // self.item_height
                        if 0 <= index < len(self.items):
                            self.selected_index = index
                            self.is_expanded = False  # Collapse after selection
                            self.rect.height = self.collapsed_height
                            self.image = pygame.Surface([self.rect.width, self.rect.height])
                            self._update_item_selection()
            self.update_output()

        # Handle scrolling if expanded
        elif self.is_expanded:
            super().handle_event(event)

    def update_output(self):
        """Draw the combo box based on its state."""
        self.image.fill(self.background_color)

        if self.is_expanded:
            # Draw the full list
            super().update_output()
        else:
            # Draw only the selected item
            selected_item_text = (self.font.render(self.get_selected_item() or "Select...", True, self.text_color))
            self.image.blit(selected_item_text, (self.margin, self.margin))

        # Draw the dropdown button
        pygame.draw.rect(self.image,self.button_color,
            pygame.Rect(self.rect.width - self.dropdown_button_width, 0, self.dropdown_button_width, self.collapsed_height),)
        pygame.draw.polygon(self.image,self.text_color,[(self.rect.width - self.dropdown_button_width + 5, self.collapsed_height // 3),
                (self.rect.width - 5, self.collapsed_height // 3),
                (self.rect.width - self.dropdown_button_width // 2,2 * self.collapsed_height // 3, ), ],)  # Down arrow
        # Draw border
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), 2)


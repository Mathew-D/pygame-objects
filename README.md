# pygame-objects

A collection of reusable pygame sprite objects for building games quickly. Includes buttons, checkboxes, text input, images, grids, lists, and database utilities.

## Modules

### buttons.py
Three button types for user interaction:
- **no_background**: Text-only buttons with hover color
- **with_background**: Buttons with text and background colors
- **with_images**: Image-based buttons with hover states

**Usage:**
```python
import objects.buttons
btn = objects.buttons.no_background(0, 0, "Arial", 12, (235, 64, 52), (98, 52, 235), "Click Me")
if btn.update(pygame.mouse.get_pos(), event):
    print("Button clicked")
btn.draw(window)
```

### checkbox.py
Checkbox and radio button widgets.
- **check_box**: Individual checkboxes with customizable appearance
- **radio_button**: Radio buttons that work in groups (only one can be selected)
- **ButtonGroup**: Group container for managing radio buttons

**Usage:**
```python
import objects.checkbox as checkbox
chk = checkbox.check_box(50, 50, size=30)
chk.update(pygame.mouse.get_pos(), event)
chk.draw(window)
```

### text.py
Text rendering and input fields.
- **blit_text()**: Render multi-line text with word wrapping
- **input**: Custom text input field with character filtering and selection

**Usage:**
```python
import objects.text
txt_input = objects.text.input(10, 400, 200, 40, 'Consolas', 30, (0,0,0), (255,255,255))
txt_input.update(pygame.mouse.get_pos(), event)
txt_input.draw(window)
entered_text = txt_input.text
```

### image.py
Image and animation handling.
- **still**: Display static images with scaling and transparency
- **animated**: Animated GIFs with frame control

**Usage:**
```python
import objects.image as image
img = image.still(0, 0, 800, 600, "images/background.png")
img.draw(window)

# For animated GIFs (requires: pip install pillow)
anim = image.animated(100, 200, 64, 64, "images/sprite.gif", 100)
anim.update()  # Call in game loop
anim.draw(window)
```

### database.py
SQLite database helper functions for data persistence.
- **create_connection()**: Connect to database file
- **create_table()**: Create new table with columns
- **insert_db()**: Add records
- **select_db()**: Query records
- **update_db()**: Modify existing records
- **delete_db()**: Remove records

**Usage:**
```python
import objects.database as db
conn = db.create_connection('game.db')
db.create_table(conn, "scores", ["player TEXT", "score INTEGER"])
db.insert_db(conn, "scores", ["player", "score"], ["Alice", 1000])
results = db.select_db(conn, "scores").fetchall()
```

### text_files.py
Read and write lists to text files.
- **strings_write()**: Save list of strings to file
- **strings_read()**: Load list of strings from file
- **int_write()**: Save list of integers to file
- **int_read()**: Load list of integers from file

**Usage:**
```python
import objects.text_files as text_files
names = ["Alice", "Bob", "Charlie"]
text_files.strings_write(names, "names.txt")
loaded_names = text_files.strings_read("names.txt")
```

### grid.py
Grid widget for displaying data in rows and columns.

### list_widget.py
List widget for displaying and selecting items.

## Installation

Simply import the modules:
```python
import objects.buttons
import objects.text
import objects.image
import objects.database
# etc.
```

For animated GIFs, install Pillow:
```bash
pip install pillow
```

## Game Loop Pattern

Most objects follow this pattern:

```python
# Setup (outside loop)
button = objects.buttons.no_background(...)

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if button.update(pygame.mouse.get_pos(), event):
            # Handle button click
            pass
    
    # Display
    window.fill((255, 255, 255))
    button.draw(window)
    pygame.display.flip()
```

## Credits

- Made by: Mathew Dusome
- Contributions by: Spencer Puckrin, Riley Czarkowski
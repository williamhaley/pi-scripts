class LCDMenu():
    """
    Navigate our menu hierarchy. Set colors, run actions, enter sub-menus, etc.
    """
    def __init__(self, lcd, menu):
        self.lcd = lcd
        self.menus = [menu]
        self.indexes = [0]
        self.current_color = (1.0, 1.0, 1.0)
        self._create_custom_chars()
        self.update_menu()

    def _create_custom_chars(self):
        """
        Create custom characters and shapes.
        https://www.quinapalus.com/hd44780udg.html
        """
        # Accessible using escape code \x01 in a string
        self.lcd.create_char(1, [0x4, 0xc, 0x1f, 0xd, 0x5, 0x1, 0xe , 0x0])

    def current_menu(self):
        # Make a copy so we can manipulate it
        current_menu = list(self.menus[-1])
        if self.in_sub_menu():
            # Add a back button
            current_menu.append({ 'text': '\x01 Back', 'action': self.prev_menu })
        return current_menu

    def current_item(self):
        return self.current_menu()[self.indexes[-1]]

    def in_sub_menu(self):
        return len(self.indexes) > 1

    def select(self):
        current_item = self.current_item()
        if 'action' in current_item:
            current_item['action']()
        elif 'menu' in current_item:
            self.menus.append(current_item['menu'])
            self.indexes.append(0)
            self.update_menu()

    def prev_menu(self):
        self.menus.pop()
        self.indexes.pop()
        self.update_menu()

    def left(self):
        self._nav(self.indexes[-1] - 1)

    def right(self):
        self._nav(self.indexes[-1] + 1)

    def _nav(self, new_index):
        menu = self.current_menu()
        self.indexes[-1] = len(menu) - 1 if new_index < 0 else 0 if new_index >= len(menu) else new_index
        self.update_menu()

    def update_menu(self):
        self.lcd.clear()
        if 'color' in self.current_item():
            self.current_color = self.current_item()['color']
        self.lcd.set_color(self.current_color[0], self.current_color[1], self.current_color[2])
        self.lcd.message(self.current_item()['text'])

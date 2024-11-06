import pyperclip # type: ignore

class String:
    def __init__(self, visible_lines_count = 9, input_box_height=50, input_box_width = 600):
        self.user_text = ""
        self.lines = [""]
        self.scroll_index = 0
        self.visible_lines_count = visible_lines_count
        self.input_box_height = input_box_height
        self.input_box_width = input_box_width

    def add(self, char, actual_height, font):
        self.lines[-1] += char
        if font.size(self.lines[-1])[0] > self.input_box_width:
            self.lines.append("")
            if actual_height != self.input_box_height * self.visible_lines_count:
                return True
            else:
                self.scroll_index += 1
        return False

    def pop(self):
        if len(self.lines[-1]) > 0:
            self.lines[-1] = self.lines[-1][:-1]  
        elif len(self.lines) > 1:
            self.lines.pop()
            if len(self.lines) >= self.visible_lines_count:
                self.scroll_index -= 1
                return False
            return True
        return False

    def submit(self):
        result = "".join(self.lines)
        self.scroll_index = 0
        self.lines = [""]
        return result
    
    def copy(self):
        pyperclip.copy("\n".join(self.lines))
        print("Text copied to clipboard")

    def paste(self, actual_height, font):
        count = 0
        clipboard_text = pyperclip.paste() 
        for char in clipboard_text:
            if char == '\n':
                self.lines.append("")
                if actual_height + count * self.input_box_height != self.input_box_height * self.visible_lines_count:
                    count += 1
                    
                if len(self.lines) - self.scroll_index > self.visible_lines_count:
                    self.scroll_index += 1    

            else:
                self.lines[-1] += char
                if font.size(self.lines[-1])[0] > self.input_box_width:
                    self.lines.append("")
                    if actual_height + count * self.input_box_height != self.input_box_height * self.visible_lines_count:
                        count += 1    

                    if len(self.lines) - self.scroll_index > self.visible_lines_count:
                        self.scroll_index += 1

        return count
    
    def scroll_up(self):
        if self.scroll_index > 0:
            self.scroll_index -= 1

    def scroll_down(self):
        if self.scroll_index < max(0, len(self.lines) - self.visible_lines_count):
            self.scroll_index += 1

    def visible_range(self):
        return self.lines[self.scroll_index:self.scroll_index + min(self.visible_lines_count, len(self.lines))]
    
    def lines_len(self):
        return len(self.lines) - self.scroll_index

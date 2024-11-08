import pyperclip # type: ignore
from const import *

class String:
    def __init__(self, font, visible_lines_count = 9, input_box_height=50, input_box_width = 600):
        self.user_text = ""
        self.lines = [""]
        self.scroll_index = 0
        self.visible_lines_count = visible_lines_count
        self.input_box_height = input_box_height
        self.input_box_width = input_box_width
        self.input_box = start_input_box.copy()
        self.font = font
        self.cursos_index = [0, 0]

    def add(self, char):
        self.lines[-1] += char
        if self.font.size(self.lines[-1])[0] > self.input_box_width:
            self.lines.append("")
            if self.input_box.height != self.input_box_height * self.visible_lines_count:
                self.input_box.height += input_box_height
            else:
                self.scroll_index += 1

    def pop(self):
        if len(self.lines[-1]) > 0:
            self.lines[-1] = self.lines[-1][:-1]  
        elif len(self.lines) > 1:
            self.lines.pop()
            if len(self.lines) >= self.visible_lines_count:
                self.scroll_index -= 1
                return
            self.input_box.height -= input_box_height
        return 

    def submit(self):
        result = "".join(self.lines)
        self.scroll_index = 0
        self.lines = [""]
        self.input_box = start_input_box.copy()
        return result
    
    def copy(self):
        pyperclip.copy("\n".join(self.lines))
        print("Text copied to clipboard")

    def paste(self):
        count = 0
        clipboard_text = pyperclip.paste() 
        for char in clipboard_text:
            if char == '\n':
                self.lines.append("")
                if self.input_box.height + count * self.input_box_height != self.input_box_height * self.visible_lines_count:
                    count += 1
                    
                if len(self.lines) - self.scroll_index > self.visible_lines_count:
                    self.scroll_index += 1    

            else:
                self.lines[-1] += char
                if self.font.size(self.lines[-1])[0] > self.input_box_width:
                    self.lines.append("")
                    if self.input_box.height + count * self.input_box_height != self.input_box_height * self.visible_lines_count:
                        count += 1    

                    if len(self.lines) - self.scroll_index > self.visible_lines_count:
                        self.scroll_index += 1

        self.input_box.height += input_box_height * count
    
    def scroll_up(self):
        if self.scroll_index > 0:
            self.scroll_index -= 1

    def scroll_down(self):
        if self.scroll_index < max(0, len(self.lines) - self.visible_lines_count):
            self.scroll_index += 1

    def scroll_left(self):
        pass

    def visible_range(self):
        return self.lines[self.scroll_index:self.scroll_index + min(self.visible_lines_count, len(self.lines))]
    
    def lines_len(self):
        return len(self.lines) - self.scroll_index
    
    def draw_input_box(self, screen):
        pygame.draw.rect(screen, input_box_color, self.input_box)
        for i, line in enumerate(self.visible_range()):
            line_for_render = line + '|' if self.lines_len() - 1 == i else line
            text_surface = self.font.render(line_for_render, True, text_color)
            screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10 + i * input_box_height))
    
    def generate_response_continuously(self, text, screen):
        for symbol in text:
            self.add(symbol)
            self.draw_input_box(screen)  
            pygame.display.flip()        
            pygame.time.delay(10) 


    def reset_line(self):
        self.scroll_index = 0
        self.lines = [""]
        self.input_box = start_input_box.copy()



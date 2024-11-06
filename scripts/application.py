import pygame
from const import * 
from stringInput import String

class Application:
    def __init__(self, language_model_manager):
        pygame.init()
        pygame.display.set_caption('Spam filter')
        self.screen = pygame.display.set_mode(display_size)

        self.language_model_manager = language_model_manager

        self.font = pygame.font.Font(None, input_box_height)
        self.start_input_box = pygame.Rect(75, 100, input_box_width, input_box_height)
        self.input_box = self.start_input_box.copy()
        self.input_string = String(visible_lines_count, input_box_height, input_box_width - width_eps)
        
        self.running = True
        self.showResult = False
        self.isSpam = False

    def start(self):
        while self.running:
            if not self.showResult:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            if self.input_string.pop():
                                self.input_box.height -= input_box_height

                        elif event.key == pygame.K_RETURN:
                            str = self.input_string.submit()
                            print(self.language_model_manager.generate_response(str))
                            self.input_box = self.start_input_box.copy()
                            self.showResult = True

                        elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.input_string.copy()

                        elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.input_box.height += input_box_height * self.input_string.paste(self.input_box.height, self.font)

                        elif event.key == pygame.K_UP:
                            self.input_string.scroll_up()
                        elif event.key == pygame.K_DOWN:
                            self.input_string.scroll_down()

                        else:
                            if self.input_string.add(event.unicode, self.input_box.height, self.font):
                                self.input_box.height += input_box_height

                    self.draw_parts()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.showResult = False
                    
                    self.draw_parts()

        pygame.quit()

    def draw_parts(self):
        self.screen.fill(bg_color)
        
        if not self.showResult:
            self.draw_input_box()
            self.draw_title()
        else:
            self.draw_spam_check_result()
            
        pygame.display.flip()

    def draw_input_box(self):
        pygame.draw.rect(self.screen, input_box_color, self.input_box)
        for i, line in enumerate(self.input_string.visible_range()):
            line_for_render = line + '|' if self.input_string.lines_len() - 1 == i else line
            text_surface = self.font.render(line_for_render, True, text_color)
            self.screen.blit(text_surface, (self.input_box.x + 10, self.input_box.y + 10 + i * input_box_height))


    def draw_title(self):
        for i in range(2):
            label_surface = self.font.render(title_text[i], True, text_color)
            self.screen.blit(label_surface, title_text_coordinates[i]) 

    def draw_spam_check_result(self):        
        for i in range(2):
            label_surface = self.font.render(spam_checker_text[i], True, text_color)
            self.screen.blit(label_surface, spam_checker_text_coordinates[i]) 

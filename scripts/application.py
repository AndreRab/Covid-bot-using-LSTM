import pygame
from const import * 
from stringInput import String

class Application:
    def __init__(self, language_model_manager):
        pygame.init()
        pygame.display.set_caption('Spam filter')
        self.screen = pygame.display.set_mode(display_size)

        self.language_model_manager = language_model_manager
        self.response = ""
        
        self.font = pygame.font.Font(None, input_box_height)
        self.input_string = String(self.font, visible_lines_count, input_box_height, input_box_width - width_eps)
        
        self.running = True
        self.showResult = False
        self.isSpam = False
        self.started_generate = False
        

    def start(self):
        while self.running:
            if not self.showResult:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.input_string.pop()

                        elif event.key == pygame.K_RETURN:
                            str = self.input_string.submit()
                            self.response = self.language_model_manager.generate_response(str)
                            self.showResult = True

                        elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.input_string.copy()

                        elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            self.input_string.paste()

                        elif event.key == pygame.K_UP:
                            self.input_string.scroll_up()
                        elif event.key == pygame.K_DOWN:
                            self.input_string.scroll_down()
                        elif event.key == pygame.K_LEFT:
                            pass
                            # self.input_string.scroll_up()
                        elif event.key == pygame.K_RIGHT:
                            pass
                            # self.input_string.scroll_down()

                        else:
                            self.input_string.add(event.unicode)

                    self.draw_parts()
            else:
                if not self.started_generate:
                    self.input_string.generate_response_continuously(self.response, self.screen)
                    self.started_generate = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.showResult = False
                            self.started_generate = False
                            self.input_string.reset_line()
                        elif event.key == pygame.K_UP:
                            self.input_string.scroll_up()
                        elif event.key == pygame.K_DOWN:
                            self.input_string.scroll_down()
                    
                    self.draw_parts()

        pygame.quit()

    def draw_parts(self):
        self.screen.fill(bg_color)
        
        if not self.showResult:
            self.draw_title()
        else:
            self.draw_answer()
        
        self.input_string.draw_input_box(self.screen)
        pygame.display.flip()


    def draw_title(self):
        for i in range(len(title_text)):
            label_surface = self.font.render(title_text[i], True, text_color)
            self.screen.blit(label_surface, title_text_coordinates[i]) 

    def draw_answer(self):        
        for i in range(len(answer_text)):
            label_surface = self.font.render(answer_text[i], True, text_color)
            self.screen.blit(label_surface, answer_text_coordinates[i]) 

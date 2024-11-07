import json
import pygame

text_color = (0, 0, 0)
bg_color = (255, 255, 255)
input_box_color = (200, 200, 200)

input_box_width = 700
width_eps = 50
input_box_height = 50
max_line_length = 40 
visible_lines_count = 9

display_size = (850, 600)

title_text = ['Write or copy-paste your question about COVID-19', 'For moving down use arrows']
answer_text = ['Asnwer (for the new question press backspace):']


title_text_coordinates = [(10, 10), (170, 50)]
answer_text_coordinates = [(30, 30)] 

start_input_box = pygame.Rect(75, 100, input_box_width, input_box_height)
import pygame

list = pygame.font.get_fonts()
list.sort()
print(list)


line = '1234567890'
n = 2
new_list = [line[i:i+n] for i in range(0, len(line), n)]
print(new_list)
import pygame


pygame.init()
# pygame windows resolution 300x300
pygame.display.set_mode([300, 300])

print pygame.K_UP
while True:
    pygame.event.pump()
    if pygame.key.get_pressed()[pygame.K_UP] == 1:
        print "up"
    else:
        print "no up"

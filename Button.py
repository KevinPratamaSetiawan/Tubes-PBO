import pygame

class Button():
    def __init__(self,screen,x,y,img):
        self._screen = screen
        self._img = img
        self._rect = self._img.get_rect()
        self._rect.x = x
        self._rect.y = y
        self._clicked = False

    def Place(self):
        command = False
        
        mouse_position = pygame.mouse.get_pos()
        if self._rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == True and self._clicked == False:
                self._clicked = True
                command = True

        if pygame.mouse.get_pressed()[0] == False:
            self._clicked = False
        
        self._screen.blit(self._img,(self._rect.x,self._rect.y))
        return command

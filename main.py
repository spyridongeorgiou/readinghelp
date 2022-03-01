import sys, pygame
from pygame import display
if __name__ == "__main__":
    pygame.init()
    #initializes the display
    pygame.display.init()
    flags = pygame.FULLSCREEN | pygame.SHOWN | pygame.FULLSCREEN
    #checks if display is initialized and returns a boolean value
    dinit = pygame.display.get_init()
    def displayinit():
        #get current desktop size in w x h
        current_w = pygame.display.Info().current_w
        current_h = pygame.display.Info().current_h
        print (current_w,"x",current_h)
    #launch the display
    while True: 
    surface.fill((255,255,255))   
    surface.blit(displayImage, (0, 0))  
    for event in pygame.event.get(): 
   
        if event.type == pygame.QUIT:    
            pygame.quit()  
            quit() 

        pygame.display.update()  
    pygame.display.set_caption('Image')
    displayinit()
    screen = pygame.display.set_mode((0,0),flags)
#for x in range(0,10000):
#    pygame.display.flip()

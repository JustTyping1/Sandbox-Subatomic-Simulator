import pygame

class Proton(xpos, ypos, xvel, yvel, xacc, yacc):
   def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc):
      self.xpos = xpos
      self.ypos = ypos
      self.xvel = xvel
      self.yvel = yvel
      self.xacc = xacc
      self.yacc = yacc

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Subatomic Simulator!")

running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
    
   pygame.display.flip()
pygame.quit()
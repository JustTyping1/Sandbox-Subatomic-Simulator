import pygame

# Class for Proton subatomic particle
class Proton(xpos, ypos, xvel, yvel, xacc, yacc):
   def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc):
      # Adding variables for the proton's velocity, acceleration, position, charge and mass
      self.xpos = xpos
      self.ypos = ypos
      self.xvel = xvel
      self.yvel = yvel
      self.xacc = xacc
      self.yacc = yacc
      self.charge = 0.00000000000000000016
      self.mass = 0.00000000000000000000000000167262192

# Class for Electron subatomic particle
class Electron(xpos, ypos, xvel, yvel, xacc, yacc):
   def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc):
      # Adding variables for the proton's velocity, acceleration, position, charge and mass
      self.xpos = xpos
      self.ypos = ypos
      self.xvel = xvel
      self.yvel = yvel
      self.xacc = xacc
      self.yacc = yacc
      self.charge = -0.00000000000000000016
      self.mass = 0.00000000000000000000000000000091093837

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
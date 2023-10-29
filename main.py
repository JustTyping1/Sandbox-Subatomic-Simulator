import pygame

# Class for Proton subatomic particle
class Proton():
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
   def render(self):
      imp = pygame.image.load("protonsprite.png").convert()
      window.blit(imp, (self.xpos, self.ypos))

# Class for Electron subatomic particle
class Electron():
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
   def render(self):
      imp = pygame.image.load("electronsprite.png").convert()
      window.blit(imp, (self.xpos, self.ypos))

# Class for Neutron subatomic particle
# mass of neutron is 1.674927471×10−27 kg or 1.674927471 "rontograms"
class Neturon():
   def __init__(self, xpos, ypos, xvel, yvel, xacc, yacc):
      # Adding variables for the proton's velocity, acceleration, position, charge and mass
      self.xpos = xpos
      self.ypos = ypos
      self.xvel = xvel
      self.yvel = yvel
      self.xacc = xacc
      self.yacc = yacc
      self.charge = 0 
      self.mass = 0.00000000000000000000000000000091093837 + 0.0000000000000000000000000167262192
   def render(self):
      imp = pygame.image.load("neutronsprite.png").convert()
      window.blit(imp, (self.xpos, self.ypos))

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Subatomic Simulator!")

running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
   
   # Rendering differnet particles at coords (test)
   proton1 = Proton(50, 50, 0, 0, 0, 0)
   proton1.render()
   electron1 = Electron(200, 300, 0, 0, 0, 0)
   electron1.render()
   neutron1 = Neturon(600, 400, 0, 0, 0, 0)
   neutron1.render()
   

    
   pygame.display.flip()

pygame.quit()

import pygame
from typing import *

eCharge = NewType("eCharge", float) # 1.602176634 10^{-19} C # Elementary charge
MeVPerCSquare = NewType("MeVPerCSquare", float) # MeV/c^2 # Common unit used in particle physics

class Vector2D():
   def __init__(self, x: float, y: float) -> None:
      self.x: float = x
      self.y: float = y

class Motion2D():
   def __init__(self, pos: Vector2D, vel: Vector2D = Vector2D(0, 0), acc: Vector2D = Vector2D(0, 0)):
      self.xpos: float = pos.x
      self.ypos: float = pos.y
      self.xvel: float = vel.x
      self.yvel: float = vel.y
      self.xacc: float = acc.x
      self.yacc: float = acc.y

# Class for Proton subatomic particle
class Proton():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion

      self.charge: eCharge = eCharge(1)
      self.mass: MeVPerCSquare = MeVPerCSquare(938.28)

   def render(self):
      imp = pygame.image.load("protonsprite.png").convert()
      window.blit(imp, (self.state.xpos, self.state.ypos))

# Class for Electron subatomic particle
class Electron():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion

      self.charge: eCharge = eCharge(-1)
      self.mass: MeVPerCSquare = MeVPerCSquare(0.511)

   def render(self):
      imp = pygame.image.load("electronsprite.png").convert()
      window.blit(imp, (self.state.xpos, self.state.ypos))

# Class for Neutron subatomic particle
class Neturon():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion

      self.charge: eCharge = eCharge(0)
      self.mass: MeVPerCSquare = MeVPerCSquare(939.57)

   def render(self):
      imp = pygame.image.load("neutronsprite.png").convert()
      window.blit(imp, (self.state.xpos, self.state.ypos))

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
   proton1 = Proton(Motion2D(Vector2D(50, 50)))
   proton1.render()

   electron1 = Electron(Motion2D(Vector2D(200, 300)))
   electron1.render()

   neutron1 = Neturon(Motion2D(Vector2D(600, 400)))
   neutron1.render()

   pygame.display.flip()

pygame.quit()
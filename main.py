import pygame
from typing import *
import math
import time

eCharge = NewType("eCharge", float) # 1.602176634 10^{-19} C # Elementary charge
MeVPerCSquare = NewType("MeVPerCSquare", float) # MeV/c^2 # Common unit used in particle physics

class Vector2D():
   def __init__(self, x: float, y: float) -> None:
      self.x: float = x
      self.y: float = y

   def magnitude(self) -> float:
      return math.sqrt(self * self)

   def normalise(self) -> "Vector2D":
      mag: float = self.magnitude()
      return Vector2D(self.x/mag, self.y/mag)

   # Scale vector or perform dot product
   def __mul__(self, c: Union[float, "Vector2D"]) -> Union["Vector2D", float]:
      if isinstance(c, (float, int)): return Vector2D(c * self.x, c * self.y) # Scaling
      if isinstance(c, Vector2D): return self.x * c.x + self.y * c.y          # Dot product (no cross product for 2D vectors so no ambiguity)
      raise TypeError(f"Cannot multiply types Vector2D and {type(c).__name__}!")

   __rmul__ = __mul__

   def __add__(self, v: "Vector2D") -> "Vector2D":
      if not isinstance(v, Vector2D): raise TypeError(f"Cannot add types Vector2D and {type(v).__name__}!")
      return Vector2D(self.x + v.x, self.y + v.y)

   def __sub__(self, v: "Vector2D") -> "Vector2D":
      return self + (-1 * v)

   # For converting to tuple
   def __iter__(self) -> Generator[float, None, None]:
      yield self.x
      yield self.y

   def __repr__(self) -> str: return f'[{self.x}, {self.y}]'
   def __str__(self) -> str: return self.__repr__()

class Motion2D():
   def __init__(self, pos: Vector2D, vel: Vector2D = Vector2D(0, 0), acc: Vector2D = Vector2D(0, 0)):
      self.pos: Vector2D = pos
      self.vel: Vector2D = vel
      self.acc: Vector2D = acc

   def step(self, delta: float) -> None:
      self.pos += delta * self.vel + 0.5 * (delta ** 2) * self.acc # s = ut + 0.5at^2
      self.vel += delta * self.acc # v = u + at

# Class for Proton subatomic particle
class Proton():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion
      self.charge: eCharge = eCharge(1)
      self.mass: MeVPerCSquare = MeVPerCSquare(938.28)

   def render(self, delta: float):
      self.state.step(delta)
      imp = pygame.image.load("protonsprite.png").convert()
      window.blit(imp, tuple(self.state.pos))

# Class for Electron subatomic particle
class Electron():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion
      self.charge: eCharge = eCharge(-1)
      self.mass: MeVPerCSquare = MeVPerCSquare(0.511)

   def render(self, delta: float):
      self.state.step(delta)
      imp = pygame.image.load("electronsprite.png").convert()
      window.blit(imp, tuple(self.state.pos))

# Class for Neutron subatomic particle
# mass of neutron is 1.674927471×10−27 kg or 1.674927471 "rontograms"
class Neturon():
   def __init__(self, initMotion: Motion2D):
      self.state: Motion2D = initMotion
      self.charge: eCharge = eCharge(0)
      self.mass: MeVPerCSquare = MeVPerCSquare(939.57)

   def render(self, delta: float):
      self.state.step(delta)
      imp = pygame.image.load("neutronsprite.png").convert()
      window.blit(imp, tuple(self.state.pos))

# Vector testing
# v1 = Vector2D(3, 4)
# v2 = Vector2D(-2, 3)
# print(v1 * v2)
# print(v1.magnitude())
# print(v1.normalise())
# print(v1 - v2)

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Subatomic Simulator!")

proton1 = Proton(Motion2D(Vector2D(50, 50), acc=Vector2D(0, 20))) # Some downwards acceleration
electron1 = Electron(Motion2D(Vector2D(200, 300)))
neutron1 = Neturon(Motion2D(Vector2D(600, 400)))

currtime = time.time()
running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT:
         running = False
   
   # How much time has passed
   (lasttime, currtime) = (currtime, time.time())
   delta: float = currtime - lasttime

   # Clear screen
   window.fill(pygame.Color(0, 0, 0))

   proton1.render(delta)
   electron1.render(delta)
   neutron1.render(delta)

   pygame.display.flip()

pygame.quit()
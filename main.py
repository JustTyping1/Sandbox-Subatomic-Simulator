from abc import ABC, abstractmethod
from typing import *
import pygame
import math
import time

eCharge = NewType("eCharge", float) # 1.602176634 10^{-19} C # Elementary charge
MeVPerCSquare = NewType("MeVPerCSquare", float) # MeV/c^2 # Common unit used in particle physics
Numeric: TypeAlias = Union[float, int]

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
   def __mul__(self, c: Union[Numeric, "Vector2D"]) -> Union["Vector2D", float]:
      if isinstance(c, (float, int)): return Vector2D(c * self.x, c * self.y) # Scaling
      if isinstance(c, Vector2D): return self.x * c.x + self.y * c.y          # Dot product (no cross product for 2D vectors so no ambiguity)
      raise TypeError(f"Cannot multiply types Vector2D and {type(c).__name__}!")

   def __truediv__(self, c: Numeric) -> "Vector2D":
      if isinstance(c, (float, int)): return self * (1/c)
      raise TypeError(f"Cannot divide types Vector2D and {type(c).__name__}!")

   __rmul__ = __mul__
   __rtruediv__ = __truediv__

   def __add__(self, v: "Vector2D") -> "Vector2D":
      if not isinstance(v, Vector2D): raise TypeError(f"Cannot add types Vector2D and {type(v).__name__}!")
      return Vector2D(self.x + v.x, self.y + v.y)

   def __sub__(self, v: "Vector2D") -> "Vector2D":
      return self + (-1 * v)

   def __eq__(self, v: "Vector2D") -> bool:
      if not isinstance(v, Vector2D): raise TypeError(f"Cannot compare types Vector2D and {type(v).__name__}!")
      return (self.x == v.x) and (self.y == v.y)

   # For converting to tuple
   def __iter__(self) -> Generator[float, None, None]:
      yield self.x
      yield self.y

   def __repr__(self) -> str: return f'[{self.x}, {self.y}]'
   def __str__(self) -> str: return self.__repr__()

ZEROVECTOR: Vector2D = Vector2D(0, 0)

class Motion2D():
   def __init__(self, pos: Vector2D, vel: Vector2D = Vector2D(0, 0)):
      self.pos: Vector2D = pos
      self.vel: Vector2D = vel

   def step(self, delta: float, acc: Vector2D) -> None:
      self.pos += delta * self.vel + 0.5 * (delta ** 2) * acc # s = ut + 0.5at^2
      self.vel += delta * acc # v = u + at

# Class for general particle
class Particle(ABC):
   state: Motion2D
   charge: eCharge
   mass: MeVPerCSquare
   sprite: pygame.surface.Surface

   def __init__(self, initMotion: Motion2D, spritePath: str):
      self.state = initMotion
      self.sprite = pygame.image.load(spritePath).convert()

   def step(self, delta: float, acc: Vector2D) -> None:
      self.state.step(delta, acc)

   def render(self) -> None:
      window.blit(self.sprite, tuple(self.state.pos))

# Class for Proton subatomic particle
class Proton(Particle):
   def __init__(self, initMotion: Motion2D):
      super().__init__(initMotion, "protonsprite.png")
      self.charge: eCharge = eCharge(10000)
      self.mass: MeVPerCSquare = MeVPerCSquare(938.28)

# Class for Electron subatomic particle
class Electron(Particle):
   def __init__(self, initMotion: Motion2D):
      super().__init__(initMotion, "electronsprite.png")
      self.charge: eCharge = eCharge(-10000)
      self.mass: MeVPerCSquare = MeVPerCSquare(0.511)

# Class for Neutron subatomic particle
# mass of neutron is 1.674927471×10−27 kg or 1.674927471 "rontograms"
class Neturon(Particle):
   def __init__(self, initMotion: Motion2D):
      super().__init__(initMotion, "neutronsprite.png")
      self.charge: eCharge = eCharge(0)
      self.mass: MeVPerCSquare = MeVPerCSquare(939.57)

# Vector testing
# v1 = Vector2D(3, 4)
# v2 = Vector2D(-2, 3)
# print(v1 * v2)
# print(v1.magnitude())
# print(v1.normalise())
# print(v1 - v2)

class Space:
   space: List[Particle]
   permittivity: float

   def __init__(self, *particles):
      self.space = list(particles)
      self.permittivity = 1

   def ElectricField(self, r: Vector2D) -> Vector2D:
      totalContribution: Vector2D = ZEROVECTOR

      for particle in self.space:
         R = r - particle.state.pos
         if R.magnitude() < 2: continue # Disregard charge at same (approximate) position

         totalContribution += (particle.charge/(R * R)) * R.normalise() # Magnitude times direction

      return totalContribution / (4*math.pi*self.permittivity)

   def step(self, delta: float) -> None:
      accels: List[Vector2D] = list()

      for particle in self.space:
         constantAccel: Vector2D = Vector2D(0, 0) # Gravity

         electricForce: Vector2D = particle.charge * self.ElectricField(particle.state.pos)
         electricAccel: Vector2D = electricForce / particle.mass

         accels.append(constantAccel + electricAccel)

      [particle.step(delta, accels[i]) for i, particle in enumerate(self.space)]

   def render(self) -> None:
      for particle in self.space: particle.render()

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Subatomic Simulator!")

proton1 = Proton(Motion2D(Vector2D(400, 300)))
electron1 = Electron(Motion2D(Vector2D(300, 300), Vector2D(0, -420)))
# neutron1 = Neturon(Motion2D(Vector2D(600, 400)))

space: Space = Space(proton1, electron1)

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

   space.step(delta)
   space.render()
   
   print(space.space[0].state.vel)
   print(space.space[1].state.vel)

   pygame.display.flip()

pygame.quit()

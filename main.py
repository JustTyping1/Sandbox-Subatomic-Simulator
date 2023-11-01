from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import *
import pygame
import math
import time

"""
Units:
- Length : Picometre                (1m = 1.0000e15pm)
- Time   : Picosecond               (1s = 1.0000e15ps)
- Mass   : MeV/c2                   (1kg = 5.6164e29MeV/c2)
- Charge : Microelementary charge   (1C = 6.2414e24μe)

Constants:
- ε₀ = 8.8542e-12 F * m-1 = 6.1412e-4 pm-4 * ps2 * (MeV/c2)-1 * μe2
"""

picoMetre = NewType("picoMetre", float)
picoSecond = NewType("picoSecond", float)
MeVPerCSquare = NewType("MeVPerCSquare", float) # MeV/c^2
μeCharge = NewType("μeCharge", float) # Microelementary charge
Numeric: TypeAlias = Union[float, int]

class Vector2D():
   def __init__(self, x: float, y: float) -> None:
      self.x: float = x
      self.y: float = y

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

   def magnitude(self) -> float:
      return math.sqrt(self * self)

   def normalise(self) -> "Vector2D":
      mag: float = self.magnitude()
      return Vector2D(self.x/mag, self.y/mag)

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

# Class for general particle
class Particle(ABC):
   position: Vector2D
   velocity: Vector2D
   
   charge: μeCharge
   mass: MeVPerCSquare

   sprite: pygame.surface.Surface

   def __init__(self, spritePath: str, position: Vector2D, velocity: Vector2D = ZEROVECTOR):
      self.position = position
      self.velocity = velocity

      self.sprite = pygame.image.load(f"Sprites/{spritePath}").convert()

   def render(self) -> None:
      size: Tuple[int, int] = self.sprite.get_size()
      window.blit(self.sprite, (self.position.x - size[0]/2, self.position.y - size[1]/2)) # Centre sprites to avoid visual issues

# Class for Proton subatomic particle
class Proton(Particle):
   def __init__(self, position: Vector2D, velocity: Vector2D = ZEROVECTOR):
      super().__init__("Proton.png", position, velocity)
      self.charge: μeCharge = μeCharge(1000000)
      self.mass: MeVPerCSquare = MeVPerCSquare(938.28)

# Class for Electron subatomic particle
class Electron(Particle):
   def __init__(self, position: Vector2D, velocity: Vector2D = ZEROVECTOR):
      super().__init__("Electron.png", position, velocity)
      self.charge: μeCharge = μeCharge(-1000000)
      self.mass: MeVPerCSquare = MeVPerCSquare(0.511)

# Class for Neutron subatomic particle
# mass of neutron is 1.674927471×10−27 kg or 1.674927471 "rontograms"
class Neturon(Particle):
   def __init__(self, position: Vector2D, velocity: Vector2D = ZEROVECTOR):
      super().__init__("Neutron.png", position, velocity)
      self.charge: μeCharge = μeCharge(0)
      self.mass: MeVPerCSquare = MeVPerCSquare(939.57)

# Vector testing
# v1 = Vector2D(3, 4)
# v2 = Vector2D(-2, 3)
# print(v1 * v2)
# print(v1.magnitude())
# print(v1.normalise())
# print(v1 - v2)

@dataclass
class Interactor:
   position: Vector2D
   charge: μeCharge

class Frame:
   space: List[Particle]

   def __init__(self, *particles) -> None:
      self.space = particles

   def dumpParticles(self) -> Generator[Particle, None, None]:
      for particle in self.space: yield particle

   def influences(self) -> List[Interactor]:
      return [
         Interactor(
            particle.position,
            particle.charge
         )
         for particle in self.space
      ]

   def render(self) -> None:
      [particle.render() for particle in self.space]

class Mechanic:
   permittivity: float
   constantAccel: Vector2D

   def __init__(self, permittivity: float, constantAccel: Vector2D = ZEROVECTOR) -> None:
      self.permittivity = permittivity
      self.constantAccel = constantAccel

   def ElectricField(self, influences: List[Interactor], r: Vector2D) -> Vector2D:
      totalContribution: Vector2D = ZEROVECTOR

      for interactor in influences:
         R = r - interactor.position
         if R.magnitude() == 0:
            continue # Disregard charge at same (approximate) position

         totalContribution += (interactor.charge/(R * R)) * R.normalise() # Magnitude times direction

      return totalContribution / (4*math.pi*self.permittivity)
   
   def step(self, frame: Frame, delta: float) -> Frame:
      influence: List[Interactor] = frame.influences()

      newParticles: List[Particle] = list()
      for particle in frame.dumpParticles():
         accel = self.constantAccel
         accel += (particle.charge / particle.mass) * self.ElectricField(influence, particle.position)

         particle.position += delta * particle.velocity + 0.5 * (delta ** 2) * accel
         particle.velocity += delta * accel

         newParticles.append(particle)

      return Frame(*newParticles)

pygame.init()
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Subatomic Simulator!")

proton = Proton(Vector2D(400, 300))
electron1 = Electron(Vector2D(300, 300), Vector2D(0, -1592000))
#electron2 = Electron(Vector2D(500, 300), Vector2D(0, 1592000))
# neutron1 = Neturon(Motion2D(Vector2D(600, 400)))

mechanic: Mechanic = Mechanic(0.00061412, Vector2D(0, 0))
frame: Frame = Frame(proton, electron1)
currtime = time.time()

running = True
while running:
   for event in pygame.event.get():
      if event.type == pygame.QUIT: running = False
   
   window.fill(pygame.Color(0, 0, 0))

   # How much time has passed
   (lasttime, currtime) = (currtime, time.time())
   delta: picoSecond = currtime - lasttime   # 1s -> 1ps
   delta /= 1000                             # 1ps -> 1fs

   # Additional slowing
   delta /= 10                               # 1fs -> 0.1fs (1s -> 0.1fs)

   frame: Frame = mechanic.step(frame, delta)
   frame.render()

   pygame.display.flip()

pygame.quit()

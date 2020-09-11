from color import *

'''
  Diana Ximena de León Figueroa
  Carne 18607
  RT2 - Phong model
  Graficas por Computadora
  10 de septiembre de 2020
'''


class Material(object):
  def __init__(self, diffuse, albedo, spec):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec


WHITE = Color(215, 200, 200)
BONE = Color(240, 225, 205)
ORANGE = Color(240, 60, 40)
BLACK = Color(10, 10, 10)
LIGHTBLUE = Color(100, 130, 200)

body = Material(diffuse = BONE, albedo = (0.6, 0.3, 0.1), spec = 10)
button = Material(diffuse = BLACK, albedo = (0.6, 0.3, 0.1), spec = 5)
eye = Material(diffuse = WHITE, albedo = (0.6, 0.3, 0.1), spec = 15)
nose = Material(diffuse = ORANGE, albedo = (0.6, 0.3, 0.1), spec = 30)
lightblue = Material(diffuse = LIGHTBLUE, albedo = (0.6, 0.3, 0.1), spec = 20)

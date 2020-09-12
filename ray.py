from utils import writebmp, norm, V3, sub, dot, reflect, length, mul, sum
from sphere import Sphere
from math import pi, tan
from materials import eye, oso1, oso2, tono2, adorno1, adorno2, mona1, mona2, tono3
import random
from light import *
from color import *

'''
    Diana Ximena de León Figueroa
    Carne 18607
    RT2 - Phong model
    Graficas por Computadora
    10 de septiembre de 2020
'''

BLACK = Color(0, 0, 0)
WHITE = Color(255, 255, 255)
BACKGROUND = Color(240, 240, 240)


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.currentColor = BACKGROUND
        self.clear()

    def clear(self):
        self.pixels = [
            [self.currentColor for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename='out.bmp'):
        writebmp(filename, self.width, self.height, self.pixels)

    def point(self, x, y, selectColor=None):
        try:
            self.pixels[y][x] = selectColor or self.currentColor
        except:
            pass

    def sceneIntersect(self, origin, direction):
        zbuffer = float('inf')
        
        material = None
        intersect = None
        
        for obj in self.scene:
            hit = obj.rayIntersect(origin, direction)
            if hit is not None:
                if hit.distance < zbuffer:
                    zbuffer = hit.distance
                    material = obj.material
                    intersect = hit
        return material, intersect

    def castRay(self, origin, direction):
        material, intersect = self.sceneIntersect(origin, direction)
        
        if material is None:
            return self.currentColor

        lightDir = norm(sub(self.light.position, intersect.point))
        lightDistance = length(sub(self.light.position, intersect.point))
        
        offsetNormal = mul(intersect.normal, 1.1)
        shadowOrigin = sub(intersect.point, offsetNormal) if dot(lightDir, intersect.normal) < 0 else sum(intersect.point, offsetNormal)
        shadowMaterial, shadowIntersect = self.sceneIntersect(shadowOrigin, lightDir)
        shadowIntensity = 0

        if shadowMaterial and length(sub(shadowIntersect.point, shadowOrigin)) < lightDistance:
            shadowIntensity = 0.9

        intensity = self.light.intensity * max(0, dot(lightDir, intersect.normal)) * (1 - shadowIntensity)

        reflection = reflect(lightDir, intersect.normal)
        specularIntensity = self.light.intensity * (
            max(0, -dot(reflection, direction)) ** material.spec
        )

        diffuse = material.diffuse * intensity * material.albedo[0]
        specular = Color(255, 255, 255) * specularIntensity * material.albedo[1]
        return diffuse + specular


    def render(self):
        fov = int(pi / 2) # field of view
        for y in range(self.height):
            for x in range(self.width):
                i = (2 * (x + 0.5) / self.width - 1) * self.width / self.height * tan(fov / 2)
                j = (2 * (y + 0.5) / self.height - 1) * tan(fov / 2)
                direction = norm(V3(i, j, -1))
                self.pixels[y][x] = self.castRay(V3(0, 0, 0), direction)

    def gradientBackground(self):
        for x in range(self.width):
            for y in range(self.height):
                r = int((x / self.width) * 255) if x / self.width < 1 else 1
                g = int((y / self.height) * 255) if y / self.height < 1 else 1
                b = 0
                self.pixels[y][x] = Color(r, g, b)
    


r = Raytracer(1000, 1000)
r.light = Light(
    position = V3(0, 0, 20),
    intensity = 1.5
)
r.scene = [
    Sphere(V3(2.5, -1, -10), 1.75, adorno2),
    Sphere(V3(-2.5, -1, -10), 1.75, adorno1),
    Sphere(V3(2.5, 2, -10), 1.5, oso2),
    Sphere(V3(-2.5, 2, -10), 1.5, oso1),
    Sphere(V3(2.5, 1.7, -9), 0.65, tono2),
    Sphere(V3(-2.5, 1.7, -9), 0.65, oso1),
    Sphere(V3(4, 0, -10), 0.6, oso2),
    Sphere(V3(-4, 0, -10), 0.6, oso1),
    Sphere(V3(1, 0, -10), 0.6, oso2),
    Sphere(V3(-1, 0, -10), 0.6, oso1),
    Sphere(V3(4, -2.5, -10), 0.75, oso2),
    Sphere(V3(-4, -2.5, -10), 0.75, oso1),
    Sphere(V3(1, -2.5, -10), 0.75, oso2),
    Sphere(V3(-1, -2.5, -10), 0.75, oso1),
    Sphere(V3(3.4, 2.9, -9), 0.4, tono3),
    Sphere(V3(-3.4, 2.9, -9), 0.4, oso1),
    Sphere(V3(1.4, 2.9, -9), 0.4, tono3),
    Sphere(V3(-1.4, 2.9, -9), 0.4, oso1),
    Sphere(V3(2.4, 0.2, -8.6), 0.2, mona2),
    Sphere(V3(2.1, 0.2, -8.6), 0.2, mona2),
    Sphere(V3(-2.4, 0.2, -8.6), 0.2, mona1),
    Sphere(V3(-2.1, 0.2, -8.6), 0.2, mona1),
    Sphere(V3(-2.5, 1.7, -8), 0.1, eye),
    Sphere(V3(2.5, 1.7, -8), 0.1, eye),
    Sphere(V3(-2.6, 2.1, -8), 0.1, eye),
    Sphere(V3(-2.2, 2.1, -8), 0.1, eye),
    Sphere(V3(2.6, 2.1, -8), 0.1, eye),
    Sphere(V3(2.2, 2.1, -8), 0.1, eye),
]
r.render()

r.write()

from utils import writebmp, norm, V3, sub, dot, reflect, length, mul, sum
from sphere import Sphere
from math import pi, tan
from materials import lightblue, body, eye, nose, button
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
BLUE = Color(60, 80, 125)


class Raytracer(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.currentColor = BLUE
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
    position = V3(-20, 20, 20),
    intensity = 1.5
)
r.scene = [
    Sphere(V3(0.7, -5.05, -15), 0.15, button),
    Sphere(V3(-0.8, -5.05, -15), 0.15, button),
    Sphere(V3(0.75, -5, -15), 0.3, eye),
    Sphere(V3(-0.75, -5, -15), 0.3, eye),
    Sphere(V3(0, -4.5, -15), 0.4, nose),
    Sphere(V3(-1, -4, -15), 0.2, button),
    Sphere(V3(-0.4, -3.5, -15), 0.2, button),
    Sphere(V3(0.4, -3.5, -15), 0.2, button),
    Sphere(V3(1, -4, -15), 0.2, button),
    Sphere(V3(0, -2, -15), 0.25, button),
    Sphere(V3(0, 0.25, -15), 0.5, button),
    Sphere(V3(0, 3, -15), 0.75, button),
    Sphere(V3(0, -3.5, -12), 1.5, body),
    Sphere(V3(0, -1, -12), 2, body),
    Sphere(V3(0, 2.5, -12), 2.5, body),
    Sphere(V3(0, 0, -11), 5, lightblue),
]
r.render()
r.write()

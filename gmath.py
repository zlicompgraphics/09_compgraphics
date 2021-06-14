import math
from display import *

# IMPORTANT NOTE

# Ambient light is represented by a color value

# Point light sources are 2D arrays of doubles.
#      - The first index (LOCATION) represents the vector to the light.
#      - The second index (COLOR) represents the color.

# Reflection constants (ka, kd, ks) are represented as arrays of
# doubles (red, green, blue)

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4


# lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect):
    color = [0, 0, 0]
    ambient_color = calculate_ambient(ambient, areflect)
    diffuse_color = calculate_diffuse(light, dreflect, normal)
    specular_color = calculate_specular(light, sreflect, view, normal)
    color[0] = ambient_color[0] + diffuse_color[0] + specular_color[0]
    color[1] = ambient_color[1] + diffuse_color[1] + specular_color[1]
    color[2] = ambient_color[2] + diffuse_color[2] + specular_color[2]
    limit_color(color)
    return color


def calculate_ambient(ambient, areflect):
    ambient_color = [ambient[0] * areflect[0], ambient[1] * areflect[1], ambient[2] * areflect[2]]
    limit_color(ambient_color)
    return ambient_color


def calculate_diffuse(light, dreflect, normal):
    diffuse_color = [0, 0, 0]
    light_vector = [light[0][0], light[0][1], light[0][2]]
    light_color = [light[1][0], light[1][1], light[1][2]]
    normalize(light_vector)
    normalize(normal)
    diffuse_color[0] = light_color[0] * dreflect[0] * (dot_product(light_vector, normal))
    diffuse_color[1] = light_color[1] * dreflect[1] * (dot_product(light_vector, normal))
    diffuse_color[2] = light_color[2] * dreflect[2] * (dot_product(light_vector, normal))
    limit_color(diffuse_color)
    return diffuse_color


def calculate_specular(light, sreflect, view, normal):
    specular_color = [0, 0, 0]
    light_vector = [light[0][0], light[0][1], light[0][2]]
    light_color = [light[1][0], light[1][1], light[1][2]]
    normalize(normal)
    normalize(light_vector)
    normalize(view)
    reflected_light = [0, 0, 0]
    reflected_light[0] = 2 * normal[0] * (dot_product(normal, light_vector)) - light_vector[0]
    reflected_light[1] = 2 * normal[1] * (dot_product(normal, light_vector)) - light_vector[1]
    reflected_light[2] = 2 * normal[2] * (dot_product(normal, light_vector)) - light_vector[2]
    specular_color[0] = light_color[0] * sreflect[0] * (dot_product(reflected_light, view) ** 2)
    specular_color[1] = light_color[1] * sreflect[1] * (dot_product(reflected_light, view) ** 2)
    specular_color[2] = light_color[2] * sreflect[2] * (dot_product(reflected_light, view) ** 2)
    limit_color(specular_color)
    return specular_color


def limit_color(color):
    for i in color:
        if i < 0:
            i = 0
        if i > 255:
            i = 255
    color[0] = int(color[0])
    color[1] = int(color[1])
    color[2] = int(color[2])


# vector functions
# normalize vector, should modify the parameter
def normalize(vector):
    magnitude = math.sqrt(vector[0] * vector[0] +
                          vector[1] * vector[1] +
                          vector[2] * vector[2])
    for i in range(3):
        vector[i] = vector[i] / magnitude


# Return the dot porduct of a . b
def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


# Calculate the surface normal for the triangle whose first
# point is located at index i in polygons
def calculate_normal(polygons, i):
    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i + 1][0] - polygons[i][0]
    A[1] = polygons[i + 1][1] - polygons[i][1]
    A[2] = polygons[i + 1][2] - polygons[i][2]

    B[0] = polygons[i + 2][0] - polygons[i][0]
    B[1] = polygons[i + 2][1] - polygons[i][1]
    B[2] = polygons[i + 2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N

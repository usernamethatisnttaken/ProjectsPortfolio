import math

def div(x, y):
    if not y:
        return 0
    return x / y

def sign(n):
    return div(n, abs(n))

def rel_theta(a, b, phi):
        theta = math.acos((b[0] - a[0]) / math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2))
        if sign(math.asin((b[1] - a[1]) / math.sqrt((b[1] - a[1])**2 + (b[0] - a[0])**2))) < 0:
            theta = math.radians(360) - theta
        theta = (theta - phi + math.radians(360)) % math.radians(360)
        return theta

a = [400, 400]
b = [450, 350]
phi = 90

theta = rel_theta(a, b, math.radians(phi))
print(round(math.degrees(theta), 2))
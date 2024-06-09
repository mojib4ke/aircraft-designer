import math

def solve_quadratic(a, b, c, name=''):
    discriminant = b**2 - 4*a*c

    if discriminant < 0:
        raise ValueError(f"There's no real solution for {name} equation")

    sqrt_discriminant = math.sqrt(discriminant)
    x1 = (-b + sqrt_discriminant) / (2*a)
    x2 = (-b - sqrt_discriminant) / (2*a)

    if x1 > 0 and x2 > 0:
        raise ValueError(f"There's to solution to {name} equation")
    elif x1 > 0:
        return x1
    elif x2 > 0:
        return x2 
    else:
        raise ValueError(f"There's no real solution for {name} equation")

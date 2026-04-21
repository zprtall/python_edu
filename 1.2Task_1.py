class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __bool__(self,):
        return self.x < 0 or self.y < 0

    def __str__(self,):
        return f"Точка имеет значеня -\nX: {self.x} \nY: {self.y}"

    def __sub__(self, other):
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

point1 = Point(10, -5)
point2 = Point(15, 0)
print(point1)
print(point2)

print(point1 - point2)

if point1:
    print("Есть отрицательная координата")
else:
    print("Обе координаты >= 0")

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __bool__(self,):
        return self.x < 0 or self.y < 0

    def __str__(self,):
        return f"{self.x}, {self.y}"

    def __sub__(self, other):
        return ((other.x - self.x) ** 2 + (other.y - self.y) ** 2) ** 0.5

class Figure:
    def area(self):
         pass

    def perimetr(self):
        pass

class Quadrilateral(Figure):
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def sides(self):
        s1 = self.p1 - self.p2
        s2 = self.p2 - self.p3
        s3 = self.p3 - self.p4
        s4 = self.p4 - self.p1
        return s1, s2, s3, s4

    def area(self):
        p = sum(self.sides()) / 2
        s1, s2, s3, s4 = self.sides()
        return ((p - s1) * (p - s2) * (p - s3) * (p - s4)) **0.5

    def perimetr(self):
        return sum(self.sides())


class Triangle:
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        return f" point1 = ({self.p1})\n point2 = ({self.p2})\n point3 = ({self.p3})"

    def sides(self):
        s1 = self.p1 - self.p2
        s2 = self.p2 - self.p3
        s3 = self.p3 - self.p1
        return s1, s2, s3

    @property
    def equilateral(self):      # проверка равносторонний ли
        s1, s2, s3 = self.sides()
        return s1 == s2 == s3

    @property
    def isosceles(self):        # провверка равнобедренный ли
        s1, s2, s3 = self.sides()
        return s1 == s2 != s3 or s2 == s3 != s1 or s3 == s1 != s2

    @property
    def right_angled(self):     # проверка прямоугольный ли
        s1, s2, s3 = self.sides()
        return s1 **2 + s2 **2 == s3 **2 or s2 **2 + s3 **2 == s1 **2 or s3 **2 + s1 **2 == s2 **2

    @property
    def blunt_angled(self):     # проверка тупоугольный ли
        s1, s2, s3 = self.sides()
        return s1 ** 2 + s2 ** 2 < s3 ** 2 or s2 ** 2 + s3 ** 2 < s1 ** 2 or s3 ** 2 + s1 ** 2 < s2 ** 2

    @property
    def sharp_angled(self):     # проверка остроугольный ли
        s1, s2, s3 = self.sides()
        return s1 ** 2 + s2 ** 2 > s3 ** 2 or s2 ** 2 + s3 ** 2 > s1 ** 2 or s3 ** 2 + s1 ** 2 > s2 ** 2

    @property
    def area(self):                # получение площади
        s1, s2, s3 = self.sides()
        p = (s1 + s2 + s3)/2
        return (p * (p - s1) * (p - s2) * (p - s3)) **0.5

triangle1 = Triangle(Point(1,2), Point(3,4), Point(-1, 8))
print(triangle1.sides())

print(triangle1.sharp_angled)
print(triangle1.area)
print(triangle1)

quadrilateral1 = Quadrilateral(Point(1,2), Point(3,4), Point(-1, 8), Point(4, 5))

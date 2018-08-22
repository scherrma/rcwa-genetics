class Vector():
    def __init__(self, vals):
        self.val = vals

    def __str__(self):
        return '<' + ', '.join(map(str, self.val)) + '>'

    def __eq__(self, other):
        if len(self.val) != len(other.val) or any([lhs != rhs for (lhs, rhs) in zip(self.val, other.val)]):
            return False
        return True

    def __neg__(self):
        return Vector([-x for x in self.val])

    def __add__(self, other):
        return Vector([x+y for (x, y) in zip(self.val, other.val)])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, rhs):
        return Vector([rhs*x for x in self.val])

    def __rmul__(self, lhs):
        return self * lhs

    def __truediv__(self, rhs):
        return self * (1/rhs)

    def norm(self):
        return sum([x*x for x in self.val])**(1/2)

    def unit(self):
        return self/self.norm()

    def dot(self, other):
        return sum([x*y for (x, y) in zip(self.val, other.val)])

    def proj(self, other):
        return self.dot(other.unit())*other.unit()

    def rej(self, other):
        return self - self.proj(other)

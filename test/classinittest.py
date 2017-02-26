b = 3


class A(object):

    def __init__(self):
        super().__init__()
        self.a = 1 + b

    def check(self):
        print(self.a)

obj = A()
obj.check()

b = 4

A().check()

print(A().a)

print(obj.a)

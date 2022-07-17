class Frange():
    def __init__(self, *args, start=0, step=1):
        if len(args) == 1:
            self.start = start
            self.stop = args[0]
            self.step = step
        elif len(args) == 2:
            self.start, self.stop = args
            self.step = step
        elif len(args) == 3:
            self.start, self.stop, self.step = args
        else:
            raise TypeError("Max 3 arguments were expected.")

    def __next__(self):
        if self.step > 0:
            if self.start + self.step >= self.stop + self.step:
                raise StopIteration
            result = self.start
            self.start = round((self.start + self.step), 1)
        else:
            if self.start + self.step <= self.stop + self.step:
                raise StopIteration
            result = self.start
            self.start = round((self.start + self.step), 1)
        return result

    def __iter__(self):
        return self


for i in Frange(1, 100, 3.5):
    print(i)

assert(list(Frange(5)) == [0, 1, 2, 3, 4])
assert(list(Frange(2, 5)) == [2, 3, 4])
assert(list(Frange(2, 10, 2)) == [2, 4, 6, 8])
assert(list(Frange(10, 2, -2)) == [10, 8, 6, 4])
assert(list(Frange(2, 5.5, 1.5)) == [2, 3.5, 5])
assert(list(Frange(1, 5)) == [1, 2, 3, 4])
assert(list(Frange(0, 5)) == [0, 1, 2, 3, 4])
assert(list(Frange(0, 0)) == [])
assert(list(Frange(100, 0)) == [])
#
print('SUCCESS!')

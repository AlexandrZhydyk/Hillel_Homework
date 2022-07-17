from colors import bcolors


class colorizer():
    def __init__(self, color='blue'):
        self.attr = bcolors.__dict__
        self.color = self.attr[color]

    def __enter__(self):
        print(self.color)
        return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(bcolors.ENDC)
        return isinstance(exc_val, TypeError)

with colorizer("blue"):
    print('printed in blue color')
print('printed in default color')

with colorizer("red"):
    print('printed in red color')
print('printed in default color')

with colorizer("green"):
    print('printed in green color')
print('printed in default color')

print('\033[93m', end='')
print('aaa')
print('bbb')
print('\033[0m', end='')
print('ccc')
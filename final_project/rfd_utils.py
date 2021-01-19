import numpy as np

class Drop:
    def __init__(self, origin=None):
        self.path = []
        if not (origin is None):
            self.path.append(origin)

    def getCurrentNode(self):
        return self.path[-1]



if __name__ == '__main__':
    d = Drop()
    d.path.append(0)
    d.path.append(7)
    d.path.append(4)

    print(d.getCurrentNode())

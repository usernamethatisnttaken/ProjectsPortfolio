class plane:
    def __init__(self, coords, nodes, color):
        self.a = coords[0]
        self.b = coords[1]
        self.c = coords[2]
        self.d = coords[3]
        self.score = (nodes[self.a][2] + nodes[self.b][2] + nodes[self.c][2] + nodes[self.d][2]) / 4
        self.color = color

    def update(self, nodes):
        self.score = (nodes[self.a][2] + nodes[self.b][2] + nodes[self.c][2] + nodes[self.d][2]) / 4

    def __repr__(self):
        return str(self.score)
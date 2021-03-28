import numpy as np
import random


class Vertex:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __add__(self, other) -> object:
        return Vertex(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f'(X={self.x}; Y={self.y})'

    def __str__(self):
        return f'(X={self.x}; Y={self.y})'

    def __hash__(self):
        return hash((self.x, self.y))

    def __left_border__(self):
        return self.x == 0

    def __top_border__(self):
        return self.y == 0

    def __right_border__(self, n):
        return self.x == n - 1

    def __bottom_border__(self, n):
        return self.y == n - 1

    def get_children(self, n):
        actions = move_actions.copy()
        if self.__left_border__():
            del actions["Left"]
        if self.__top_border__():
            del actions["Up"]
        if self.__right_border__(n):
            del actions["Right"]
        if self.__bottom_border__(n):
            del actions["Down"]
        return [val + self for val in actions.values()]

    def distance(self, vert):
        return abs(self.x - vert.x) + abs(self.y - vert.y)


move_actions = {
    "Up": Vertex(0, -1),
    "Down": Vertex(0, 1),
    "Left": Vertex(-1, 0),
    "Right": Vertex(1, 0)
}


class World:

    def __init__(self, world_size, initial_pos):
        self.world_size = world_size
        self.current_pos = initial_pos
        self.visited = {self.current_pos}
        self.cost = dict()
        for x, y in np.ndindex(world_size, world_size):
            vert = Vertex(x, y)
            for vert_child in vert.get_children(world_size):
                if (vert, vert_child) not in self.cost and (vert_child, vert) not in self.cost:
                    self.cost[vert, vert_child] = random.randint(1, 10)
        self.trash = []

    def __eq__(self, other):
        return self.world_size == other.world_size and self.current_pos == other.current_pos \
               and self.trash == other.trash and self.visited == other.visited

    def __str__(self):
        trash_state = f'Trash in: {self.trash} '
        visited_state = f'Visited: {self.visited}'
        return f'World state: current pos {self.current_pos}) ' + trash_state + visited_state

    def __hash__(self):
        trash_hash = 0
        for vert in self.trash:
            trash_hash = trash_hash + hash(vert)
        for vert in self.visited:
            trash_hash = trash_hash + hash(vert)
        return hash((trash_hash, self.current_pos))

    def create_trash(self, trash_size_known=True):
        if trash_size_known:
            self.trash = [Vertex(0, 0), Vertex(1, 0), Vertex(2, 0)]
        else:
            probability = 0.2
            self.trash = [Vertex(x, y) for x, y in np.ndindex(self.world_size, self.world_size)
                          if random.random() < probability]

    def child_vertexes(self):
        return self.current_pos.get_children(self.world_size)

    def move(self, vertex):
        self.current_pos = vertex
        self.visited.add(vertex)

    def has_trash(self):
        return self.current_pos in self.trash

    def clean(self):
        if self.has_trash():
            self.trash.remove(self.current_pos)

    def is_clean(self):
        return len(self.trash) == 0

    def all_visited(self):
        return len(self.visited) == pow(self.world_size, 2)

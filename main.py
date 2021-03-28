from world import *
from search import *


def main():
    world_size = 10
    initial_pos = Vertex(4, 2)
    world = World(world_size, initial_pos)
    search = Search(world, False)
    search.dfs()
    search.random()
    world = World(3, Vertex(1, 1))
    search_known = Search(world)
    search_known.bfs()


if __name__ == "__main__":
    main()

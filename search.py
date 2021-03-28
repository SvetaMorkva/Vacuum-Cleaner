import copy
import random


class Search:
    visited_fee = 5
    move_fee = 1

    def __init__(self, world, trash_size_known=True):
        world.create_trash(trash_size_known)
        self.world = world
        self.trash_size_known = trash_size_known

    def dfs_util(self, current, world):
        print("\n------DFS------\n")
        stack = [current]
        path = []
        cost = 0
        while not self.solution_found(world):
            current = stack.pop()
            cost = self.calculate_cost(world, cost, current)
            path.append(copy.deepcopy(world))
            for vert in world.child_vertexes():
                if vert not in world.visited:
                    stack.append(vert)
        for world_state in path:
            print(world_state)
        print(f'Cost {cost}')
        print(f'Number of iterations {len(path)}')

    def dfs(self):
        self.dfs_util(self.world.current_pos, copy.deepcopy(self.world))

    def find_path(self, end_state, parents_state):
        if end_state in parents_state:
            state = parents_state[end_state]
            self.find_path(state, parents_state)
        print(end_state)

    def random(self):
        print("\n------Random------\n")
        cur_world = self.world
        print(cur_world)
        cost = 0
        iterations = 0

        while not self.solution_found(cur_world):
            vert = random.choice(cur_world.child_vertexes())
            cost = self.calculate_cost(cur_world, cost, vert)
            iterations = iterations + 1
            print(cur_world)
        print(f'Cost {cost}')
        print(f'Number of iterations {iterations}')

    def bfs(self):
        print("\n------BFS------\n")
        queue = []
        parents = dict()
        cur_world = self.world
        print(cur_world)
        if cur_world.has_trash():
            cur_world.clean()
        visited_state = [cur_world]
        cost = {cur_world: 0}

        while not self.solution_found(cur_world):
            for vert in cur_world.child_vertexes():
                new_world = copy.deepcopy(cur_world)
                _cost = self.calculate_cost(new_world, cost[cur_world], vert)
                if new_world not in visited_state:
                    queue.append(new_world)
                    cost[new_world] = _cost
                    parents[new_world] = cur_world
                    visited_state.append(new_world)

            cur_world = queue[0]
            queue.pop(0)

        print("\nBest path:")
        self.find_path(cur_world, parents)
        print(f'Cost of the best path {cost[cur_world]}')

    def solution_found(self, world):
        if self.trash_size_known:
            return world.is_clean()
        return world.all_visited()

    def calculate_cost(self, world, cost, vert):
        if vert in world.visited and vert != world.current_pos:
            cost = cost + world.current_pos.distance(vert) * self.visited_fee
        world.move(vert)
        world.clean()
        return cost + self.move_fee

import random
import matplotlib.pyplot as plt
import sys
import math


class TSP:
    def __init__(self, n, mode):
        if mode == 'random':
            self.nodes = [(random.random() * 100, random.random() * 100) for i in range(n)]
        elif mode == 'separated':
            list1 = [(random.random(), random.random()) for i in range(n // 4)]
            list2 = [(random.random() + 10, random.random()) for i in range(n // 4)]
            list3 = [(random.random(), random.random() + 50) for i in range(n // 4)]
            list4 = [(random.random() + 10, random.random() + 20) for i in range(n // 4)]
            self.nodes = list1 + list2 + list3 + list4
            random.shuffle(self.nodes)
        else:
            print("unknown mode")
            sys.exit()

    def euclidean_metric(self, point1, point2):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

    def path_length(self, nodes):
        length = 0
        for i in range(len(nodes)):
            length += self.euclidean_metric(nodes[i], nodes[(i + 1) % len(nodes)])
        return length


class SimulatedAnnealing:
    best_path = []

    def show_cloud(self, points):
        x = list(map(lambda x: x[0], points))
        y = list(map(lambda x: x[1], points))
        plt.plot(x, y)
        plt.show()

    def show_graph(self, xs, ys):
        plt.plot(xs, ys)
        plt.show()

    def swap_nodes(self, points, tsp, prob):
        old_length = tsp.path_length(points)
        node = random.randint(0, len(points) - 2)
        points[node], points[node + 1] = points[node + 1], points[node]
        new_length = tsp.path_length(points)
        if new_length > old_length:
            if random.random() > prob:
                points[node], points[node + 1] = points[node + 1], points[node]

    #  simulated annealing
    def simulate(self, iter_count, p, count, mode):
        tsp = TSP(count, mode)
        iterations = []
        energy = []
        curr_len = tsp.path_length(tsp.nodes)
        i = 0

        best_path = tsp.nodes
        sim.show_cloud(tsp.nodes)

        while i < iter_count:
            self.swap_nodes(tsp.nodes, tsp, p)
            curr_len = tsp.path_length(tsp.nodes)
            if curr_len < tsp.path_length(best_path):
                best_path = tsp.nodes
            iterations.append(i)
            energy.append(curr_len)
            if i % 100 == 0:
                p *= 0.99
            i += 1

        self.show_cloud(best_path)
        print(tsp.path_length(best_path))
        print(tsp.path_length(tsp.nodes))

        self.show_graph(iterations, energy)


if __name__ == "__main__":
    sim = SimulatedAnnealing()
    sim.simulate(100000, 0.9, 32, 'separated')

import numpy as np
import random
import csv
import networkx as nx
import matplotlib.pyplot as plt
from sympy.physics.quantum.tests.test_circuitplot import mpl


def visualize(graph, special_nodes, mode):
    pos = {}
    if mode == "rand":
        pos = nx.layout.spring_layout(graph)
    elif mode == "bridge":
        pos = nx.layout.spring_layout(graph)
    elif mode == "2d":
        pos = {}
        for i, j in graph.nodes():
            pos.update({(i, j): [i, -j]})
    else:
        pos = nx.shell_layout(graph)

    current = [100 * graph[e1][e2]['I'] for e1, e2 in graph.edges()]
    # for i in current:
    #     # print(i)
    colors_node = []
    size_node = []
    for node in graph.nodes():
        if node in special_nodes:
            colors_node.append('red')
            size_node.append(100)
        else:
            colors_node.append('black')
            size_node.append(25)
    labels = nx.get_edge_attributes(graph, 'I')
    for e in graph.edges():
        graph[e[0]][e[1]]['I'] = round(graph[e[0]][e[1]]['I'], 4)
    fig = plt.gcf()
    fig.set_size_inches(10, 10)

    nx.draw(graph, pos, edges=graph.edges(), with_labels=False, edge_color=current,
            edge_cmap=plt.cm.Blues, node_color=colors_node, node_size=size_node)

    nx.draw_networkx_edge_labels(graph, pos, font_size=4, edge_labels=labels)
    plt.show()
    #fig.savefig('SOME PATH', dpi=400)


def import_from_file(file):
    records = []
    G = nx.Graph()
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            records.append(row)
    G.add_nodes_from(list(map(lambda x: int(x[0]), records)))
    for i, record in enumerate(records):
        # print(record, i)
        G.add_edge(int(record[0]), int(record[1]), R=abs(int(record[2])), no=i + 1, sem=0)
    return G


def KirII(G):
    eq = []
    b = []
    edges_count = len(G.edges)
    for cycle in nx.cycle_basis(G):
        # print(cycle)
        Is = [0 for i in range(edges_count)]
        b.append(0)
        for i in range(len(cycle)):
            n1 = cycle[i]
            n2 = cycle[(i + 1) % len(cycle)]
            data = G.get_edge_data(n1, n2)
            Is[data['no']] = data['R'] if n1 > n2 else -data['R']
            b[-1] += data['sem'] if n1 > n2 else -data['sem']
        eq.append(Is)
    return eq, b


def kirchoffs_circuit_laws(G):
    # I Kirchoff's law
    eq = []
    b = []
    edges_count = len(G.edges)
    for n in G.nodes:
        Is = [0 for j in range(edges_count)]
        b.append(0)
        for e in G.edges(n):
            data = G.get_edge_data(*e)
            Is[data['no']] = 1 if e[0] > e[1] else -1
        eq.append(Is)
    # II Kirchoff's law
    eq1, b1 = KirII(G)
    eqs = eq + eq1
    b = b + b1
    return eqs, b


def check_I_law(G, res):
    for node in G.nodes:
        checker = 0
        for edge in G.edges(node):
            curr_id = G.get_edge_data(*edge).get('no')
            if edge[0] > edge[1]:
                checker += res[curr_id]
            else:
                checker -= res[curr_id]
        if checker > 1e-10:
            return False
    return True


def check_II_law(G, res):
    for cycle in nx.cycle_basis(G):
        sems = 0
        valtages = 0
        for i in range(len(cycle)):
            node1 = cycle[i]
            node2 = cycle[(i + 1) % len(cycle)]
            r = G.get_edge_data(node1, node2).get('R') if node1 > node2 else -G.get_edge_data(node1, node2).get('R')
            valtages += r * res[G.get_edge_data(node1, node2).get('no')]
            sems += G.get_edge_data(node1, node2).get('sem') if node1 > node2 else -G.get_edge_data(node1, node2).get(
                'sem')
        if abs(sems - valtages) > 1e-10:
            return False
    return True


def convert_to_digraph(G):
    I, E = kirchoffs_circuit_laws(G)
    res = np.linalg.lstsq(I, E, rcond=None)[0]
    # for e in G.edges:
    #     print(e)
    for i, e in enumerate(G.edges):
        G[e[0]][e[1]]['I'] = res[G[e[0]][e[1]]["no"]]
    digraph = nx.DiGraph()
    digraph.add_nodes_from(G)
    for i, e in enumerate(G.edges):
        # print(e, G[e[0]][e[1]]['I'])
        if G[e[0]][e[1]]['I'] > 0:
            digraph.add_edge(max(e[0], e[1]), min(e[0], e[1]), I=G[e[0]][e[1]]['I'])
        else:
            digraph.add_edge(min(e[0], e[1]), max(e[0], e[1]), I=abs(G[e[0]][e[1]]['I']))
    return digraph, res


def print_whether_correct(G, res):
    if check_I_law(G, res):
        print("I law fulfilled ")
    else:
        print("something went wrong :(")
    if check_II_law(G, res):
        print("II law fulfilled ")
    else:
        print("something went wrong :(")


# SPÓJNY LOSOWY GRAF:

G_sample_rand = nx.erdos_renyi_graph(25, 0.3)
Grand = nx.Graph()
Grand.add_nodes_from(G_sample_rand)
i = 1
for e in G_sample_rand.edges:
    Grand.add_edge(e[0], e[1], R=random.randint(1, 3), no=i, sem=0)
    # print(e, "weight: ", Grand[e[0]][e[1]]['R'], "no: ", Grand[e[0]][e[1]]['no'])
    i += 1

# add sem:
e = (0, 1)
if Grand.has_edge(*e):
    Grand[0][1]['sem'] = 1000
    Grand[0][1]['R'] = 0
else:
    Grand.add_edge(0, 1, no=0, R=0, sem=1000)

digraph_rand, resrand = convert_to_digraph(Grand)
print("random graph:")
print_whether_correct(Grand, resrand)

visualize(digraph_rand, [0, 1], "rand")
#
# GRAF 2D
G_sample2D = nx.grid_2d_graph(10, 10)
G2D = nx.Graph()
G2D.add_nodes_from(G_sample2D)
i = 0
for e in G_sample2D.edges:
    G2D.add_edge(e[0], e[1], R=random.randint(1, 3), no=i, sem=0)
    # print(e, "weight: ", G2D[e[0]][e[1]]['R'], "no: ", G2D[e[0]][e[1]]['no'])
    i += 1
e = ((0, 0), (0, 1))
G2D[(0, 0)][(0, 1)]['sem'] = 1000
G2D[(0, 0)][(0, 1)]['R'] = 0

digraph2D, res2D = convert_to_digraph(G2D)
print("cubic:")
print_whether_correct(G2D, res2D)

visualize(digraph2D, [(0, 1), (0, 0)], "2d")

# GRAF 3-regularny
G_sample_rand = nx.random_regular_graph(3, 100)
Greg = nx.Graph()
Greg.add_nodes_from(G_sample_rand)
i = 1
for e in G_sample_rand.edges:
    Greg.add_edge(e[0], e[1], R=random.randint(1, 3), no=i, sem=0)
    # print(e, "weight: ", Greg[e[0]][e[1]]['R'], "no: ", Greg[e[0]][e[1]]['no'])
    i += 1

# add sem:
e = (0, 1)
if Greg.has_edge(*e):
    Greg[0][1]['sem'] = 1000
    Greg[0][1]['R'] = 0
else:
    Greg.add_edge(0, 1, no=0, R=0, sem=1000)

digraph_reg, resreg = convert_to_digraph(Greg)
print("3-reg graph:")
print_whether_correct(Greg, resreg)

visualize(digraph_reg, [0, 1], "3reg")

# GRAF Z MOSTKIEM:

G_1 = nx.erdos_renyi_graph(25, 0.3)
G_2 = nx.erdos_renyi_graph(25, 0.3)
Grand1 = nx.Graph()
Grand1.add_nodes_from(G_1)

for node in G_2.nodes():
    Grand1.add_node(node + 25)

i = 1
for e in G_1.edges:
    Grand1.add_edge(e[0], e[1], R=random.randint(1, 3), no=i, sem=0)
    i += 1
for e in G_2.edges:
    Grand1.add_edge(e[0] + 25, e[1] + 25, R=random.randint(1, 3), no=i, sem=0)
    i += 1

# add sem:
e = (0, 25)
Grand1.add_edge(3, 43, no=0, R=0, sem=1000)

# add bridge:

Grand1.add_edge(4, 30, R=1, no=i, sem=0)

digraph_rand, randbridge = convert_to_digraph(Grand1)
print("bridge:")
print_whether_correct(Grand1, randbridge)

visualize(digraph_rand, [3, 43], "bridge")

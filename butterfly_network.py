import matplotlib.pyplot as plt
import networkx as nx
import math


def build_butterfly_network(n):
    assert (n & (n - 1)) == 0 and n > 0, "n must be a power of 2"
    logn = int(math.log2(n))
    stages = 2 * logn
    G = nx.DiGraph()

    for stage in range(stages):
        for node in range(n):
            G.add_node((stage, node), layer=stage)

    for stage in range(stages - 1):
        for node in range(n):
            G.add_edge((stage, node), (stage + 1, node))

            if stage < logn:
                bit = logn - stage - 1
            else:
                bit = stage - logn + 1

            partner = node ^ (1 << bit)
            G.add_edge((stage, node), (stage + 1, partner))

    return G, stages, n


def draw_butterfly_network(G, stages, n):
    pos = {}
    node_colors = []
    cmap = plt.get_cmap("viridis")

    for (stage, node) in G.nodes():
        x = node
        y = -stage
        pos[(stage, node)] = (x, y)
        node_colors.append(cmap(stage / stages))

    plt.figure(figsize=(14, 8))
    nx.draw_networkx_nodes(G, pos, node_size=100, node_color=node_colors)
    nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=10)

    for node in range(n):
        plt.text(node, 0.5, f"in({node})", ha="center", va="bottom", fontsize=9)
        plt.text(node, -stages + 0.5, f"out({node})", ha="center", va="top", fontsize=9)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

n = 2 ** 3
G, stages, n = build_butterfly_network(n)
draw_butterfly_network(G, stages, n)


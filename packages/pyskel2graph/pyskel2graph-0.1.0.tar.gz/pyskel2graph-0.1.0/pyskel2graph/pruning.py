import networkx as nx
import numpy as np
from skimage.morphology import skeletonize

from .metrics import cal_points_length
from .graph import skel_to_graph


def pruning(
        graph: nx.MultiGraph,
        threshold: int | float,
        shape: tuple[int, int],
) -> nx.MultiGraph:
    canvas = np.zeros(shape, dtype=np.uint8)

    edges = [
        ((u, v, k), cal_points_length(data['comp'].points))
        for u, v, k, data in graph.edges(data=True, keys=True)
        if graph.degree(u) == 1 or graph.degree(v) == 1
    ]
    edges = sorted(edges, key=lambda x: x[1])

    for (u, v, k), length in edges:
        if length > threshold:
            break
        if len(list(graph.neighbors(u))) >= 3 or len(list(graph.neighbors(v))) >= 3:
            graph.remove_edge(u, v, k)

    graph.remove_nodes_from(list(nx.isolates(graph)))

    for u, v, k, data in graph.edges(data=True, keys=True):
        comp = data['comp']
        points = comp.points
        canvas[points[:, 0], points[:, 1]] = 255

    for n, data in graph.nodes(data=True):
        comp = data['comp']
        points = comp.points
        canvas[points[:, 0], points[:, 1]] = 255

    canvas = skeletonize(canvas)
    return skel_to_graph(canvas)

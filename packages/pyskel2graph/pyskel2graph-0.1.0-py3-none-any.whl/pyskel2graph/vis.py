import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def vis_skeleton(skeleton) -> np.ndarray:
    canvas = np.zeros_like(skeleton, dtype=np.uint8)
    canvas[skeleton > 0] = 255
    return canvas


def vis_degrees(
        degree_map: np.ndarray,
        color_1: tuple[int, int, int] = (0, 0, 255),
        color_2: tuple[int, int, int] = (255, 255, 255),
        color_3: tuple[int, int, int] = (0, 255, 0),
) -> np.ndarray:
    canvas = np.zeros(degree_map.shape + (3,), dtype=np.uint8)
    canvas[degree_map == 1] = color_1
    canvas[degree_map == 2] = color_2
    canvas[degree_map >= 3] = color_3
    return canvas


def vis_graph(
        graph: nx.MultiGraph,
        shape: tuple[int, int],
):
    canvas = np.zeros(shape, dtype=np.uint8)
    for _, data in graph.nodes(data=True):
        comp = data['comp']
        coords = comp.points
        rs, cs = coords[:, 0], coords[:, 1]
        canvas[rs, cs] = 255

    for _, _, _, data in graph.edges(data=True, keys=True):
        comp = data['comp']
        coords = comp.points
        rs, cs = coords[:, 0], coords[:, 1]
        canvas[rs, cs] = 128

    return canvas


def vis_graph_plt(graph, img=None, edge_color='yellow', end_color='red', branch_color='green'):
    fig, ax = plt.subplots(figsize=(10, 10))

    if img is not None:
        ax.imshow(img, cmap='gray')

    # draw edges
    for u, v, k, data in graph.edges(keys=True, data=True):
        edge_obj = data.get('comp')
        if edge_obj:
            # (r, c) -> x=c, y=r
            ax.plot(edge_obj.points[:, 1], edge_obj.points[:, 0],
                    color=edge_color, linewidth=1, alpha=0.6)

    # draw nodes
    for n, data in graph.nodes(data=True):
        node_obj = data.get('comp')
        if node_obj:
            r, c = node_obj.centroid
            color = branch_color if node_obj.type == 'branch' else end_color
            ax.scatter(c, r, s=30, c=color, edgecolors='white', zorder=5)

    ax.axis('off')
    plt.show()

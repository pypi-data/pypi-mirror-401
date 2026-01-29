import networkx as nx
import numpy as np

from dataclasses import dataclass

from .degree import get_degrees, get_regions


@dataclass
class Component:
    id: int
    points: np.ndarray  # [N, 2] (r, c)
    centroid: tuple[float, float]  # (r, c)


@dataclass
class Node(Component):
    type: str  # 'end' or 'branch'


@dataclass
class Edge(Component):
    uid: int
    vid: int
    u: str
    v: str


def _get_pixel_to_node_map(graph: nx.MultiGraph) -> dict[tuple[int, int], str]:
    pixel2node = {}
    for node_key, data in graph.nodes(data=True):
        comp: Node = data['comp']
        for r, c in comp.points:
            pixel2node[(r, c)] = node_key

    return pixel2node


def _neighbors(p):
    r, c = p
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            yield r + dr, c + dc


def get_graph(regions) -> nx.MultiGraph:
    endpoint_regions, edge_regions, branch_regions = regions

    graph = nx.MultiGraph()

    # add endpoint nodes
    for i, region in enumerate(endpoint_regions):
        node = Node(
            id=i + 1,
            points=region.coords,
            centroid=region.centroid,
            type='end'
        )
        graph.add_node(
            f'end_{i + 1}',
            comp=node
        )
    # add branch nodes
    for i, region in enumerate(branch_regions):
        node = Node(
            id=i + 1,
            points=region.coords,
            centroid=region.centroid,
            type='branch'
        )
        graph.add_node(
            f'branch_{i + 1}',
            comp=node
        )

    # add edges
    pixel2node = _get_pixel_to_node_map(graph)
    edge_id = 1
    for region in edge_regions:
        nodes = set()

        for p in region.coords:
            for nb in _neighbors(p):
                if nb in pixel2node:
                    nodes.add(pixel2node[nb])

        assert len(nodes) == 2

        u, v = nodes
        uid, vid = graph.nodes[u]['comp'].id, graph.nodes[v]['comp'].id
        edge = Edge(
            id=edge_id,
            points=region.coords,
            centroid=region.centroid,
            uid=uid, vid=vid,
            u=u, v=v,
        )
        graph.add_edge(u, v, comp=edge)
        edge_id += 1

    graph.remove_nodes_from(list(nx.isolates(graph)))

    return graph


def skel_to_graph(skeleton: np.ndarray) -> nx.MultiGraph:
    degrees = get_degrees(skeleton)
    regions = get_regions(degrees)
    graph = get_graph(regions)
    return graph

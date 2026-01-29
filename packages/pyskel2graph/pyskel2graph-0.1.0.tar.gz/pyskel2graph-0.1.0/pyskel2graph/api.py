import numpy as np
import networkx as nx

from .graph import skel_to_graph
from .pruning import pruning


def skel2graph(skeleton_img: np.ndarray, pruning_threshold: float | int = 0) -> nx.MultiGraph:
    assert skeleton_img.ndim == 2
    graph = skel_to_graph(skeleton_img)
    if pruning_threshold > 0:
        graph = pruning(graph, pruning_threshold, skeleton_img.shape)
    return graph




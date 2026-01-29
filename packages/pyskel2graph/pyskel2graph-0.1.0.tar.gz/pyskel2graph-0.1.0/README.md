# PySkel2Graph

### Convert the Skeleton to a Graph using Python.

---

## Install

```shell
pip install pyskel2graph
```

## Use

```python
from pyskel2graph.io import imread, imwrite
from pyskel2graph import skel2graph
from pyskel2graph.vis import vis_graph, vis_graph_plt

img = imread('assets/test.jpg')
skel = imread('assets/skeleton.png')
graph = skel2graph(skel, pruning_threshold=5)
vis_graph_plt(graph, img=img)
imwrite(vis_graph(graph, skel.shape), 'assets/pruning_skel.png')
```

### Image
![img](assets/test.jpg)

### Skeleton (Obtain through certain methods)
![skeleton](assets/skeleton.png)

### Skeleton (pruning_threshold=5)
![sp](assets/pruning_skel.png)

### Graph
![graph](assets/graph_plt.png)


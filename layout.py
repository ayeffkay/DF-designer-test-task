import random
import json
import math
import sys
import itertools
from typing import List, Dict, Union, Any, Optional

random.seed(42)


class Node:
    def __init__(self, title: str, 
                 adj: Union[List[str], List[int]], 
                 width: int = 10,
                 height: int = 10
                ):
        self.title = title
        x = random.uniform(0, width)
        y = random.uniform(0, height)
        self.force = [x, y]
        self.adj = adj
    
    def __str__(self):
        return json.dumps({'title': self.title, 
                          'force': '({:.4f}, {:.4f})'.format(*self.force), 
                          'adj': '; '.join(map(str, self.adj))})

    def get_coords(self) -> List[float]:
        return self.force

    def get_neighbors(self) -> list:
        return self.adj

    def __sub__(self, other) -> List[float]:
        """
            Elementwise subtraction
        """
        d_x = self.force[0] - other.force[0]
        d_y = self.force[1] - other.force[1]
        return [d_x, d_y]


class Graph:
    def __init__(self, graph_dict: Dict[str, List[str]], width: int = 10, height: int = 10):
        self.graph_dict = graph_dict
        self.nodes = []
        self.width = width
        self.height = height
        self.build_graph()

    def __getitem__(self, key: str) -> Union[Any, Node]:
        for node in self.nodes:
            if node.title == key:
                return node
        return None

    def get_graph_dict(self):
        nodes = []
        edges = []
        for i, node in enumerate(self.nodes):
            nodes.append({'title': node.title, 
                          'x': node.force[0], 
                          'y': node.force[1]})
            for src, trg in itertools.product([i], node.adj):
                edges.append({'src': src, 'trg': trg})
        graph_dict = dict(nodes=nodes, edges=edges)
        return graph_dict

    def __str__(self):
        graph_dict = self.get_graph_dict()
        return json.dumps(graph_dict)


    def build_graph(self):
        """
            Build list of Node() instances with neighbor indices in this list
        """
        if len(self.nodes) > 0:
            del self.nodes[:]
        all_nodes = list(self.graph_dict.keys())
        for node_name in all_nodes:
            adj_idxs = [all_nodes.index(neighbor_name) for neighbor_name in self.graph_dict[node_name]]
            node = Node(node_name, adj_idxs, self.width, self.height)
            self.nodes.append(node)

    @staticmethod
    def norm(node1: Node, 
             node2: Optional[Node] = None) -> float:
             
        if node2 is not None:
            d_x, d_y = node1 - node2
        else:
            d_x, d_y = node1.force
        return math.sqrt(d_x ** 2 + d_y ** 2)

    @staticmethod
    def unit_vector(node1: Node, 
                    node2: Node) -> List[float]:

        d_x, d_y = node2 - node1
        n = Graph.norm(node1, node2)
        return [d_x / n, d_y / n]

    @staticmethod
    def f_rep(c_rep: float, 
              node1: Node, 
              node2: Node) -> List[float]:

        x_u, y_u = Graph.unit_vector(node1, node2) 
        rep = c_rep / Graph.norm(node1, node2) ** 2
        return [x_u * rep, y_u * rep]

    @staticmethod
    def f_spring(c_spring: float, 
                 l: float, 
                 node1: Node, 
                 node2: Node) -> List[float]:
        x_u, y_u = Graph.unit_vector(node2, node1)
        spring = c_spring * math.log(Graph.norm(node1, node2) / l)
        return [x_u * spring, y_u * spring]

    def make_step(self, c_rep: float = 1.0, 
                  c_spring: float = 2.0, 
                  l: float = 1.0, 
                  delta: float = 0.99):

        for i in range(len(self.nodes)):
            f_rep_dict = {}
            f_attr_dict = {}
            # compute repulsive forces
            for j in range(len(self.nodes)):
                if i == j:
                    continue
                rep = Graph.f_rep(c_rep, self.nodes[j], self.nodes[i])
                f_rep_dict[j] = rep
            # compute attractive forces
            for adj_idx in self.nodes[i].adj:
                spring = Graph.f_spring(c_spring, l, self.nodes[adj_idx], self.nodes[i])
                f_attr_x = spring[0] - f_rep_dict[adj_idx][0]
                f_attr_y = spring[1] - f_rep_dict[adj_idx][1]
                f_attr_dict[adj_idx] = [f_attr_x, f_attr_y]
            
            f_rep_x = sum(t[0] for t in f_rep_dict.values())
            f_rep_y = sum(t[1] for t in f_rep_dict.values())
            f_attr_x = sum(t[0] for t in f_attr_dict.values())
            f_attr_y = sum(t[1] for t in f_attr_dict.values())
            
            # resulting displacement
            f_x = f_rep_x + f_rep_y
            f_y = f_attr_x + f_attr_y

            # update
            self.nodes[i].force[0] += delta * f_x
            self.nodes[i].force[1] += delta * f_y
    
    def neg_alignment(self):
        """
            All coordinates need to be non-negative
        """
        min_x = min(self.nodes, key=lambda x: x.force[0]).force[0]
        min_y = min(self.nodes, key=lambda x: x.force[1]).force[1]
        if min_x > 0 and min_y > 0:
            return
        for i in range(len(self.nodes)):
            if min_x < 0:
                self.nodes[i].force[0] += abs(min_x)
            if min_y < 0:
                self.nodes[i].force[1] += abs(min_y)

    def forces2int(self):
        """
            As coordinates need to be integers
        """
        for i in range(len(self.nodes)):
            self.nodes[i].force[0] = int(round(self.nodes[i].force[0]))
            self.nodes[i].force[1] = int(round(self.nodes[i].force[1]))

    def compute_forces(self, T: int = 100, 
                       c_rep: float = 1.0, 
                       c_spring: float = 2.0, 
                       l: float = 1.0, 
                       delta: float = 0.99, 
                       eps: float = 1.0):

        t = 0
        max_norm = sys.maxsize
        while t < T and max_norm > eps:
            self.make_step(c_rep, c_spring, l, delta)
            max_norm = Graph.norm(max(self.nodes, key=lambda x: Graph.norm(x)))
            t += 1
        self.neg_alignment()
        self.forces2int()
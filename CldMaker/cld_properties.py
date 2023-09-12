import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

class CLD(nx.MultiDigraph):
    def __init__(self, data = None, **attr):
        super().__init__(data, **attr)

    def __str__(self):
        graph_properties ={
            "Nodes": self.number_of_nodes(),
            "Links": self.number_of_links(),
            "Loops": self.get_num_loops(),
            "R_loop": self.get_num_r_loop(),
            "B_loop": self.get_num_b_loop(),
            "Edge Polarity": self.get_edge_polarity(),
            "Nodes List": self.get_node_list(),
            "Adjacency Matrix\n": self.get_adjacency_matrix(),
            "Polarity Matrix\n": self.get_polarity_matrix()
        }

        properties_str = "\n".join([f"{prop}:{value}"for prop, value in graph_properties.items()])
        return properties_str

    def get_cycle(self):
        return sorted(nx.simple_cycle())

    def get_num_loops(self):
        return len(self.get_cycle())
    def get_edge_polarity(self):
        return list(nx.get_edge_attributes(self, "weight").values())

    def get_r_b_loop(self, sg):
        edges = sg.get_edge_polarity()
        edges = np.array(edges)
        label = np.prod(edges)
        return label

    def get_cycle_subgraph(self, sg_nodes):
        nxg = CLD()
        sg_nodes_dict = [(n,{'label':n}) for n in sg_nodes]
        nxg.add_nodes_from(sg_nodes_dict)
        for i in range(len(sg_nodes_dict)):
            n1 = sg_nodes[i]
            n2 = sg_nodes[(i+1)%len(sg_nodes)]

            weight = self.get_edge_data(n1,n2)[0]['weight']
            nxg.add_edge(n1,n2, weight = weight)
        return  nxg

    def get_all_loops(self):
        loops =[]
        loop_list = self.get_cycle()
        for loop in loop_list:
            sg = self.get_cycle_subgraph(loop)
            loop_type = self.get_r_b_loop(sg)
            loops.append(loop_type)
        return loops

    def get_num_r_loop(self):
        loops = self.get_all_loops()
        num_r_loop = loops.count(1)
        return num_r_loop

    def get_num_b_loop(self):
        loops = self.get_all_loops()
        num_b_loop = loops.count(-1)
        return num_b_loop

    def get_node_list(self):
        return list(self.nodes)

    def get_adjacency_matrix(self):
        a = nx.adjacency_matrix(
            self,
            nodelist = list(self.nodes),
            weight ='None'
        ).todense(
        )
        return a

    def get_polarity_matrix(self):
        a = nx.adjacency_matrix(
            self,
            nodelist=list(self.nodes),
            weight='weight'
        ).todense(
        )
        return a

    ###

def get_graph_distance(g1, g2):
    paths, cost = nx.optimal_edit_paths(g1,g2)
    return cost

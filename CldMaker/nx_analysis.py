import re

import networkx as nx


def graphviz_2_nx(g):
    nxg = nx.DiGraph()
    all_nodes = re.findall(r'"([^"]*)"', g)
    all_nodes_dict = [(n, {'label': n}) for n in all_nodes]
    nxg.add_nodes_from(all_nodes_dict)
    edges = g.split('\n')
    for edge in edges:
        edge_n = re.findall(r'"([^"]*)"', edge)
        weight = re.findall(r'\[arrowhead = ([^"]*)\]', edge)
        if weight == ['vee'] or weight == []:
            weight = 1
        elif weight == ['tee']:
            weight = -1
        else:
            print('weight not recognised!')
        if len(edge_n) == 2 and edge_n[0] != edge_n[1]:
            nxg.add_edge(edge_n[0], edge_n[1], weight=weight)
    return nxg


def nx_2_graphviz(nxg):
    g = 'digraph {\n'
    edges = list(nxg.edges())
    weights = list(nx.get_edge_attributes(nxg, 'weight').values())
    weights = ['vee' if w == 1 else 'tee' for w in weights]
    for edge, w in zip(edges, weights):
        g += '\"%s\" -> \"%s\" [arrowhead=%s]\n' % (*edge, w)
    g += '}'
    return g

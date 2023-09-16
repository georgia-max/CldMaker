# import nltk
# import numpy as np
# import regex as re
import graphviz
from IPython.display import display


# def check_syntax(r):
#     r = r.strip()
#     nq = len(re.findall(re.compile(r'\"'),r))
#     nb = len(re.findall(re.compile(r'\[|\]',r)))
#     if nq%2 != 0 or nb%2 != 0:
#         return '\n'
#     elif nb ==0 and '\"' in r:
#         return '\n'
#     r = re.sub(re.compile('arrowhead='),'arrowhead =',r)
#     return r

# def clean_graphs(g):
#     #remove uneeded text/numbers
#     pattern_string = r'\d\)[Graph:|(\n)?(})?Input:.*|\<(.*?)\>|#include(})?|\*/'
#     ng_pattern = re.compile(pattern_string)
#     g = re.sub(ng_pattern, '',g)
#     #remove trailing spaces
#     g = g.strip()
#     g = re.sub(' +', ' ',g)
#     # check if empty i.e just \n characters
#     if set(g) <= set('\n ') or set(g) <=set(' '):
#         return None

#     # if 2 digraphs, merge them
#     dg_pattern = re.compile('digraph {\n|}')
#     disjoint_g = len(re.findall(dg_pattern,g)) >2
#     if disjoint_g:
#         new_g = 'digraph {\n'
#         new_g += re.sub(dg_pattern, '',g)
#         new_g += '}'
#         g = new_g

#     #remove rows with incorrect syntax
#     rows = g.split('\n')
#     rows = [check_syntax(row) for row in rows]
#     g = '\n'.join(rows)
#     #format closing
#     if g[-1] != '}':
#         g += '}'
#     if g[-3:] == '->}' or g[-3:] == '-> }':
#         g = g[:-3] + '}'
#     return g


def render_gvz(dot_source: str, name: str, file_name: str):
    """
    Renders the graphviz image given DOT format. 
    """
    g = graphviz.Source(dot_source) 
    display(g)
    g.render(filename=f'img/{file_name}_{name}', format = 'png')
    return None


# g = """
#     digraph {
#     "order rate" -> "inventory" [arrowhead = vee]
#     "inventory"->"order rate"[arrowhead = tee] 
#     "desired inventory" -> "order rate"[arrowhead = vee] 
#     "adjustment time" -> "order rate"[arrowhead = tee] }
#     """

# render_gvz(g, "test")
import os
import pygraphviz
import inherit_relation as ir
from clang.cindex import Index

kInputsDir = os.path.join(os.path.dirname(__file__), 'cpp')

def draw(G, output_filename):
    G.layout(prog='dot')
    G.draw(output_filename)

def build():
    cpp_file_path = os.path.join(kInputsDir, 'main.cpp')
    index = Index.create()
    tu = index.parse(cpp_file_path)
    G = pygraphviz.AGraph(directed=True)
    for this, parent in ir.each_inheritance_relation(tu.cursor):
        edge = (parent, this)
        G.add_edge(edge)
    return G

if __name__ == '__main__':
    graph = build()
    draw(graph, 'inherit.png')

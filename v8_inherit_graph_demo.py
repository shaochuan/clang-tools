import os
import pygraphviz
import inherit_relation as ir
from clang.cindex import Index

opencv_dir = os.path.sep.join(['v8', 'src'])
kInputsDir = os.path.join(os.path.dirname(__file__), opencv_dir)

include_args = ['-I'+dirname for dirname, dirs, files in os.walk('v8') if
        os.path.basename(dirname) in ('include', 'includes')]
include_args.append('-Iv8/src')
extra_args = ['-stdlib=libc++', '-std=c++0x']

def draw(G, output_filename):
    G.layout(prog='sfdp')
    G.draw(output_filename)

def get_tu(cpp_basename):
    cpp_file_path = os.path.join(kInputsDir, cpp_basename)
    print 'clang++ -c ' + ' '.join(extra_args) + \
            ' ' + ' '.join(include_args) + ' ' + cpp_file_path
    index = Index.create()
    tu = index.parse(cpp_file_path, args=extra_args+include_args)
    return tu

def build(cpp_basename):
    tu = get_tu(cpp_basename)
    G = pygraphviz.AGraph(directed=True)
    for this, parent in ir.each_inheritance_relation(tu.cursor):
        print this,parent
        edge = (this, parent)
        G.add_edge(edge)
    return G

if __name__ == '__main__':
    graph = build('v8.cc')
    draw(graph, 'inherit.svg')

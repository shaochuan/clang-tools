clang-tools
===========
A tool that visualizes inheritance relations between classes in C++.

Dependencies
============
1. `brew install graphviz`
2. `sudo pip install pygraphviz`

How to Run?
===========
1. Running simple_inherit_graph_demo.py
```
$ git clone https://github.com/shaochuan/clang-tools.git
$ cd clang-tools
$ python simple_inherit_graph_demo.py
```

![](https://github.com/shaochuan/clang-tools/blob/master/output/inherit.png)

2. Running v8 example
```
$ ./pull_submod.sh
$ python v8_inherit_graph_demo.py
```

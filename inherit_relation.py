import os
from clang.cindex import TranslationUnit
from clang.cindex import TokenKind, CursorKind
from clang.cindex import Index

kInputsDir = os.path.join(os.path.dirname(__file__), 'cpp')

def each_class_cursor(cursor):
    for c in cursor.get_children():
        if c.kind == CursorKind.CLASS_DECL:
            yield c
        each_class_cursor(c)

def each_inheritance_relation(cursor):
    for cls in each_class_cursor(cursor):
        for c in cls.get_children():
            if c.kind == CursorKind.CXX_BASE_SPECIFIER:
                yield cls.displayname, c.get_definition().displayname

if __name__ == '__main__':
    # demo parsing the base class and parent class relations
    cpp_file_path = os.path.join(kInputsDir, 'main.cpp')
    index = Index.create()
    tu = index.parse(cpp_file_path)
    for base, parent in each_inheritance_relation(tu.cursor):
        print base, parent

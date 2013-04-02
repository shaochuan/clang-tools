import os
from clang.cindex import TranslationUnit
from clang.cindex import TokenKind

kInputsDir = os.path.join(os.path.dirname(__file__), 'cpp')

def dump_tokens(cursor, level):
    for token in cursor.get_tokens():
        print '\t'*level, 'token:', token.kind, token.spelling

def dump_cursor(cur, level=0):
    if not cur:
        return
    print 
    print '\t'*level, cur.kind, cur.spelling
    print '\t'*level, cur.type.kind
    print '\t'*level, cur.displayname
    defi = cur.get_definition()
    if defi:
        print '\t'*level, 'definition:',defi.spelling
    dump_tokens(cur, level)

loop_keywords = ('for', 'while')
branch_keywords = ('if', 'else')
type_keywords = ('class', 'struct', 'typedef')
privacy_keywords = ('public', 'protected', 'private')
keywords = loop_keywords + branch_keywords + type_keywords + privacy_keywords

def warning_syntax_error(tu, token):
    print 'Warning! Syntax error at [file="%s", line=%s, col=%s]' % (
            tu.spelling, token.location.line, token.location.column)

def parse_parent(tokens, idx):
    idx += 1
    privacy_or_parent = tokens[idx]
    parent = privacy_or_parent
    if privacy_or_parent.spelling in privacy_keywords:
        idx += 1
        parent = tokens[idx]
    if parent.kind != TokenKind.IDENTIFIER:
        return idx, None
    return idx, parent

def each_inheritance_relation(tu):
    tokens = tuple(tu.cursor.get_tokens())
    n_tokens = len(tokens)
    for idx in xrange(n_tokens):
        tk = tokens[idx]
        if tk.spelling != 'class':
            continue

        idx += 1
        cls_token = tokens[idx]
        if cls_token.kind != TokenKind.IDENTIFIER or cls_token.spelling in keywords:
            warning_syntax_error(tu, cls_token)
            continue

        idx += 1
        punc_char = tokens[idx]
        if punc_char.spelling != ':':
            if punc_char.spelling != '{':
                warning_syntax_error(tu, punc_char)
            continue

        idx, parent = parse_parent(tokens, idx)
        if not parent:
            warning_syntax_error(tu, tokens[idx])
            continue
        yield (cls_token.spelling, parent.spelling)
        while True:
            idx += 1
            coma_or_brace = tokens[idx]
            if coma_or_brace.spelling != ',':
                break
            idx, parent = parse_parent(tokens, idx)
            if not parent:
                warning_syntax_error(tu, tokens[idx])
                break
            yield (cls_token.spelling, parent.spelling)
    #children = list(cursor.get_children())
    #dump_cursor(cursor)
    #for idx in xrange(len(children)-1):
    #    tks = list(children[idx].get_tokens())
    #    if not tks:
    #        continue
    #    if tks[0].spelling == 'class' and tks[-1].spelling in (':'):
    #        parent_tks = list(children[idx+1].get_tokens())
    #        if parent_tks[-1].kind == TokenKind.PUNCTUATION:
    #            yield (tks[1].spelling, parent_tks[1].spelling)
    #for c in children:
    #    for c, p in each_inheritance_relation(c):
    #        yield c, p

def each_include_file(cpp_file_path):
    tu = TranslationUnit.from_source(cpp_file_path)
    for file_inc in tu.get_includes():
        hfile = file_inc.include.name
        print hfile
        yield hfile


cpp_file_path = os.path.join(kInputsDir, 'main.cpp')

for hfile in each_include_file(cpp_file_path):
    tuh = TranslationUnit.from_source(hfile)
    for c, p in each_inheritance_relation(tuh):
        print c,p

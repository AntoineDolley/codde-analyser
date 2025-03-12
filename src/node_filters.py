import clang.cindex

def is_class(node):
    return node.kind in [clang.cindex.CursorKind.CLASS_DECL]

def is_struct(node):
    return node.kind in [clang.cindex.CursorKind.STRUCT_DECL]

def is_function(node):
    return node.kind in [clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]

def is_namespace(node):
    return node.kind == clang.cindex.CursorKind.NAMESPACE

def is_custom_type(node):
    return node.kind in [clang.cindex.CursorKind.TYPE_ALIAS_DECL]
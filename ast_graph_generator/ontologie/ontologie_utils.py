# ontologie/ontologie_utils.py
from dataclasses import dataclass, field
from ..utils import get_correct_path
import networkx as nx
from typing import Optional
import clang.cindex
import os

def get_function_signature(node: clang.cindex.Cursor) -> str:
    """
    Construit la signature complète d'une fonction, incluant son nom et ses paramètres.
    Exemple : "maFonction(int a, float b)"
    """
    if node.kind not in [clang.cindex.CursorKind.FUNCTION_DECL,
                         clang.cindex.CursorKind.CXX_METHOD,
                         clang.cindex.CursorKind.CONSTRUCTOR]:
        return node.spelling

    func_name = node.spelling
    params = []
    for arg in node.get_arguments():
        param_type = arg.type.spelling
        param_name = arg.spelling
        params.append(f"{param_type} {param_name}" if param_name else param_type)
    signature = f"{func_name}({', '.join(params)})"
    return signature


def get_class_node(node):
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            for child in node.get_children():
                if child.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                    for sub_child_1 in child.get_children():
                        if sub_child_1.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
                            for sub_child_2 in sub_child_1.referenced.get_children():
                                if sub_child_2.kind == clang.cindex.CursorKind.TYPE_REF:
                                    return sub_child_2
    print("N'est pas une fonction d'une custom class", node.spelling)
    return node
                                    
                            

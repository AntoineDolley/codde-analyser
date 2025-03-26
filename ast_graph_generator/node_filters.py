# node_filters.py
import clang.cindex
import os

def is_in_ontologie(node):
    """
    Retourne True si le nœud appartient à l'ontologie
    """
    return (
        is_class_decl(node) or
        is_struct_decl(node) or
        is_function_decl(node) or
        is_namespace_decl(node) or
        uses_custom_type(node) or
        is_custom_type(node) or
        is_function_call(node) or
        is_class_function_call(node)
    )

def is_a_declaration(node):
    """
    Retourne True si le nœud est une declaration
    """
    return (
        is_class_decl(node) or
        is_struct_decl(node) or
        is_function_decl(node) or
        is_namespace_decl(node)
    )

def is_class_decl(node):
    return node.kind in [clang.cindex.CursorKind.CLASS_DECL]

def is_struct_decl(node):
    return node.kind in [clang.cindex.CursorKind.STRUCT_DECL]

def is_function_decl(node):
    return node.kind in [clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]

def is_namespace_decl(node):
    return node.kind in [clang.cindex.CursorKind.NAMESPACE]

def uses_custom_type(node):
    return node.kind in [clang.cindex.CursorKind.TYPE_REF]

def is_custom_type(node):
    return node.kind in [clang.cindex.CursorKind.TYPE_ALIAS_DECL]

def is_function_call(node):
    return node.kind in [clang.cindex.CursorKind.CALL_EXPR, clang.cindex.CursorKind.MEMBER_REF_EXPR]

def is_class_function_call(node: clang.cindex.Cursor) -> bool:
    """
    Vérifie si le schéma spécifié existe dans l'AST.
    """
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
        for child in node.get_children():
            if child.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                for sub_child in child.get_children():
                    if sub_child.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
                        return True
    return False

import os
import logging

def is_allowed_node(node, ALLOWED_PATHS):
    """
    Retourne True si le nœud est autorisé selon les règles suivantes :
    
      - Si le node.spelling est présent dans ALLOWED_PATHS (détection du root node), on accepte.
      - Si le nœud n'a pas de localisation, on l'exclut.
      - Si le nœud se trouve dans un fichier source (extensions : .cpp, .c, .cc, .cxx), 
        on vérifie que son chemin complet ou son nom de fichier correspond à l'un des éléments de ALLOWED_PATHS.
      - Si le nœud se trouve dans un fichier d'en-tête (extensions : .h, .hpp, .hh), 
        on construit les noms de fichiers source correspondants en remplaçant l'extension par chacune 
        des extensions sources et on les accepte si l'un d'eux correspond à ALLOWED_PATHS.
    """
    # Détection du root node
    if node.spelling in ALLOWED_PATHS:
        return True

    # Exclure les nœuds sans localisation
    if not (node.location and node.location.file):
        return False

    # Normalisation du chemin du fichier du nœud
    file_path = os.path.normpath(os.path.abspath(node.location.file.name))
    root_name, ext = os.path.splitext(file_path)
    ext = ext.lower()

    # Extensions de fichiers source attendues
    source_exts = ['.cpp', '.c', '.cc', '.cxx']

    # Si le nœud est dans un fichier source
    if ext in source_exts:
        for allowed in ALLOWED_PATHS:
            allowed_abs = os.path.normpath(os.path.abspath(allowed))
            if file_path == allowed_abs or os.path.basename(file_path).lower() == os.path.basename(allowed_abs).lower():
                return True
        return False

    # Si le nœud est dans un fichier d'en-tête, on accepte uniquement s'il existe un fichier source correspondant
    if ext in ['.h', '.hpp', '.hh']:
        for src_ext in source_exts:
            corresponding = root_name + src_ext
            corresponding_abs = os.path.normpath(os.path.abspath(corresponding))
            for allowed in ALLOWED_PATHS:
                allowed_abs = os.path.normpath(os.path.abspath(allowed))
                if corresponding_abs == allowed_abs or os.path.basename(corresponding_abs).lower() == os.path.basename(allowed_abs).lower():
                    return True
        return False

    # Pour les autres types de fichiers, on exclut le nœud
    return False


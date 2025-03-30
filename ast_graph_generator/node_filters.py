# node_filters.py
import os
import logging
import clang.cindex

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
        is_standalone_function_call(node) or
        is_class_function_call(node) or 
        is_class_function_call_unxeposed(node) or 
        is_constructor_call(node)
    )

def is_decl(node):
    """
    Retourne True si le nœud est une declaration
    """
    return (
        is_class_decl(node) or
        is_struct_decl(node) or
        is_function_decl(node) or
        is_namespace_decl(node) 
    )

def is_call(node):
    """
    Retourne True si le nœud est un appel
    """
    return (
        is_function_decl(node) or
        uses_custom_type(node) or
        is_standalone_function_call(node) or
        is_class_function_call(node) or 
        is_class_function_call_unxeposed(node) or 
        is_constructor_call(node)
    )


# =================================
# Parsing des noeuds de declaration
# =================================

def is_class_decl(node):
    return node.kind in [clang.cindex.CursorKind.CLASS_DECL]

def is_struct_decl(node):
    return node.kind in [clang.cindex.CursorKind.STRUCT_DECL]

def is_function_decl(node):
    return node.kind in [clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]

def is_namespace_decl(node):
    return node.kind in [clang.cindex.CursorKind.NAMESPACE]

def is_custom_type_decl(node):
    return node.kind in [clang.cindex.CursorKind.TYPE_ALIAS_DECL]

# =================================
# Parsing des noeuds des references
# =================================

def uses_custom_type(node):
    return node.kind in [clang.cindex.CursorKind.TYPE_REF] and node.referenced is not None

def is_standalone_function_call(node):
    if node.kind in [clang.cindex.CursorKind.CALL_EXPR] and node.referenced is not None:
        if node.referenced.kind in [clang.cindex.CursorKind.FUNCTION_DECL]:
            return True
    return False

def is_class_function_call(node):
    if node.kind in [clang.cindex.CursorKind.CALL_EXPR] and node.referenced is not None:
        if node.referenced.kind in [clang.cindex.CursorKind.CXX_METHOD]:
            return True
    return False

def is_class_function_call_unxeposed(node):
    if node.kind in [clang.cindex.CursorKind.UNEXPOSED_EXPR]:
        for child in node.get_children():
            if child.kind in [clang.cindex.CursorKind.MEMBER_REF_EXPR] and child.referenced is not None:
                return True
    return False

def is_constructor_call(node):
    if node.kind == clang.cindex.CursorKind.DECL_STMT:
        for child in node.get_children():
            if child.kind == clang.cindex.CursorKind.VAR_DECL:
                for grandchild in child.get_children():
                    if grandchild.kind == clang.cindex.CursorKind.TYPE_REF and grandchild.referenced is not None:
                        if grandchild.referenced.kind == clang.cindex.CursorKind.CLASS_DECL:
                            return True
    return False

# =================================
# Filtres
# =================================

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
    
    # Extensions de fichiers headers attendues
    header_ext = ['.h', '.hpp', '.hh']

    # Si le nœud est dans un fichier d'en-tête, on accepte uniquement s'il existe un fichier source correspondant
    if ext in header_ext:
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

import os

def is_allowed_source_node(node, ALLOWED_PATHS):
    """
    Retourne True si le nœud se trouve dans un fichier source (.cpp, .c, .cc, .cxx)
    dont le chemin complet ou le nom de fichier correspond à l'un des éléments de ALLOWED_PATHS.
    """
    # Détection du root node
    if node.spelling in ALLOWED_PATHS:
        return True

    # Exclure les nœuds sans localisation
    if not (node.location and node.location.file):
        return False

    file_path = os.path.normpath(os.path.abspath(node.location.file.name))
    root_name, ext = os.path.splitext(file_path)
    ext = ext.lower()

    source_exts = ['.cpp', '.c', '.cc', '.cxx']
    if ext in source_exts:
        for allowed in ALLOWED_PATHS:
            allowed_abs = os.path.normpath(os.path.abspath(allowed))
            if file_path == allowed_abs or os.path.basename(file_path).lower() == os.path.basename(allowed_abs).lower():
                return True
        return False
    return False

def is_allowed_header_node(node, ALLOWED_PATHS):
    """
    Retourne True si le nœud se trouve dans un fichier d'en-tête (.h, .hpp, .hh) et s'il existe un fichier source
    correspondant (avec une extension source) présent dans ALLOWED_PATHS.
    
    ALLOWED_PATHS ne contient que des chemins se terminant par .cpp.
    """
    # Détection du root node
    if node.spelling in ALLOWED_PATHS:
        return True

    # Exclure les nœuds sans localisation
    if not (node.location and node.location.file):
        return False

    file_path = os.path.normpath(os.path.abspath(node.location.file.name))
    root_name, ext = os.path.splitext(file_path)
    ext = ext.lower()

    header_exts = ['.h', '.hpp', '.hh']
    if ext in header_exts:
        source_exts = ['.cpp', '.c', '.cc', '.cxx']
        for src_ext in source_exts:
            corresponding = root_name + src_ext
            corresponding_abs = os.path.normpath(os.path.abspath(corresponding))
            for allowed in ALLOWED_PATHS:
                allowed_abs = os.path.normpath(os.path.abspath(allowed))
                if corresponding_abs == allowed_abs or os.path.basename(corresponding_abs).lower() == os.path.basename(allowed_abs).lower():
                    return True
        return False
    return False







# node_filters.py
import clang.cindex
import os
import logging

def is_class(node):
    return node.kind in [clang.cindex.CursorKind.CLASS_DECL]

def is_struct(node):
    return node.kind in [clang.cindex.CursorKind.STRUCT_DECL]

def is_function(node):
    return node.kind in [clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.CXX_METHOD, clang.cindex.CursorKind.FUNCTION_DECL]

def is_namespace(node):
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

def is_allowed_node(node, ALLOWED_PATHS):
    """
    Retourne True si le nœud appartient à l'un des fichiers autorisés.
    Si le nœud n'a pas de localisation (par exemple la racine), on le considère autorisé.
    Pour plus de flexibilité, si le basename (nom du fichier) du nœud correspond à celui
    d'un chemin autorisé, on accepte également.
    Si le nœud appartient à un fichier d'en-tête, il est autorisé si le fichier source
    correspondant est autorisé.
    """
    logging.debug(f"ALLOWED_PATHS={ALLOWED_PATHS}")
    if node.location and node.location.file:
        # Normalisation du chemin absolu du fichier du nœud
        file_path = os.path.normpath(os.path.abspath(node.location.file.name))
        base_name = os.path.basename(file_path)
        for allowed in ALLOWED_PATHS:
            # Normalisation du chemin absolu autorisé
            allowed_abs = os.path.normpath(os.path.abspath(allowed))
            allowed_base_name = os.path.basename(allowed_abs)
            # Option stricte : le chemin complet correspond ou est dans le même répertoire
            if file_path == allowed_abs or file_path.startswith(os.path.dirname(allowed_abs)):
                return True
            # Option plus flexible : le nom du fichier correspond (pour gérer les cas src/../Include)
            if base_name == allowed_base_name:
                return True
            # Vérification du fichier source correspondant pour les fichiers d'en-tête
            if file_path.endswith('.h'):
                corresponding_source = file_path.replace('.h', '.cpp')
                corresponding_source_base_name = os.path.basename(corresponding_source)
                if corresponding_source_base_name == allowed_base_name:
                    return True
                # Option pour d'autres extensions de fichiers source
                corresponding_source = file_path.replace('.h', '.c')
                corresponding_source_base_name = os.path.basename(corresponding_source)
                if corresponding_source_base_name == allowed_base_name:
                    return True
        return False
    return True


# debug_util.py
import logging
from .node_filters import is_allowed_node

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def print_ast(node, ALLOWED_PATHS, depth=0, file=None):
    """
    Parcourt récursivement l'AST et écrit chaque nœud dans le fichier passé en argument.
    """
    indent = "  " * depth
    # Récupérer la ligne (si disponible)
    location = node.location if node.location else "N/A"

    new_node = "None"

    if node.referenced: 
            new_node = node.referenced.get_definition()
            if new_node is None:
                try :
                    new_node = node.referenced.get_declaration()
                except : 
                    pass
    ref = ""
    args = ""
    try:
        ref_kind = node.referenced.kind
        ref_node = node.referenced
        location2 = ref_node.location if ref_node.location else "N/A"
        ref = f"<Kind: {ref_node.kind}| Spelling: {ref_node.displayname} | Location: {location2}>"
    except :
        pass

    try:
        args = node.get_arguments()
        params = []
        for arg in node.get_arguments():
            param_type = arg.type.spelling
            param_name = arg.spelling
            params.append(f"{param_type} {param_name}" if param_name else param_type)
        args = ', '.join(params)
    except:
        pass
                
    # Construire la chaîne à écrire pour ce nœud
    file.write(f"{indent}Kind: {node.kind} {args} | Is allowed {is_allowed_node(node, ALLOWED_PATHS)} | Spelling: {node.displayname} | Is Ref {ref} | Location: {location}\n")
    
    # Parcourir les enfants du nœud
    for child in node.get_children():
        print_ast(child, ALLOWED_PATHS, depth + 1, file)

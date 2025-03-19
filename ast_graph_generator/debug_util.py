# debug_util.py
import logging

def setup_logging(level=logging.DEBUG):
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def print_ast(node, depth=0, file=None):
    """
    Parcourt récursivement l'AST et écrit chaque nœud dans le fichier passé en argument.
    """
    indent = "  " * depth
    # Récupérer la ligne (si disponible)
    line = node.location.line if node.location and node.location.file else "N/A"
    # Construire la chaîne à écrire pour ce nœud
    file.write(f"{indent}{node.kind} {node.spelling} [line: {line}]\n")
    
    # Parcourir les enfants du nœud
    for child in node.get_children():
        print_ast(child, depth + 1, file)

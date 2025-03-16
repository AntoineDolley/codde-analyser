# main.py
import argparse
import clang.cindex
import logging
from debug_util import setup_logging
from utils import setup_for_os
from graph_postprocessing import merge_duplicate_nodes
from ast_parser import parse_source, get_root_cursor
from graph_builder import build_graph_from_ast
from exporter import export_to_gml, export_to_graphml

def main():
    parser = argparse.ArgumentParser(description="Parser l'AST d'un fichier source et l'exporter en format graphique.")
    parser.add_argument('--source', required=True, help="Chemin vers le fichier source à analyser")
    parser.add_argument('--export', choices=['gml', 'graphml'], default='graphml', help="Format d'export")
    parser.add_argument('--output', default="graph_output", help="Nom de base du fichier de sortie (sans extension)")
    parser.add_argument('--includes', nargs='+', default=[], help="Les includes nécessaires à la compilation du fichier")
    args = parser.parse_args()

    setup_logging()  # Initialisation du logging en mode DEBUG
    logging.debug("Démarrage du programme en mode DEBUG")

    #library_paths = setup_for_os()

    library_paths = []

    ALLOWED_PATHS = args.includes.copy()
    ALLOWED_PATHS.append(args.source) 

    logging.debug(f"ALLOWED_PATHS={ALLOWED_PATHS}")

    tu = parse_source(args.source, args.includes, library_paths)

    root = get_root_cursor(tu)

    graph = build_graph_from_ast(root, ALLOWED_PATHS)

    graph = merge_duplicate_nodes(graph)

    if args.export == 'gml':
        export_to_gml(graph, args.output + ".gml")
    else:
        export_to_graphml(graph, args.output + ".graphml")

    logging.debug(f"Export effectué vers {args.output}.{args.export}")

if __name__ == "__main__":
    main()

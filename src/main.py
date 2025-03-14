import argparse
import clang.cindex
from utils import setup_for_os
from ast_parser import parse_source, get_root_cursor
from graph_builder import build_graph_from_ast
from exporter import export_to_gml, export_to_graphml

def print_nodes(node, indent=0):
    # Affichage des informations du n\u0153ud
    print(' ' * indent + f'Kind: {node.kind}, Spelling: {node.spelling}, Location: {node.location}')

    # Parcourir les enfants du n\u0153ud
    for child in node.get_children():
        print_nodes(child, indent + 2)

def main():
    parser = argparse.ArgumentParser(description="Parser l'AST d'un fichier source et l'exporter en format graphique.")
    parser.add_argument('--source', required=True, help="Chemin vers le fichier source à analyser")
    parser.add_argument('--export', choices=['gml', 'graphml'], default='graphml', help="Format d'export")
    parser.add_argument('--output', default="graph_output", help="Nom de base du fichier de sortie (sans extension)")
    parser.add_argument('--includes', default=[], help="Les includes nécessaires a la compilation du fihicer")
    args = parser.parse_args()

    print(args.includes)

    library_paths = setup_for_os()

    include_paths = [args.includes]

    tu = parse_source(args.source, include_paths, library_paths)

    root = get_root_cursor(tu)

    print_nodes(root)

    graph = build_graph_from_ast(root)

    if args.export == 'gml':
        export_to_gml(graph, args.output + ".gml")
    else:
        export_to_graphml(graph, args.output + ".graphml")

    print(f"Export effectué vers {args.output}.{args.export}")

if __name__ == "__main__":
    main()

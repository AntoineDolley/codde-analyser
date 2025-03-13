import argparse
import clang.cindex
from ast_parser import parse_source, get_root_cursor
from graph_builder import build_graph_from_ast
from exporter import export_to_gml, export_to_graphml

def main():
    parser = argparse.ArgumentParser(description="Parser l'AST d'un fichier source et l'exporter en format graphique.")
    parser.add_argument('--source', required=True, help="Chemin vers le fichier source à analyser")
    parser.add_argument('--export', choices=['gml', 'graphml'], default='graphml', help="Format d'export")
    parser.add_argument('--output', default="graph_output", help="Nom de base du fichier de sortie (sans extension)")
    args = parser.parse_args()

    # Configurez clang si nécessaire, par exemple :
    # clang.cindex.Config.set_library_file("chemin/vers/libclang.so")

    tu = parse_source(args.source)
    root = get_root_cursor(tu)
    graph = build_graph_from_ast(root)

    if args.export == 'gml':
        export_to_gml(graph, args.output + ".gml")
    else:
        export_to_graphml(graph, args.output + ".graphml")

    print(f"Export effectué vers {args.output}.{args.export}")

if __name__ == "__main__":
    main()

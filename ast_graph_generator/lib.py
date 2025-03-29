import argparse
import logging
import os
import clang.cindex
from .debug_util import setup_logging, print_ast  # Assurez-vous que print_ast est défini dans debug_util.py
from .utils import setup_for_os
from .graph_postprocessing import merge_duplicate_nodes
from .ast_parser import parse_source, get_root_cursor
from .graph_builder import build_graph_from_ast
from .exporter import export_to_gml, export_to_graphml

def create_ast_graph_from_file_with_args(source_file: str, args: list[str], export_dir: str, out_name = "graph_output"):
    """
    Crée l'AST, construit le graph, effectue le post-traitement, 
    et exporte le graph dans le dossier 'ast_gen'. En mode debug, 
    l'AST est aussi exporté dans 'ast_gen/debug' avec un nom modifié.
    """
    logging.debug("Démarrage de la génération du graph")

    logging.info(f"Génération du graph pour le fichier {source_file}")

    ALLOWED_PATHS = [source_file]
    logging.debug(f"ALLOWED_PATHS={ALLOWED_PATHS}")

    args = ["-std=c++11"] + args
    logging.info(f"args={args}")

    # Parsing du fichier source pour obtenir l'AST
    index = clang.cindex.Index.create()
    tu = index.parse(source_file, args = args)
    root = get_root_cursor(tu)

    # Si mode debug, écrire l'AST dans le dossier ast_gen/debug/
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        debug_dir = os.path.join(export_dir, "ast_gen", "debug")
        os.makedirs(debug_dir, exist_ok=True)
        # Remplacer les "/" et "\" par des "_" pour créer un nom de fichier valide
        debug_file_name = source_file.replace("/", "#").replace("\\", "#")
        ast_file_path = os.path.join(debug_dir, debug_file_name)
        with open(ast_file_path, "w") as ast_file:
            print_ast(root, ALLOWED_PATHS, depth=0, file=ast_file)
        logging.debug(f"L'AST a été écrit dans {ast_file_path}")

    # Construction et post-traitement du graph
    graph = build_graph_from_ast(root, ALLOWED_PATHS)
    #graph = merge_duplicate_nodes(graph)

    # Exporter le graph dans le dossier ast_gen/
    
    os.makedirs(export_dir, exist_ok=True)
    try:
        graph_file_path = os.path.join(export_dir, out_name + ".graphml")
        export_to_graphml(graph, graph_file_path)
    except : 
        #si le nom de fichier a créer trop grand
        curr_dir = os.getcwd()
        os.chdir(export_dir)
        graph_file_path = os.path.join(out_name + ".graphml")
        export_to_graphml(graph, graph_file_path)
        os.chdir(curr_dir)


    logging.info(f"Graph exporté vers {graph_file_path}")

def create_ast_graph_from_file(source_file: str, include_paths: list[str], library_paths: list[str]):
    """
    Crée l'AST, construit le graph, effectue le post-traitement, 
    et exporte le graph dans le dossier 'ast_gen'. En mode debug, 
    l'AST est aussi exporté dans 'ast_gen/debug' avec un nom modifié.
    """
    logging.debug("Démarrage de la génération du graph")

    logging.info(f"Génération du graph pour le fichier {source_file}")

    ALLOWED_PATHS = include_paths.copy()
    ALLOWED_PATHS.append(source_file)
    logging.debug(f"ALLOWED_PATHS={ALLOWED_PATHS}")

    # Parsing du fichier source pour obtenir l'AST
    tu = parse_source(source_file, include_paths, library_paths)
    root = get_root_cursor(tu)

    # Si mode debug, écrire l'AST dans le dossier ast_gen/debug/
    if logging.getLogger().getEffectiveLevel() == logging.DEBUG:
        debug_dir = os.path.join("ast_gen", "debug")
        os.makedirs(debug_dir, exist_ok=True)
        # Remplacer les "/" et "\" par des "_" pour créer un nom de fichier valide
        debug_file_name = source_file.replace("/", "_").replace("\\", "_")
        ast_file_path = os.path.join(debug_dir, debug_file_name)
        with open(ast_file_path, "w") as ast_file:
            print_ast(root, file=ast_file)
        logging.debug(f"L'AST a été écrit dans {ast_file_path}")

    # Construction et post-traitement du graph
    graph = build_graph_from_ast(root, ALLOWED_PATHS)
    graph = merge_duplicate_nodes(graph)

    # Exporter le graph dans le dossier ast_gen/
    export_dir = "ast_gen"
    os.makedirs(export_dir, exist_ok=True)
    return graph

def main():
    parser = argparse.ArgumentParser(
        description="Parser l'AST d'un fichier source et l'exporter en format graphique (lib.py)."
    )
    parser.add_argument('--source', required=True, help="Chemin vers le fichier source à analyser")
    parser.add_argument('--export', choices=['gml', 'graphml'], default='graphml', help="Format d'export")
    parser.add_argument('--output', default="graph_output", help="Nom de base du fichier de sortie (sans extension)")
    parser.add_argument('--includes', nargs='+', default=[], help="Les includes nécessaires à la compilation du fichier")
    parser.add_argument('--libraries', nargs='+', default=[], help="Les librairies nécessaires à la compilation du fichier")
    parser.add_argument('--debug', action='store_true', help="Active le mode debug avec des logs détaillés")
    args = parser.parse_args()

    # Définir le niveau de logging en fonction de l'option --debug
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(log_level)
    logging.debug("Démarrage du programme en mode DEBUG (lib.py)")

    # Configuration de libclang (adapter le chemin à votre système)
    libclang_path = "/usr/lib64/libclang.so.18.1.8"
    clang.cindex.Config.set_library_file(libclang_path)

    # Parsing du fichier source pour obtenir l'AST et construire le graph
    graph = create_ast_graph_from_file(args.source, args.includes, args.libraries)

    # Exporter le graph dans le dossier ast_gen/
    export_dir = "ast_gen"
    os.makedirs(export_dir, exist_ok=True)
    if args.export == 'gml':
        graph_file_path = os.path.join(export_dir, args.output + ".gml")
        export_to_gml(graph, graph_file_path)
    else:
        graph_file_path = os.path.join(export_dir, args.output + ".graphml")
        export_to_graphml(graph, graph_file_path)

    logging.info(f"Graph exporté vers {graph_file_path}")

if __name__ == "__main__":
    main()

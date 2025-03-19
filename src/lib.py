import argparse
import clang.cindex
import logging
from .debug_util import setup_logging
from .utils import setup_for_os
from .graph_postprocessing import merge_duplicate_nodes
from .ast_parser import parse_source, get_root_cursor
from .graph_builder import build_graph_from_ast
from .exporter import export_to_gml, export_to_graphml
from .ontologie import Entity, FunctionEntity,FunctionCallEntity, TypeRefEntity

def create_ast_graph_from_file(source_file: str, export_format: str, export_file_name: str, include_paths: list[str], library_paths: list[str]):
    setup_logging()  # Initialisation du logging en mode DEBUG
    logging.debug("Démarrage du programme en mode DEBUG")

    ALLOWED_PATHS = []#include_paths.copy()
    ALLOWED_PATHS.append(source_file) 

    logging.debug(f"ALLOWED_PATHS={ALLOWED_PATHS}")

    tu = parse_source(source_file, include_paths, library_paths)

    root = get_root_cursor(tu)

    graph = build_graph_from_ast(root, ALLOWED_PATHS)

    graph = merge_duplicate_nodes(graph)

    if export_format == 'gml':
        export_to_gml(graph, export_file_name + ".gml")
    else:
        export_to_graphml(graph, export_file_name + ".graphml")

    logging.debug(f"Export effectué vers {export_file_name}.{export_format}")

if __name__ == "__main__":
    main()

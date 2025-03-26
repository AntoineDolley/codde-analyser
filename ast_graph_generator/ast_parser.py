# ast_parser.py
import clang.cindex
import logging

def parse_source(source_path: str, include_paths, library_paths) -> clang.cindex.TranslationUnit:
    """
    Parse le fichier source et retourne l'unité de traduction (AST)
    """
    includes = ['-I' + path for path in include_paths]

    std_libraries = ["-std=c++11"]

    library_paths = ['-L' + path for path in include_paths]

    args = includes + library_paths + std_libraries

    logging.info(f"args={args}")

    index = clang.cindex.Index.create()
    translation_unit = index.parse(source_path, args = args)
    return translation_unit

def get_root_cursor(translation_unit: clang.cindex.TranslationUnit) -> clang.cindex.Cursor:
    """
    Retourne le noeud racine de l'AST
    """
    return translation_unit.cursor

def parse_source_agrs(source_path: str, list_args) -> clang.cindex.TranslationUnit:
    """
    Parse le fichier source et retourne l'unité de traduction (AST)
    """

    std_libraries = ["-std=c++11"]

    args = std_libraries + list_args

    logging.info(f"args={args}")

    index = clang.cindex.Index.create()
    translation_unit = index.parse(source_path, args = args)
    return translation_unit

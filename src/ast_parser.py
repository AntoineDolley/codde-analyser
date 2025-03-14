import clang.cindex

def parse_source(source_path: str, include_paths, library_paths) -> clang.cindex.TranslationUnit:
    """
    Parse le fichier source et retourne l'unité de traduction (AST)
    """
    includes = ['-I' + path for path in include_paths]

    libraries = ['-l' + lib for lib in library_paths]

    args = includes + libraries

    print(f"args{args}")

    index = clang.cindex.Index.create()
    translation_unit = index.parse(source_path, args = args)
    return translation_unit

def get_root_cursor(translation_unit: clang.cindex.TranslationUnit) -> clang.cindex.Cursor:
    """
    Retourne le noeud racine de l'AST
    """
    return translation_unit.cursor

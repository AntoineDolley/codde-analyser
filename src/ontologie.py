from dataclasses import dataclass, field
from typing import Optional
import clang.cindex

@dataclass
class Entity:
    name: str = field(init=False)
    decl_file: Optional[str] = field(init=False)
    decl_file_row: int = field(init=False)
    decl_file_column: int = field(init=False)
    namespace_position: Optional[str] = field(init=False)

    def __init__(self, node: clang.cindex.Cursor):
        """
        Initialise l'entité à partir d'un node de l'AST.
        Extraction automatique du nom, fichier, ligne, colonne et position dans le namespace.
        """
        self.name = node.spelling

        # Extraction des informations de localisation
        file = node.location.file
        self.decl_file = file.name if file else None
        self.decl_file_row = node.location.line
        self.decl_file_column = node.location.column

        # Construction de la hiérarchie du namespace
        self.namespace_position = self._build_namespace_position(node)

    def _build_namespace_position(self, node: clang.cindex.Cursor) -> Optional[str]:
        """
        Parcourt les parents du node pour reconstituer la position dans la hiérarchie
        des namespaces et classes (ex: Namespace::Class::...).
        """
        parts = []
        parent = node.semantic_parent

        # On parcourt jusqu'au niveau de translation unit pour construire le chemin complet
        while parent and parent.kind != clang.cindex.CursorKind.TRANSLATION_UNIT:
            if parent.kind in [
                clang.cindex.CursorKind.NAMESPACE, 
                clang.cindex.CursorKind.CLASS_DECL, 
                clang.cindex.CursorKind.STRUCT_DECL
            ]:
                # On insère en début de liste pour avoir l'ordre hiérarchique
                parts.insert(0, parent.spelling)
            parent = parent.semantic_parent

        return "::".join(parts) if parts else None
    
@dataclass
class FunctionEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(node)
        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(node)
        # On remplace le nom par la signature complète
        self.name = signature
    
def get_function_signature(node: clang.cindex.Cursor) -> str:
    """
    Construit la signature complète d'une fonction, incluant son nom et ses paramètres.
    Exemple : "maFonction(int a, float b)"
    """
    if node.kind not in [clang.cindex.CursorKind.FUNCTION_DECL,
                         clang.cindex.CursorKind.CXX_METHOD,
                         clang.cindex.CursorKind.CONSTRUCTOR]:
        return node.spelling

    func_name = node.spelling
    params = []
    for arg in node.get_arguments():
        param_type = arg.type.spelling
        param_name = arg.spelling
        params.append(f"{param_type} {param_name}" if param_name else param_type)
    signature = f"{func_name}({', '.join(params)})"
    return signature
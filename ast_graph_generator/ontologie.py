# ontologie.py
from dataclasses import dataclass, field
from .utils import get_correct_path
import networkx as nx
from typing import Optional
import clang.cindex
import os

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

        # Extraction des informations de localisation
        self.decl_file_row = node.location.line if node.location else "Decl file non trouvée"
        self.decl_file_column = node.location.column if node.location else "Decl file non trouvée"

        file = node.location.file

        if file :
            # self.decl_file = os.path.normpath(file.name)
            self.decl_file = get_correct_path(os.path.normpath(file.name))

        elif self.decl_file_row == 0 and (file is None) : 
            # En general quand le file n'est par trouvé c'est prsq le node est le root du fichier
            # self.decl_file = node.spelling
            self.decl_file = get_correct_path(node.spelling)
            
        else : 
            self.decl_file = 'Decl_file non trouvée'

        self.name = node.spelling

        # Construction de la hiérarchie du namespace
        self.namespace_position = self._build_namespace_position(node)
        
        if '::' in self.name :
            self.name = self.name.split('::')[-1]

        #if self.decl_file != self.name: # Si on est sur le root pour eviter file.cpp#file.cpp
        self.name = f"{self.decl_file}#{self.namespace_position}"

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

        if parts :
            namespace_position = f"{'::'.join(parts)}::{self.name}"
        else :
            namespace_position = self.name

        namespace_position = namespace_position.split('class ')[-1]

        return namespace_position

    def add_to_graph(self, graph: nx.DiGraph, node_type):
        """
        Ajoute L'entitée au graph, avec tout ses attributs
        """
        graph.add_node(
            self.name,
            label = self.name, 
            declaration_file = self.decl_file, 
            declaration_file_row = self.decl_file_row,
            declaration_file_column = self.decl_file_column,
            namespace_position = self.namespace_position,
            node_type = node_type
            )
    
@dataclass
class FunctionEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(node)
        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(node)
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(node)
        self.name = f"{self.decl_file}#{self.namespace_position}"
    
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


@dataclass
class FunctionCallEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(node)

        if node.referenced: 
            new_node = node.referenced.get_definition()
            if new_node is None:
                try :
                    new_node = node.referenced.get_declaration()
                    if new_node is None:
                        node = node
                    else : 
                        node = new_node
                except : 
                    #print(f"From func {node.spelling}")
                    pass
            else : 
                node = new_node

        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(node)
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(node)
        self.name = f"{self.decl_file}#{self.namespace_position}"

@dataclass
class TypeRefEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste

        if node.referenced: 
            new_node = node.referenced.get_definition()
            if new_node is None:
                try :
                    new_node = node.referenced.get_declaration()
                    if new_node is None:
                        node = node
                    else : 
                        node = new_node
                except : 
                    #print(f"From Type {node.spelling}")
                    pass
            else : 
                node = new_node


        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(node)
        # On remplace le nom par la signature complète
        self.namespace_position = self.name

@dataclass
class ClassFunctionCallEntity(TypeRefEntity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(node)

        class_node = get_class_node(node)

        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(class_node) # Initialise correctement decl_file row et columns
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(node)
        self.name = f"{self.decl_file}#{self.namespace_position}"


def get_class_node(node):
    if node.kind == clang.cindex.CursorKind.CALL_EXPR:
            for child in node.get_children():
                if child.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                    for sub_child_1 in child.get_children():
                        if sub_child_1.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
                            for sub_child_2 in sub_child_1.referenced.get_definition().get_children():
                                if sub_child_2.kind == clang.cindex.CursorKind.TYPE_REF:
                                    return sub_child_2
    print("N'est pas une fonction d'une custom class", node.spelling)
    return node
                                    
                            

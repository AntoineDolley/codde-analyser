# ontologie/entity.py
import os
import clang.cindex
import networkx as nx
from typing import Optional
from ..utils import get_correct_path
from .node_type_enum import NodeType
from dataclasses import dataclass, field

@dataclass
class Entity:
    name: str = field(init=False)
    decl_file: Optional[str] = field(init=False)
    decl_file_row: int = field(init=False)
    decl_file_column: int = field(init=False)
    namespace_position: Optional[str] = field(init=False)
    node_type: str = field(init=False)

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
        self.node_type = NodeType.GENERIC

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

    def add_to_graph(self, graph: nx.DiGraph):
        """
        Ajoute L'entitée au graph, avec tout ses attributs
        """
        if self.name in graph :
            # si le noeud est deja ddans le graph 
            # pas besion de le reajouter et aussi 
            # on ne veux pas ecraser un attribut node_type
            # par exemple un appel a une fonction qui est declarée dans le meme fichier 
            # replacerai son node type de DECL a CALL ce que l'on de veut pas
            return
        
        graph.add_node(
            self.name,
            label = self.name, 
            declaration_file = self.decl_file, 
            declaration_file_row = self.decl_file_row,
            declaration_file_column = self.decl_file_column,
            namespace_position = self.namespace_position,
            node_type = self.node_type
            )
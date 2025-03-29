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
    start_line: Optional[int] = field(init=False)
    end_line: Optional[int] = field(init=False)
    namespace_position: Optional[str] = field(init=False)
    type: str = field(init=False)
    
    def __init__(self, node: clang.cindex.Cursor):
        """
        Initialise l'entité à partir d'un node de l'AST.
        Extraction automatique du nom, fichier, lignes de début et fin de déclaration, et position dans le namespace.
        """

        # Extraction des informations de localisation via extent pour obtenir la ligne de début et de fin de déclaration
        self.start_line = node.extent.start.line if node.extent and node.extent.start else None
        self.end_line = node.extent.end.line if node.extent and node.extent.end else None

        file = node.location.file if node.location else None
        
        if file:
            self.decl_file = get_correct_path(os.path.normpath(file.name))
        elif self.start_line == 1 and file is None:
            # En général, quand le file n'est pas trouvé c'est parce que le node est le root du fichier
            self.decl_file = get_correct_path(node.spelling)
        else:
            self.decl_file = 'Decl_file non trouvée'
        
        self.name = node.spelling
        # Construction de la hiérarchie du namespace
        self.namespace_position = self._build_namespace_position(node)
        
        if '::' in self.name:
            self.name = self.name.split('::')[-1]
        
        self.name = f"{self.decl_file}#{self.namespace_position}"
        self.type = NodeType.GENERIC.value
    
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
            
        if parts:
            namespace_position = f"{'::'.join(parts)}::{self.name}"
        else:
            namespace_position = self.name
        namespace_position = namespace_position.split('class ')[-1]
        return namespace_position
    
    def add_to_graph(self, graph: nx.DiGraph):
        """
        Ajoute l'entité au graph, avec tous ses attributs.
        Si un attribut est None, il est remplacé par une chaîne de caractères "unknown".
        """
        if self.name in graph:
            # Si le nœud est déjà dans le graph, on ne le réajoute pas
            # pour ne pas écraser un attribut existant, par exemple le type.
            return

        attributes = {
            'label': self.name,
            'declaration_file': self.decl_file if self.decl_file is not None else "unknown",
            'start_line': self.start_line if self.start_line is not None else "unknown",
            'end_line': self.end_line if self.end_line is not None else "unknown",
            'namespace_position': self.namespace_position if self.namespace_position is not None else "unknown",
            'type': self.type if self.type is not None else "unknown"
        }
        graph.add_node(self.name, **attributes)

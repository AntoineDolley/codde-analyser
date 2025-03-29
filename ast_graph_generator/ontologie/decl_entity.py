# ontologie/decl_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType
from .ontologie_utils import get_function_signature


@dataclass
class DeclEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)
        self.type = NodeType.DECL.value

@dataclass
class NamespaceDeclEntity(DeclEntity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)

@dataclass
class ClassDeclEntity(DeclEntity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)

@dataclass
class StrcutDeclEntity(DeclEntity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)

@dataclass
class FunctionDeclEntity(DeclEntity):
    def __init__(self, node: clang.cindex.Cursor):
        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(node)
        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(node)
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(node)
        self.name = f"{self.decl_file}#{self.namespace_position}"
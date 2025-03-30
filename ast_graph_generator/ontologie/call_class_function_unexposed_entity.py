# ontologie/call_class_function_unexposed_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType
from .call_type_ref_entity import TypeRefEntity
from .ontologie_utils import get_function_signature, get_class_node

@dataclass
class UnexposedClassFunctionCallEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):

        func_node = node

        for child in node.get_children():
            if child.kind in [clang.cindex.CursorKind.MEMBER_REF_EXPR] and child.referenced is not None:
                func_node = child.referenced

        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(func_node)

        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(func_node) # Initialise correctement decl_file row et columns
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(func_node)
        self.name = f"{self.decl_file}#{self.namespace_position}"
        self.type = NodeType.CALL.value
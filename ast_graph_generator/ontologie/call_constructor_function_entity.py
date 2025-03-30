# ontologie/call_constructor_function_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType
from .ontologie_utils import get_function_signature, get_class_node

@dataclass
class ConstructorClassFunctionCallEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):

        func_node = node

        for child in node.walk_preorder():
            if child.kind in [clang.cindex.CursorKind.CALL_EXPR] and child.referenced is not None:
                if child.referenced.kind in [clang.cindex.CursorKind.CONSTRUCTOR, clang.cindex.CursorKind.FUNCTION_DECL]:
                    if child.referenced.location:
                        if not child.referenced.location.file.name.startswith("/"):
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

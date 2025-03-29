# ontologie/call_standalone_function.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType
from .ontologie_utils import get_function_signature

@dataclass
class StandaloneFunctionCallEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):

        func_node = node

        if node.referenced is not None: 
            func_node = node.get_definition()

        # On calcule la signature complète avant d'initialiser le reste
        signature = get_function_signature(func_node)

        # Appel à l'initialisation de la classe parente pour récupérer les autres attributs
        super().__init__(func_node)
        # On remplace le nom par la signature complète
        self.name = signature
        self.namespace_position = self._build_namespace_position(func_node)
        self.name = f"{self.decl_file}#{self.namespace_position}"
        self.type = NodeType.CALL.value

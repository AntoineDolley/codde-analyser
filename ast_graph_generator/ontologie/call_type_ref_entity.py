# ontologie/uses_type_ref_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType

@dataclass
class TypeRefEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):

        # On recupère le neud du type custom
        node_ref = node
        if node.referenced is not None: 
            new_node = node.get_definition()
            if new_node is None:
                print("Didint find node Type")
                node_ref = node
            else : 
                node_ref = new_node

        super().__init__(node_ref)
        self.type = NodeType.CALL.value
        # # On remplace le nom par la signature complète
        # self.namespace_position = self.name
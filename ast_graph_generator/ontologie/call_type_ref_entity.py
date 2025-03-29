# ontologie/uses_type_ref_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType

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
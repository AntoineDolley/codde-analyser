# ontologie/call_standalone_function.py
from dataclasses import dataclass
import clang.cindex
from .entity import Entity
from .ontologie_utils import get_function_signature

@dataclass
class StandaloneFunctionCallEntity(Entity):
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

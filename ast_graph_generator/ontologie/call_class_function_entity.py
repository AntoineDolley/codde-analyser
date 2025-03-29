# ontologie/call_class_function_entity.py
from dataclasses import dataclass
import clang.cindex
from .uses_type_ref_entity import TypeRefEntity
from .ontologie_utils import get_function_signature, get_class_node

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
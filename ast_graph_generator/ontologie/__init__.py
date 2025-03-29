# ontologie/__init__.py
from .entity import Entity

# Objet correspondant au debut de file
from .file_entity import FileEntity

# Objets correspondants aux declarations d'entitées
from .decl_entity import NamespaceDeclEntity, ClassDeclEntity, FunctionDeclEntity, StrcutDeclEntity

# Objet correspondant aux utilisation de types custom
from .call_type_ref_entity import TypeRefEntity

# Objet correspondant aux appels de fonctions methodes constructeurs
from .call_standalone_function import StandaloneFunctionCallEntity
from .call_class_function_entity import ClassFunctionCallEntity
from .call_class_function_unexposed_entity import UnexposedClassFunctionCallEntity
from .call_constructor_function_entity import ConstructorClassFunctionCallEntity

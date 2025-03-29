# ontologie/decl_struct_entity.py
from dataclasses import dataclass
import clang.cindex
from .entity import Entity

@dataclass
class StrcutDeclEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)
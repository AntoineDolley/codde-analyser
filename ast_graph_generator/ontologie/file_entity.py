# ontologie/file_entity.py
import clang.cindex
from .entity import Entity
from dataclasses import dataclass
from .node_type_enum import NodeType


@dataclass
class FileEntity(Entity):
    def __init__(self, node: clang.cindex.Cursor):
        super().__init__(node)
        self.node_type = NodeType.FILE.value
        self.name = self.decl_file

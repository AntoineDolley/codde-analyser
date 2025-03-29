# ontologie/node_type_enum.py
from enum import Enum, auto

class NodeType(Enum):
    GENERIC = "Entity"
    DECL = "DECL"
    CALL = "CALL"
    FILE = "FILE"

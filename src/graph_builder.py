import networkx as nx
import clang.cindex
from ontologie import Entity, FunctionEntity
from node_filters import is_class,  is_custom_type, is_function, is_namespace, is_struct

def build_hierarchy_graph(node: clang.cindex.Cursor, graph: nx.DiGraph, parent_node: str = None) -> None:
    """
    Parcours récursif de l'AST pour construire un graphe hiérarchique.
    """
    # Par exemple, gérer les namespaces, classes, fonctions, etc.
    if parent_node is None:
        entity = Entity(node)
        graph.add_node(entity.name, entity=entity)
        parent_node = entity.name

    for child in node.get_children():
        if is_class(child) or is_custom_type(child) or is_function(child) or is_namespace(child) or is_struct(child):
            if is_function(child) : 
                child_entity = FunctionEntity(child)
            else : 
                child_entity = Entity(child)
            graph.add_node(child_entity.name, entity=child_entity)
            # Exemple d'ajout d'une relation, vous pouvez adapter en fonction de votre ontologie
            graph.add_edge(parent_node, child_entity.name, relation=f'contains_{child.kind.name.lower()}')
            build_hierarchy_graph(child, graph, parent_node=child_entity.name)
        else:
            build_hierarchy_graph(child, graph, parent_node)
    
def build_graph_from_ast(root: clang.cindex.Cursor) -> nx.DiGraph:
    """
    Crée et retourne un graphe à partir du noeud racine de l'AST.
    """
    graph = nx.DiGraph()
    build_hierarchy_graph(root, graph)
    return graph

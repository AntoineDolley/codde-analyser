# graph_builder.py
import networkx as nx
import clang.cindex
from .ontologie import Entity, FunctionEntity, FunctionCallEntity, TypeRefEntity, ClassFunctionCallEntity
from .node_filters import is_class,  uses_custom_type, is_function, is_namespace, is_struct, is_custom_type, is_function_call, is_allowed_node, is_class_function_call

def build_hierarchy_graph(node: clang.cindex.Cursor, graph: nx.DiGraph, ALLOWED_PATHS: list[str], parent_node: str = None) -> None:
    """
    Parcours récursif de l'AST pour construire un graphe hiérarchique.
    """
    # Par exemple, gérer les namespaces, classes, fonctions, etc.

    old_parent = parent_node

    if parent_node is None:
        # Si parent node est None cela signifie que le node est le node representant le fichier
        entity = Entity(node)
        node_type = f'{node.kind.name.lower()}'
        entity.add_to_graph(graph, node_type)
        parent_node = entity.name

    for child in node.get_children():
        if child is not None : 
            if not is_allowed_node(child, ALLOWED_PATHS):
                continue

        if is_class(child) or uses_custom_type(child) or is_function(child) or is_namespace(child) or is_struct(child) or is_custom_type(child) or is_function_call(child):

            relation = f'contains_{child.kind.name.lower()}'
            node_type = f'{child.kind.name.lower()}'

            if is_class_function_call(child): # Doit etre mis avant le check is_function()
                print("a trouve un class typeref")
                child_entity = ClassFunctionCallEntity(child)

            elif is_function(child): 
                child_entity = FunctionEntity(child)
                relation = f'contains_fun_decl'

            elif is_function_call(child):
                child_entity = FunctionCallEntity(child)
                relation = f'calls_function'

            elif uses_custom_type(child):
                child_entity = TypeRefEntity(child)
                relation = f'uses_custom_type'

            else : 
                child_entity = Entity(child)
                
            child_entity.add_to_graph(graph, node_type)

            graph.add_edge(parent_node, child_entity.name, relation=relation)

            #Dans le cas ou des fonctions sont appelées a la suite func1().func2() pour eviter qu'une fonction inclue une autre
            if is_function_call(child):
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=old_parent)
            else: 
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=child_entity.name)
        else:
            build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node)
    
def build_graph_from_ast(root: clang.cindex.Cursor, ALLOWED_PATHS: list[str]) -> nx.DiGraph:
    """
    Crée et retourne un graphe à partir du noeud racine de l'AST.
    """
    graph = nx.DiGraph()
    build_hierarchy_graph(root, graph, ALLOWED_PATHS)
    return graph


def print_function_location(call_cursor: clang.cindex.Cursor) -> None:
    """
    Affiche le fichier de déclaration ou de définition de la fonction appelée.
    """
    # Vérifier que le curseur d'appel possède une référence
    if call_cursor.referenced:
        # Essayer d'obtenir le curseur de définition
        func_cursor = call_cursor.referenced.get_definition()
        if func_cursor is None:
            # Si aucune définition n'est trouvée, utiliser la déclaration
            func_cursor = call_cursor.referenced.get_declaration()
        
        if func_cursor is not None and func_cursor.location:
            file = func_cursor.location.file
            if file:
                print("Fichier:", file.name)
            else:
                print("Le fichier de localisation n'est pas disponible.")
        else:
            print("Impossible de récupérer la définition ou la déclaration.")
    else:
        print("Le curseur ne référence pas une entité (fonction) valide.")

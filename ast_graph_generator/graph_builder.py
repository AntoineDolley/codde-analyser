# graph_builder.py
import networkx as nx
import clang.cindex
from .ontologie import *
from .node_filters import *

def build_graph_from_ast(root: clang.cindex.Cursor, ALLOWED_PATHS: list[str]) -> nx.DiGraph:
    """
    Crée et retourne un graphe à partir du noeud racine de l'AST.
    """
    graph = nx.DiGraph()
    build_hierarchy_graph(root, graph, ALLOWED_PATHS)
    return graph

def build_hierarchy_graph(node: clang.cindex.Cursor, graph: nx.DiGraph, ALLOWED_PATHS: list[str], parent_node: str = None) -> None:
    """
    Parcours récursif de l'AST pour construire un graphe hiérarchique.
    """
    # Par exemple, gérer les namespaces, classes, fonctions, etc.

    old_parent = parent_node

    if parent_node is None:
        # Si parent node est None cela signifie que le node est le node representant le fichier
        entity = FileEntity(node)
        node_type = f'{node.kind.name.lower()}'
        entity.add_to_graph(graph, node_type)
        parent_node = entity.name

    for child in node.get_children():
        if child is not None : 
            if not is_allowed_node(child, ALLOWED_PATHS):
                continue

        if is_in_ontologie(child):

            relation = f'contains_{child.kind.name.lower()}'
            node_type = f'{child.kind.name.lower()}'

            # =================================
            # Parsing des noeuds des references
            # =================================

            if is_standalone_function_call(child):
                print("a trouve un standalone_function_call", node.spelling)
                child_entity = StandaloneFunctionCallEntity(child)
                relation = f'calls_function'

            elif is_class_function_call(child):
                print("a trouve un class typeref", node.spelling)
                child_entity = ClassFunctionCallEntity(child)
                relation = f'calls_class_function'

            elif is_class_function_call_unxeposed(child):
                print("a trouve un class_function_call_unxeposed", node.spelling)
                child_entity = UnexposedClassFunctionCallEntity(child)
                relation = f'calls_class_function'

            elif is_constructor_call(child):
                #Correspond a un constructeur
                print("found constructeur",type(child.spelling))
                child_entity = ConstructorClassFunctionCallEntity(child)
                relation = f'calls_class_constructor'
                
            elif uses_custom_type(child):
                child_entity = TypeRefEntity(child)
                relation = f'calls_custom_type'

            # =================================
            # Parsing des noeuds de declaration
            # =================================

            elif is_namespace_decl(child):
                child_entity = NamespaceDeclEntity(child)
                relation = f'contains_namespace_decl'
            
            elif is_class_decl(child):
                child_entity = ClassDeclEntity(child)
                relation = f'contains_class_decl'

            elif is_function_decl(child): 
                print(child.spelling)
                child_entity = FunctionDeclEntity(child)
                relation = f'contains_fun_decl'
            
            elif is_struct_decl(child): 
                print(child.spelling)
                child_entity = StrcutDeclEntity(child)
                relation = f'contains_struct_decl'

            else : 
                print("Noeud passe les tests de types mais non parsé", node.spelling, node.location.file)
                child_entity = Entity(child)
                
            child_entity.add_to_graph(graph, node_type)

            graph.add_edge(parent_node, child_entity.name, relation=relation)

            #Dans le cas ou des fonctions sont appelées a la suite func1().func2() pour eviter qu'une fonction inclue une autre
            if is_standalone_function_call(child):
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=old_parent)
            else: 
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=child_entity.name)
        else:
            build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node)

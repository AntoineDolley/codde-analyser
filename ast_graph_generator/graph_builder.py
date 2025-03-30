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
        entity.add_to_graph(graph)
        parent_node = entity.name

    for child in node.get_children():
        if child is not None : 
            if not is_allowed_node(child, ALLOWED_PATHS):
                continue

        if is_in_ontologie(child):

            relation = f'contains_{child.kind.name.lower()}'

            # =================================
            # Parsing des noeuds des references
            # =================================

            is_header = is_allowed_header_node(child, ALLOWED_PATHS)
            is_source = is_allowed_source_node(child, ALLOWED_PATHS)

            if is_standalone_function_call(child) and is_source and not is_header:
                child_entity = StandaloneFunctionCallEntity(child)
                relation = f'calls_function'

            elif is_class_function_call(child) and is_source and not is_header:
                child_entity = ClassFunctionCallEntity(child)
                relation = f'calls_class_function'

            elif is_class_function_call_unxeposed(child) and is_source and not is_header:
                child_entity = UnexposedClassFunctionCallEntity(child)
                relation = f'calls_class_function'

            elif is_constructor_call(child) and is_source and not is_header:
                #Correspond a un constructeur
                child_entity = ConstructorClassFunctionCallEntity(child)
                relation = f'calls_class_constructor'
                
            elif uses_custom_type(child) and is_source and not is_header:
                child_entity = TypeRefEntity(child)
                relation = f'calls_custom_type'

            # =================================
            # Parsing des noeuds de declaration
            # =================================

            elif is_namespace_decl(child) and is_header and not is_source:
                child_entity = NamespaceDeclEntity(child)
                relation = f'contains_namespace_decl'
            
            elif is_class_decl(child) and is_header and not is_source:
                child_entity = ClassDeclEntity(child)
                relation = f'contains_class_decl'

            elif is_function_decl(child) and (is_header or is_source): 
                child_entity = FunctionDeclEntity(child)
                relation = f'contains_fun_decl'
            
            elif is_struct_decl(child) and is_header and not is_source: 
                child_entity = StrcutDeclEntity(child)
                relation = f'contains_struct_decl'

            else : 
                print("Noeud passe les tests de types mais non parsé", node.spelling, node.location.file)
                child_entity = Entity(child)
                
            child_entity.add_to_graph(graph)

            graph.add_edge(parent_node, child_entity.name, relation=relation)

            #Dans le cas ou des fonctions sont appelées a la suite func1().func2() pour eviter qu'une fonction inclue une autre
            if is_standalone_function_call(child):
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=old_parent)
            else: 
                build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=child_entity.name)
        else:
            # si le noeud ne nous interesse pas le lien est passé au noeudds en dessous
            build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node)

# def build_hierarchy_graph(node: clang.cindex.Cursor, graph: nx.DiGraph, ALLOWED_PATHS: list[str], parent_node: str = None) -> None:
#     """
#     Parcours récursif de l'AST pour construire un graphe hiérarchique.
#     """
#     # Par exemple, gérer les namespaces, classes, fonctions, etc.

#     old_parent = parent_node

#     if parent_node is None:
#         # Si parent node est None cela signifie que le node est le node representant le fichier
#         entity = FileEntity(node)
#         node_type = f'{node.kind.name.lower()}'
#         entity.add_to_graph(graph)
#         parent_node = entity.name

#     for child in node.get_children():
#         if child is not None : 
#             if not is_allowed_node(child, ALLOWED_PATHS):
#                 continue
#         if is_allowed_header_node(child, ALLOWED_PATHS):
#             if is_decl(child):

#                 relation = f'contains_{child.kind.name.lower()}'

#                 # =================================
#                 # Parsing des noeuds de declaration
#                 # =================================

#                 if is_namespace_decl(child):
#                     child_entity = NamespaceDeclEntity(child)
#                     relation = f'contains_namespace_decl'
                
#                 elif is_class_decl(child):
#                     child_entity = ClassDeclEntity(child)
#                     relation = f'contains_class_decl'

#                 elif is_function_decl(child): 
#                     child_entity = FunctionDeclEntity(child)
#                     relation = f'contains_fun_decl'
                
#                 elif is_struct_decl(child): 
#                     child_entity = StrcutDeclEntity(child)
#                     relation = f'contains_struct_decl'

#                 else : 
#                     print("Noeud passe les tests de types mais non parsé", node.spelling, node.location.file)
#                     child_entity = Entity(child)
                    
#                 child_entity.add_to_graph(graph)

#                 graph.add_edge(parent_node, child_entity.name, relation=relation)

#         elif is_allowed_source_node(child, ALLOWED_PATHS):
#             if is_call(child):
#                 relation = f'contains_{child.kind.name.lower()}'

#                 # =================================
#                 # Parsing des noeuds des references
#                 # =================================

#                 if is_standalone_function_call(child):
#                     child_entity = StandaloneFunctionCallEntity(child)
#                     relation = f'calls_function'

#                 elif is_class_function_call(child):
#                     child_entity = ClassFunctionCallEntity(child)
#                     relation = f'calls_class_function'

#                 elif is_class_function_call_unxeposed(child):
#                     child_entity = UnexposedClassFunctionCallEntity(child)
#                     relation = f'calls_class_function'

#                 elif is_constructor_call(child):
#                     #Correspond a un constructeur
#                     child_entity = ConstructorClassFunctionCallEntity(child)
#                     relation = f'calls_class_constructor'
                    
#                 elif uses_custom_type(child):
#                     child_entity = TypeRefEntity(child)
#                     relation = f'calls_custom_type'

#                 # =================================
#                 # Parsing des noeuds de declaration
#                 # =================================

#                 elif is_function_decl(child): 
#                     child_entity = FunctionDeclEntity(child)
#                     relation = f'contains_fun_decl'
#                 else : 
#                     print("Noeud passe les tests de types mais non parsé", node.spelling, node.location.file)
#                     child_entity = Entity(child)
                    
#                 child_entity.add_to_graph(graph)

#                 if not is_function_decl(child): 
#                     # on ajoute un relation seulement si le noeud 
#                     # n'est pas une decl pour eviter de tout coller au file_node
#                     graph.add_edge(parent_node, child_entity.name, relation=relation)

#                 #Dans le cas ou des fonctions sont appelées a la suite func1().func2() pour eviter qu'une fonction inclue une autre
#                 if is_standalone_function_call(child):
#                     build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=old_parent)
#                 else: 
#                     build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node=child_entity.name)
#         else:
#             # si le noeud ne nous interesse pas le lien est passé au noeudds en dessous
#             build_hierarchy_graph(child, graph, ALLOWED_PATHS, parent_node) 
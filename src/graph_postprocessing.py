# graph_postprocessing.py
import networkx as nx

def merge_duplicate_nodes(graph: nx.DiGraph) -> nx.DiGraph:
    """
    Fusionne les nœuds du graphe qui partagent le même 'namespace_position'.
    Pour chaque groupe de doublons, le nœud dont le fichier de déclaration se termine par ".cpp"
    est privilégié. On redirige ensuite les arêtes vers ce nœud canonique avant de supprimer les doublons.
    """
    # Regrouper les nœuds par 'namespace_position'
    groups = {}
    for node in list(graph.nodes):
        canonical_key = graph.nodes[node].get("namespace_position", node)
        groups.setdefault(canonical_key, []).append(node)
    
    nodes_to_remove = set()
    
    for key, nodes in groups.items():
        if len(nodes) < 2:
            continue  # Pas de doublon dans ce groupe

        # Choisir le nœud canonique : celui dont le fichier de déclaration se termine par ".cpp", sinon le premier
        canonical_node = None
        for node in nodes:
            file_attr = graph.nodes[node].get("declration_file", "")
            if file_attr.endswith(".cpp"):
                canonical_node = node
                break
        if canonical_node is None:
            canonical_node = nodes[0]
        
        # Fusionner les autres nœuds dans le nœud canonique
        for node in nodes:
            if node == canonical_node:
                continue
            # Rediriger les arêtes entrantes du nœud à fusionner vers le nœud canonique
            for pred, _, data in list(graph.in_edges(node, data=True)):
                if pred != canonical_node and not graph.has_edge(pred, canonical_node):
                    graph.add_edge(pred, canonical_node, **data)
            # Rediriger les arêtes sortantes du nœud à fusionner depuis le nœud canonique
            for _, succ, data in list(graph.out_edges(node, data=True)):
                if succ != canonical_node and not graph.has_edge(canonical_node, succ):
                    graph.add_edge(canonical_node, succ, **data)
            nodes_to_remove.add(node)
    
    graph.remove_nodes_from(nodes_to_remove)
    return graph

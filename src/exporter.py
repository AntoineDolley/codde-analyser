import networkx as nx

def export_to_gml(graph: nx.DiGraph, output_file: str) -> None:
    nx.write_gml(graph, output_file)

def export_to_graphml(graph: nx.DiGraph, output_file: str) -> None:
    nx.write_graphml(graph, output_file)

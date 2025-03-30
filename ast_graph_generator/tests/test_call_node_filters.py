# tests/test_parsing_functions_real.py
import os
import config
import unittest
import clang.cindex
from ast_graph_generator.node_filters import (
    uses_custom_type,
    is_standalone_function_call,
    is_class_function_call,
    is_class_function_call_unxeposed,
    is_constructor_call,
    is_allowed_node
)

def collect_nodes_by_predicate(predicate, root_node, ALLOWED_PATHS):
    """
    Parcourt récursivement l'AST à partir de root_node et renvoie une liste
    de chaînes contenant le type (kind) et le spelling de chaque nœud satisfaisant le prédicat.
    """
    results = []
    for node in root_node.walk_preorder():
        if predicate(node) and is_allowed_node(node, ALLOWED_PATHS):
            results.append(f"Node spelling {node.spelling} Node location file {node.location.file} Node decl start line {node.extent.start.line} Node decl end line {node.extent.end.line}")
    return results

class TestCallParsingFunctionsReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuration de libclang
        libclang_path = config.LIBCLANG_PATH
        clang.cindex.Config.set_library_file(libclang_path)

        # Positionnement dans le dossier des tests
        os.chdir("/home/antoine/Documents/codde-analyser/ast_graph_generator/tests")
        cls.index = clang.cindex.Index.create()
        cls.test_file = "test_files/test_call/Actions.cpp"
        args = ['-std=c++11', '-c', '-I./test_files/test_call']
        cls.ALLOWED_PATHS = [cls.test_file]
        cls.translation_unit = cls.index.parse(cls.test_file, args=args)
    
    def _write_found_nodes(self, test_name, nodes):
        """
        Écrit dans un fichier la liste des nœuds trouvés pour le test donné.
        Le fichier sera créé dans le répertoire des tests.
        """
        output_file = os.path.join(os.path.dirname(__file__), f"{test_name}_found_nodes.txt")
        with open(output_file, "w") as f:
            for n in nodes:
                f.write(n + "\n")
    
    def test_uses_custom_type(self):
        found_nodes = collect_nodes_by_predicate(uses_custom_type, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_uses_custom_type", found_nodes)
        self.assertTrue(len(found_nodes) > 0, "Aucune utilisation de type personnalisé trouvée dans le fichier de test.")
    
    def test_standalone_function_call(self):
        found_nodes = collect_nodes_by_predicate(is_standalone_function_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_standalone_function_call", found_nodes)
        self.assertTrue(len(found_nodes) > 0, "Aucun appel de fonction autonome trouvé dans le fichier de test.")
    
    def test_class_function_call(self):
        found_nodes = collect_nodes_by_predicate(is_class_function_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_class_function_call", found_nodes)
        self.assertTrue(len(found_nodes) > 0, "Aucun appel de fonction de classe trouvé dans le fichier de test.")
    
    def test_class_function_call_unexposed(self):
        found_nodes = collect_nodes_by_predicate(is_class_function_call_unxeposed, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_class_function_call_unexposed", found_nodes)
        self.assertTrue(len(found_nodes) > 0, "Aucun appel de fonction de classe non exposé trouvé dans le fichier de test.")
    
    def test_constructor_call(self):
        found_nodes = collect_nodes_by_predicate(is_constructor_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_constructor_call", found_nodes)
        self.assertTrue(len(found_nodes) > 0, "Aucun appel de constructeur trouvé dans le fichier de test.")

if __name__ == '__main__':
    unittest.main()

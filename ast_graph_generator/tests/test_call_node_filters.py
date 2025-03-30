# tests/test_parsing_functions_real.py
import os
import config
import unittest
import clang.cindex
from ast_graph_generator.debug_util import print_ast
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
    d'objets (dictionnaires) contenant les informations suivantes pour chaque nœud satisfaisant le prédicat :
        - spelling
        - chemin du fichier (location)
        - ligne de début de déclaration
        - ligne de fin de déclaration
    """

    # debug_file = "debug.txt"
    # with open(debug_file, "w") as ast_file:
    #     print_ast(root_node, ALLOWED_PATHS, depth=0, file=ast_file)

    results = []
    for node in root_node.walk_preorder():
        if is_allowed_node(node, ALLOWED_PATHS) and predicate(node):
            node_info = {
                "spelling": node.spelling,
                "file": str(node.location.file),
                "start_line": node.extent.start.line,
                "end_line": node.extent.end.line,
            }
            results.append(node_info)
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
        cls.test_file = "test_files/sep_test/Actions.cpp"
        args = ['-std=c++11', '-c', '-I./test_files/sep_test/']
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
                f.write(str(n) + "\n")
    
    def test_standalone_function_call(self):
        found_nodes = collect_nodes_by_predicate(is_standalone_function_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "displayPersonInfo",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 21,
                "end_line": 21,
            }
        ]
        self.assertEqual(found_nodes, expected, "Les appels de fonction autonome trouvés ne correspondent pas au résultat attendu.")
    
    def test_constructor_call(self):
        found_nodes = collect_nodes_by_predicate(is_constructor_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 19,
                "end_line": 19,
            }
        ]
        self.assertEqual(found_nodes, expected, "Les appels de constructeur trouvés ne correspondent pas au résultat attendu.")

    def test_class_function_call_unexposed(self):
        found_nodes = collect_nodes_by_predicate(is_class_function_call_unxeposed, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_class_function_call_unexposed", found_nodes)
        expected = []  # Aucun nœud ne doit être trouvé pour ce test
        self.assertEqual(found_nodes, expected, "Aucun appel de fonction de classe non exposé ne devrait être trouvé dans le fichier de test.")
    
    def test_class_function_call(self):
        found_nodes = collect_nodes_by_predicate(is_class_function_call, self.translation_unit.cursor, self.ALLOWED_PATHS)
        self._write_found_nodes("test_class_function_call", found_nodes)
        expected = [
            {
                "spelling": "getName",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 7,
                "end_line": 7,
            },
            {
                "spelling": "getAge",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 8,
                "end_line": 8,
            },
            {
                "spelling": "getCompanyName",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 12,
                "end_line": 12,
            },
            {
                "spelling": "setFrom",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 20,
                "end_line": 20,
            },
        ]
        self.assertEqual(found_nodes, expected, "Les appels de fonction de classe trouvés ne correspondent pas au résultat attendu.")

    def test_uses_custom_type(self):
        found_nodes = collect_nodes_by_predicate(uses_custom_type, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.h",
                "start_line": 7,
                "end_line": 7,
            },
            {
                "spelling": "class Entities::Company",
                "file": "test_files/sep_test/Actions.h",
                "start_line": 8,
                "end_line": 8,
            },
            {
                "spelling": "class Entities::Company",
                "file": "test_files/sep_test/Actions.h",
                "start_line": 9,
                "end_line": 9,
            },
            {
                "spelling": "CustomTypes::SizeType",
                "file": "test_files/sep_test/Actions.h",
                "start_line": 9,
                "end_line": 9,
            },
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.h",
                "start_line": 10,
                "end_line": 10,
            },
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 6,
                "end_line": 6,
            },
            {
                "spelling": "class Entities::Company",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 11,
                "end_line": 11,
            },
            {
                "spelling": "class Entities::Company",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 15,
                "end_line": 15,
            },
            {
                "spelling": "CustomTypes::SizeType",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 15,
                "end_line": 15,
            },
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 18,
                "end_line": 18,
            },
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 19,
                "end_line": 19,
            },
            {
                "spelling": "class Entities::Person",
                "file": "test_files/sep_test/Actions.cpp",
                "start_line": 19,
                "end_line": 19,
            },
        ]
        self.assertEqual(found_nodes, expected, "Les utilisations de type personnalisé trouvées ne correspondent pas au résultat attendu.")


if __name__ == '__main__':
    unittest.main()

# tests/test_parsing_functions_real.py
import os
import config
import unittest
import clang.cindex
from ast_graph_generator.node_filters import (
    is_namespace_decl,
    is_class_decl,
    is_function_decl,
    is_custom_type_decl,
    is_allowed_node,
)

def collect_nodes_by_predicate(predicate, root_node, ALLOWED_PATHS):
    """
    Parcourt récursivement l'AST à partir de root_node et renvoie une liste d'objets (dictionnaires)
    contenant les informations suivantes pour chaque nœud satisfaisant le prédicat :
        - spelling
        - chemin du fichier (location)
        - ligne de début de déclaration
        - ligne de fin de déclaration
    """
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

class TestDeclParsingFunctionsReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuration de libclang
        libclang_path = config.LIBCLANG_PATH
        clang.cindex.Config.set_library_file(libclang_path)

        # Positionnement dans le dossier des tests
        os.chdir("/home/antoine/Documents/codde-analyser/ast_graph_generator/tests")
        cls.index = clang.cindex.Index.create()
        cls.test_file = "test_files/test_decl/src/test_code.cpp"
        args = ['-std=c++11', '-c', '-I./test_files/test_decl/Include']
        cls.ALLOWED_PATHS = [cls.test_file]
        cls.translation_unit = cls.index.parse(cls.test_file, args=args)
    
    def test_namespace_decl(self):
        found_nodes = collect_nodes_by_predicate(is_namespace_decl, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "CustomTypes",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 8,
                "end_line": 12,
            },
            {
                "spelling": "Entities",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 14,
                "end_line": 47,
            },
            {
                "spelling": "Actions",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 49,
                "end_line": 54,
            },
            {
                "spelling": "Entities",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 3,
                "end_line": 72,
            },
            {
                "spelling": "Actions",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 74,
                "end_line": 93,
            },
        ]
        # Comparaison des listes d'objets
        self.assertEqual(found_nodes, expected, "Les déclarations de namespace trouvées ne correspondent pas au résultat attendu.")
    
    def test_class_decl(self):
        found_nodes = collect_nodes_by_predicate(is_class_decl, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "Person",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 16,
                "end_line": 30,
            },
            {
                "spelling": "Company",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 32,
                "end_line": 46,
            },
        ]
        self.assertEqual(found_nodes, expected, "Les déclarations de classe trouvées ne correspondent pas au résultat attendu.")
       
    def test_custom_type_decl(self):
        found_nodes = collect_nodes_by_predicate(is_custom_type_decl, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "StringType",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 9,
                "end_line": 9,
            },
            {
                "spelling": "SizeType",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 10,
                "end_line": 10,
            },
            {
                "spelling": "IntegerType",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 11,
                "end_line": 11,
            },
        ]
        self.assertEqual(found_nodes, expected, "Les déclarations de type personnalisé trouvées ne correspondent pas au résultat attendu.")

    def test_function_decl(self):
        found_nodes = collect_nodes_by_predicate(is_function_decl, self.translation_unit.cursor, self.ALLOWED_PATHS)
        expected = [
            {
                "spelling": "Person",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 22,
                "end_line": 22,
            },
            {
                "spelling": "getName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 23,
                "end_line": 23,
            },
            {
                "spelling": "setName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 24,
                "end_line": 24,
            },
            {
                "spelling": "getAge",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 25,
                "end_line": 25,
            },
            {
                "spelling": "setAge",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 26,
                "end_line": 26,
            },
            {
                "spelling": "updateName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 27,
                "end_line": 27,
            },
            {
                "spelling": "updateAge",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 28,
                "end_line": 28,
            },
            {
                "spelling": "setFrom",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 29,
                "end_line": 29,
            },
            {
                "spelling": "Company",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 38,
                "end_line": 38,
            },
            {
                "spelling": "addEmployee",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 39,
                "end_line": 39,
            },
            {
                "spelling": "getCompanyName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 40,
                "end_line": 40,
            },
            {
                "spelling": "getEmployees",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 41,
                "end_line": 41,
            },
            {
                "spelling": "setCompanyName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 42,
                "end_line": 42,
            },
            {
                "spelling": "updateCompanyName",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 43,
                "end_line": 43,
            },
            {
                "spelling": "addEmployeeChain",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 44,
                "end_line": 44,
            },
            {
                "spelling": "setFrom",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 45,
                "end_line": 45,
            },
            {
                "spelling": "displayPersonInfo",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 50,
                "end_line": 50,
            },
            {
                "spelling": "displayCompanyInfo",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 51,
                "end_line": 51,
            },
            {
                "spelling": "displayEmployeeInfo",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 52,
                "end_line": 52,
            },
            {
                "spelling": "initializeAndDisplayPersonInfo",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 53,
                "end_line": 53,
            },
            {
                "spelling": "transformPerson",
                "file": "test_files/test_decl/src/../Include/test_code.h",
                "start_line": 57,
                "end_line": 57,
            },
            {
                "spelling": "Person",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 5,
                "end_line": 6,
            },
            {
                "spelling": "getName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 8,
                "end_line": 10,
            },
            {
                "spelling": "setName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 12,
                "end_line": 14,
            },
            {
                "spelling": "getAge",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 16,
                "end_line": 18,
            },
            {
                "spelling": "setAge",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 20,
                "end_line": 22,
            },
            {
                "spelling": "updateName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 24,
                "end_line": 27,
            },
            {
                "spelling": "updateAge",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 29,
                "end_line": 32,
            },
            {
                "spelling": "setFrom",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 34,
                "end_line": 37,
            },
            {
                "spelling": "Company",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 39,
                "end_line": 40,
            },
            {
                "spelling": "addEmployee",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 42,
                "end_line": 44,
            },
            {
                "spelling": "getCompanyName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 46,
                "end_line": 48,
            },
            {
                "spelling": "getEmployees",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 50,
                "end_line": 52,
            },
            {
                "spelling": "setCompanyName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 54,
                "end_line": 56,
            },
            {
                "spelling": "updateCompanyName",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 58,
                "end_line": 61,
            },
            {
                "spelling": "addEmployeeChain",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 63,
                "end_line": 66,
            },
            {
                "spelling": "setFrom",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 68,
                "end_line": 71,
            },
            {
                "spelling": "displayPersonInfo",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 76,
                "end_line": 78,
            },
            {
                "spelling": "displayCompanyInfo",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 80,
                "end_line": 82,
            },
            {
                "spelling": "displayEmployeeInfo",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 84,
                "end_line": 86,
            },
            {
                "spelling": "initializeAndDisplayPersonInfo",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 88,
                "end_line": 92,
            },
            {
                "spelling": "transformPerson",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 96,
                "end_line": 100,
            },
            {
                "spelling": "main",
                "file": "test_files/test_decl/src/test_code.cpp",
                "start_line": 102,
                "end_line": 113,
            },
        ]
        self.assertEqual(found_nodes, expected, "Les déclarations de fonction trouvées ne correspondent pas au résultat attendu.")
 
if __name__ == '__main__':
    unittest.main()

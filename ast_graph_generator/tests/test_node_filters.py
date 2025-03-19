import os
import unittest
import clang.cindex
from ast_graph_generator.ast_parser import parse_source, get_root_cursor
from ast_graph_generator.node_filters import is_class, is_struct, is_function, is_namespace, is_custom_type

# Si nécessaire, configurer le chemin de la librairie clang (adaptez le chemin à votre environnement)
# clang.cindex.Config.set_library_file('/usr/lib/llvm-10/lib/libclang.so.1')

class TestRealCppEntities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Le dossier sample_code se trouve dans tests/
        cls.test_dir = os.path.join(os.path.dirname(__file__), "sample_code")
    
    def count_nodes(self, cursor, predicate):
        """Fonction récursive pour compter les nodes vérifiant une condition donnée."""
        count = 1 if predicate(cursor) else 0
        for child in cursor.get_children():
            count += self.count_nodes(child, predicate)
        return count

    def test_class_detection(self):
        file_path = os.path.join(self.test_dir, "test_class.cpp")
        tu = parse_source(file_path)
        root = get_root_cursor(tu)
        total_classes = self.count_nodes(root, is_class)
        # Dans test_class.cpp, nous attendons :
        # - MyClass
        # - Outer
        # - Outer::Inner (classe imbriquée)
        # Donc 3 classes au total.
        self.assertEqual(total_classes, 3, f"Nombre de classes incorrect dans {file_path}")

    def test_struct_detection(self):
        file_path = os.path.join(self.test_dir, "test_struct.cpp")
        tu = parse_source(file_path)
        root = get_root_cursor(tu)
        total_structs = self.count_nodes(root, is_struct)
        # Dans test_struct.cpp, nous attendons 3 structs :
        # MyStruct, OuterStruct, OuterStruct::InnerStruct
        self.assertEqual(total_structs, 3, f"Nombre de structs incorrect dans {file_path}")

    def test_function_detection(self):
        file_path = os.path.join(self.test_dir, "test_function.cpp")
        tu = parse_source(file_path)
        root = get_root_cursor(tu)
        total_functions = self.count_nodes(root, is_function)
        # Dans test_function.cpp, nous attendons 3 fonctions :
        # - freeFunction (fonction globale)
        # - MyFunctionClass::memberFunction (méthode)
        # - MyFunctionClass::constructor (constructeur)
        self.assertEqual(total_functions, 3, f"Nombre de fonctions incorrect dans {file_path}")

    def test_namespace_detection(self):
        file_path = os.path.join(self.test_dir, "test_namespace.cpp")
        tu = parse_source(file_path)
        root = get_root_cursor(tu)
        total_namespaces = self.count_nodes(root, is_namespace)
        # Dans test_namespace.cpp, nous attendons 2 namespaces : OuterNS et OuterNS::InnerNS.
        self.assertEqual(total_namespaces, 2, f"Nombre de namespaces incorrect dans {file_path}")

    def test_custom_type_detection(self):
        file_path = os.path.join(self.test_dir, "test_custom_type.cpp")
        tu = parse_source(file_path)
        root = get_root_cursor(tu)
        total_custom_types = self.count_nodes(root, is_custom_type)
        # Dans test_custom_type.cpp, nous attendons 3 déclarations d'alias :
        # - using CustomInt = int;
        # - typedef double CustomDouble;
        # - using StringVector = std::vector<std::string>; (dans le namespace AliasNS)
        self.assertEqual(total_custom_types, 3, f"Nombre de types custom incorrect dans {file_path}")

if __name__ == "__main__":
    unittest.main()

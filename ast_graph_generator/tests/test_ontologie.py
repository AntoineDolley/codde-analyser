import os
import unittest
import clang.cindex
from ast_graph_generator.ontologie import Entity, FunctionEntity

# Optionnel : ajustez le chemin vers votre libclang si nécessaire
# clang.cindex.Config.set_library_file('/usr/lib/llvm-10/lib/libclang.so.1')

class TestOntologieComplex(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Chemin vers le fichier C++ de test
        cls.test_file = os.path.join(os.path.dirname(__file__), "sample_code", "test_entity.cpp")
        index = clang.cindex.Index.create()
        cls.tu = index.parse(cls.test_file)
        cls.root = cls.tu.cursor

    def find_node(self, spelling, kind=None):
        """Parcourt l'AST pour trouver le premier node dont le spelling correspond (et éventuellement dont le kind correspond)."""
        for node in self.root.walk_preorder():
            if node.spelling == spelling:
                if kind is None or node.kind == kind:
                    return node
        return None

    def test_class_extraction(self):
        # Test pour la classe Base
        base_node = self.find_node("Base", clang.cindex.CursorKind.CLASS_DECL)
        self.assertIsNotNone(base_node, "La classe 'Base' n'a pas été trouvée")
        base_entity = Entity(base_node)
        self.assertEqual(base_entity.name, "Base", "Nom de 'Base' incorrect")
        self.assertEqual(base_entity.namespace_position, "TestNS", "Namespace de 'Base' incorrect")

        # Test pour la classe Derived
        derived_node = self.find_node("Derived", clang.cindex.CursorKind.CLASS_DECL)
        self.assertIsNotNone(derived_node, "La classe 'Derived' n'a pas été trouvée")
        derived_entity = Entity(derived_node)
        self.assertEqual(derived_entity.name, "Derived", "Nom de 'Derived' incorrect")
        self.assertEqual(derived_entity.namespace_position, "TestNS", "Namespace de 'Derived' incorrect")

        # Test pour la classe InnerClass dans InnerNS
        inner_class_node = self.find_node("InnerClass", clang.cindex.CursorKind.CLASS_DECL)
        self.assertIsNotNone(inner_class_node, "La classe 'InnerClass' n'a pas été trouvée")
        inner_entity = Entity(inner_class_node)
        self.assertEqual(inner_entity.name, "InnerClass", "Nom de 'InnerClass' incorrect")
        self.assertEqual(inner_entity.namespace_position, "TestNS::InnerNS", "Namespace de 'InnerClass' incorrect")

    def test_function_extraction(self):
        # Test pour freeFunction dans TestNS
        free_func_node = self.find_node("freeFunction", clang.cindex.CursorKind.FUNCTION_DECL)
        self.assertIsNotNone(free_func_node, "La fonction 'freeFunction' n'a pas été trouvée")
        free_func_entity = FunctionEntity(free_func_node)
        self.assertTrue(free_func_entity.name.startswith("freeFunction("),
                        f"Signature incorrecte pour freeFunction: {free_func_entity.name}")
        self.assertEqual(free_func_entity.namespace_position, "TestNS", "Namespace de 'freeFunction' incorrect")
        
        # Test pour globalFunction hors namespace
        global_func_node = self.find_node("globalFunction", clang.cindex.CursorKind.FUNCTION_DECL)
        self.assertIsNotNone(global_func_node, "La fonction globale 'globalFunction' n'a pas été trouvée")
        global_func_entity = FunctionEntity(global_func_node)
        self.assertTrue(global_func_entity.name.startswith("globalFunction("),
                        f"Signature incorrecte pour globalFunction: {global_func_entity.name}")
        self.assertEqual(global_func_entity.namespace_position, "", "La fonction globale ne doit pas avoir de namespace")
        
        # Test pour les méthodes testMethod surchargées dans Derived
        test_method_nodes = [node for node in self.root.walk_preorder() if node.spelling == "testMethod"]
        self.assertTrue(len(test_method_nodes) >= 2, "La méthode surchargée 'testMethod' n'est pas correctement détectée")
        signatures = [FunctionEntity(node).name for node in test_method_nodes]
        found_no_param = any("testMethod()" in sig for sig in signatures)
        found_with_param = any("testMethod(" in sig and "int" in sig for sig in signatures)
        self.assertTrue(found_no_param, "Méthode 'testMethod' sans paramètre non détectée")
        self.assertTrue(found_with_param, "Méthode 'testMethod' avec paramètres non détectée")
        
    def test_custom_type_extraction(self):
        # Test pour l'alias CustomInt
        custom_int_node = self.find_node("CustomInt", clang.cindex.CursorKind.TYPE_ALIAS_DECL)
        self.assertIsNotNone(custom_int_node, "L'alias 'CustomInt' n'a pas été trouvé")
        custom_int_entity = Entity(custom_int_node)
        self.assertEqual(custom_int_entity.name, "CustomInt", "Nom de l'alias 'CustomInt' incorrect")
        self.assertEqual(custom_int_entity.namespace_position, "TestNS", "Namespace de 'CustomInt' incorrect")
        
        # Test pour l'alias CustomDouble
        custom_double_node = self.find_node("CustomDouble", clang.cindex.CursorKind.TYPE_ALIAS_DECL)
        self.assertIsNotNone(custom_double_node, "L'alias 'CustomDouble' n'a pas été trouvé")
        custom_double_entity = Entity(custom_double_node)
        self.assertEqual(custom_double_entity.name, "CustomDouble", "Nom de l'alias 'CustomDouble' incorrect")
        self.assertEqual(custom_double_entity.namespace_position, "TestNS", "Namespace de 'CustomDouble' incorrect")
        
    def test_inner_method_extraction(self):
        # Test pour la méthode innerMethod dans InnerClass (dans InnerNS)
        inner_method_node = self.find_node("innerMethod", clang.cindex.CursorKind.CXX_METHOD)
        self.assertIsNotNone(inner_method_node, "La méthode 'innerMethod' n'a pas été trouvée")
        inner_method_entity = FunctionEntity(inner_method_node)
        self.assertTrue(inner_method_entity.name.startswith("innerMethod("),
                        f"Signature incorrecte pour innerMethod: {inner_method_entity.name}")
        self.assertEqual(inner_method_entity.namespace_position, "TestNS::InnerNS::InnerClass",
                         "Namespace de 'innerMethod' incorrect")

if __name__ == "__main__":
    unittest.main()

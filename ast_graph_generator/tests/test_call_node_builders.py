# tests/test_call_entities.py
import os
import config
import unittest
import clang.cindex
from ast_graph_generator.ontologie import (
    StandaloneFunctionCallEntity,
    ClassFunctionCallEntity,
    UnexposedClassFunctionCallEntity,
    ConstructorClassFunctionCallEntity,
)
from ast_graph_generator.node_filters import (
    is_standalone_function_call,
    is_class_function_call,
    is_class_function_call_unxeposed,
    is_constructor_call,
    is_allowed_node,
)

def collect_entities_by_predicate(predicate, entity_class, root_node, ALLOWED_PATHS):
    """
    Parcourt récursivement l'AST à partir de root_node et renvoie une liste
    d'objets instanciés à partir de entity_class pour chaque nœud satisfaisant le prédicat.
    
    Parameters:
      - predicate: fonction de filtrage sur les nœuds (ex: is_standalone_function_call)
      - entity_class: la classe d'ontologie associée (ex: StandaloneFunctionCallEntity)
      - root_node: nœud racine de l'AST
      - ALLOWED_PATHS: liste des chemins autorisés (utilisée dans is_allowed_node)
    
    Returns:
      - Liste d'objets créés avec entity_class(node)
    """
    results = []
    for node in root_node.walk_preorder():
        if is_allowed_node(node, ALLOWED_PATHS) and predicate(node):
            entity = entity_class(node)
            results.append(entity)
    return results

class TestCallEntities(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuration de libclang (exécutée une seule fois pour ce module)
        libclang_path = config.LIBCLANG_PATH
        clang.cindex.Config.set_library_file(libclang_path)
        
        # Positionnement dans le dossier des tests
        os.chdir("/home/antoine/Documents/codde-analyser/ast_graph_generator/tests")
        cls.index = clang.cindex.Index.create()
        cls.test_file = "test_files/sep_test/Actions.cpp"
        args = ['-std=c++11', '-c', '-I./test_files/sep_test/']
        # On limite l'analyse au fichier de test
        cls.ALLOWED_PATHS = [cls.test_file]
        cls.translation_unit = cls.index.parse(cls.test_file, args=args)

        # Pour afficher la diff complète en cas d'erreur
        cls.maxDiff = None

    def extract_keys(self, d):
        keys = ["name", "decl_file", "start_line", "end_line", "namespace_position", "type"]
        return {k: d.get(k) for k in keys}

    def test_standalone_function_call(self):
        entities = collect_entities_by_predicate(is_standalone_function_call,
                                                 StandaloneFunctionCallEntity,
                                                 self.translation_unit.cursor,
                                                 self.ALLOWED_PATHS)
        found = [self.extract_keys(vars(entity)) for entity in entities]
        expected = [
            {
                "name": "test_files/sep_test/Actions.cpp#Actions::displayPersonInfo(const Entities::Person & person)",
                "decl_file": os.path.normpath("test_files/sep_test/Actions.cpp"),
                "start_line": 6,
                "end_line": 9,
                "namespace_position": "Actions::displayPersonInfo(const Entities::Person & person)", 
                "type": "CALL",
            }
        ]
        self.assertEqual(found, expected, "Les appels de fonction autonome ne correspondent pas aux objets attendus.")

    def test_constructor_call(self):
        entities = collect_entities_by_predicate(is_constructor_call,
                                                 ConstructorClassFunctionCallEntity,
                                                 self.translation_unit.cursor,
                                                 self.ALLOWED_PATHS)
        found = [self.extract_keys(vars(entity)) for entity in entities]
        expected = [
            {
                "name": "test_files/sep_test/Entities.h#Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",  # Pour un appel de constructeur, le spelling peut être vide
                "decl_file": os.path.normpath("test_files/sep_test/Entities.h"),
                "start_line": 15,
                "end_line": 15,
                "namespace_position": "Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",  # Selon votre implémentation
                "type": "CALL",
            }
        ]
        self.assertEqual(found, expected, "Les appels de constructeur ne correspondent pas aux objets attendus.")

    def test_class_function_call(self):
        entities = collect_entities_by_predicate(is_class_function_call,
                                                 ClassFunctionCallEntity,
                                                 self.translation_unit.cursor,
                                                 self.ALLOWED_PATHS)
        found = [self.extract_keys(vars(entity)) for entity in entities]
        expected = [
            {
                "name": "test_files/sep_test/Entities.h#Entities::Person::getName()",
                "decl_file": os.path.normpath("test_files/sep_test/Entities.h"),
                "start_line": 16,
                "end_line": 16,
                "namespace_position": "Entities::Person::getName()", 
                "type": "CALL",
            },
            {
                "name": "test_files/sep_test/Entities.h#Entities::Person::getAge()",
                "decl_file": os.path.normpath("test_files/sep_test/Entities.h"),
                "start_line": 18,
                "end_line": 18,
                "namespace_position": "Entities::Person::getAge()",
                "type": "CALL",
            },
            {
                "name": "test_files/sep_test/Entities.h#Entities::Company::getCompanyName()",
                "decl_file": os.path.normpath("test_files/sep_test/Entities.h"),
                "start_line": 33,
                "end_line": 33,
                "namespace_position": "Entities::Company::getCompanyName()",
                "type": "CALL",
            },
            {
                "name": "test_files/sep_test/Entities.h#Entities::Person::setFrom(const Person & other)",
                "decl_file": os.path.normpath("test_files/sep_test/Entities.h"),
                "start_line": 22,
                "end_line": 22,
                "namespace_position": "Entities::Person::setFrom(const Person & other)",
                "type": "CALL",
            },
        ]
        self.assertEqual(found, expected, "Les appels de fonction de classe ne correspondent pas aux objets attendus.")

    def test_class_function_call_unexposed(self):
        entities = collect_entities_by_predicate(is_class_function_call_unxeposed,
                                                 UnexposedClassFunctionCallEntity,
                                                 self.translation_unit.cursor,
                                                 self.ALLOWED_PATHS)
        found = [self.extract_keys(vars(entity)) for entity in entities]
        expected = []  # Aucun appel non exposé attendu
        self.assertEqual(found, expected, "Il ne devrait y avoir aucun appel de fonction de classe non exposé.")

if __name__ == '__main__':
    unittest.main()

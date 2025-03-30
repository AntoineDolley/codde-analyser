# tests/test_decl_node_builders.py
import os
import config
import unittest
import clang.cindex
from ast_graph_generator.ontologie import (
    NamespaceDeclEntity, 
    ClassDeclEntity, 
    FunctionDeclEntity,
)
from ast_graph_generator.node_filters import (
    is_namespace_decl,
    is_class_decl,
    is_function_decl,
    is_allowed_node,
)

def collect_entities_by_predicate(predicate, entity_class, root_node, ALLOWED_PATHS):
    """
    Parcourt récursivement l'AST à partir de root_node et renvoie une liste
    d'objets instanciés à partir de entity_class pour chaque nœud satisfaisant le prédicat.
    
    Parameters:
      - predicate: fonction de filtrage sur les nœuds (ex: is_namespace_decl)
      - entity_class: la classe d'ontologie associée (ex: NamespaceDeclEntity)
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

class TestDeclParsingFunctionsReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Configuration de libclang (exécutée une seule fois pour ce module)
        libclang_path = config.LIBCLANG_PATH
        clang.cindex.Config.set_library_file(libclang_path)

        # Positionnement dans le dossier des tests
        os.chdir("/home/antoine/Documents/codde-analyser/ast_graph_generator/tests")
        cls.index = clang.cindex.Index.create()
        cls.test_file = os.path.join(os.path.dirname(__file__), "test_files", "test_decl", "src", "test_code.cpp")
        args = ['-std=c++11', '-c', '-I./test_files/test_decl/Include']
        # Ici, on limite l'analyse au fichier de test (vous pouvez adapter ALLOWED_PATHS si besoin)
        cls.ALLOWED_PATHS = [cls.test_file]
        cls.translation_unit = cls.index.parse(cls.test_file, args=args)
        cls.maxDiff = None
    
    def test_namespace_decl(self):
        # Collecte des objets de type NamespaceDeclEntity
        entities = collect_entities_by_predicate(is_namespace_decl, NamespaceDeclEntity, self.translation_unit.cursor, self.ALLOWED_PATHS)
        found = [vars(entity) for entity in entities]
        expected = [
            {
                "name": "test_files/test_decl/Include/test_code.h#CustomTypes",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 8,
                "end_line": 12,
                "namespace_position": "CustomTypes",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 14,
                "end_line": 47,
                "namespace_position": "Entities",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Actions",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 49,
                "end_line": 54,
                "namespace_position": "Actions",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 3,
                "end_line": 72,
                "namespace_position": "Entities",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Actions",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 74,
                "end_line": 93,
                "namespace_position": "Actions",
                "type": "DECL",
            },
        ]
        self.assertEqual(found, expected, "Les déclarations de namespace trouvées ne correspondent pas aux objets attendus.")
    
    def test_class_decl(self):
        # Collecte des objets de type ClassDeclEntity
        entities = collect_entities_by_predicate(is_class_decl, ClassDeclEntity, self.translation_unit.cursor, self.ALLOWED_PATHS)
        found = [vars(entity) for entity in entities]
        expected = [
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 16,
                "end_line": 30,
                "namespace_position": "Entities::Person",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 32,
                "end_line": 46,
                "namespace_position": "Entities::Company",
                "type": "DECL",
            },
        ]
        self.assertEqual(found, expected, "Les déclarations de classe trouvées ne correspondent pas aux objets attendus.")
       
    def test_function_decl(self):
        # Collecte des objets de type FunctionDeclEntity
        entities = collect_entities_by_predicate(is_function_decl, FunctionDeclEntity, self.translation_unit.cursor, self.ALLOWED_PATHS)
        found = [vars(entity) for entity in entities]
        expected = [
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 22,
                "end_line": 22,
                "namespace_position": "Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::getName()",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 23,
                "end_line": 23,
                "namespace_position": "Entities::Person::getName()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::setName(const CustomTypes::StringType & newName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 24,
                "end_line": 24,
                "namespace_position": "Entities::Person::setName(const CustomTypes::StringType & newName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::getAge()",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 25,
                "end_line": 25,
                "namespace_position": "Entities::Person::getAge()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::setAge(CustomTypes::IntegerType newAge)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 26,
                "end_line": 26,
                "namespace_position": "Entities::Person::setAge(CustomTypes::IntegerType newAge)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::updateName(const CustomTypes::StringType & newName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 27,
                "end_line": 27,
                "namespace_position": "Entities::Person::updateName(const CustomTypes::StringType & newName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::updateAge(CustomTypes::IntegerType newAge)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 28,
                "end_line": 28,
                "namespace_position": "Entities::Person::updateAge(CustomTypes::IntegerType newAge)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Person::setFrom(const Person & other)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 29,
                "end_line": 29,
                "namespace_position": "Entities::Person::setFrom(const Person & other)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::Company(const CustomTypes::StringType & companyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 38,
                "end_line": 38,
                "namespace_position": "Entities::Company::Company(const CustomTypes::StringType & companyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::addEmployee(const Person & employee)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 39,
                "end_line": 39,
                "namespace_position": "Entities::Company::addEmployee(const Person & employee)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::getCompanyName()",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 40,
                "end_line": 40,
                "namespace_position": "Entities::Company::getCompanyName()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::getEmployees()",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 41,
                "end_line": 41,
                "namespace_position": "Entities::Company::getEmployees()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::setCompanyName(const CustomTypes::StringType & newCompanyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 42,
                "end_line": 42,
                "namespace_position": "Entities::Company::setCompanyName(const CustomTypes::StringType & newCompanyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::updateCompanyName(const CustomTypes::StringType & newCompanyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 43,
                "end_line": 43,
                "namespace_position": "Entities::Company::updateCompanyName(const CustomTypes::StringType & newCompanyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::addEmployeeChain(const Person & employee)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 44,
                "end_line": 44,
                "namespace_position": "Entities::Company::addEmployeeChain(const Person & employee)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Entities::Company::setFrom(const Company & other)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 45,
                "end_line": 45,
                "namespace_position": "Entities::Company::setFrom(const Company & other)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Actions::displayPersonInfo(const Entities::Person & person)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 50,
                "end_line": 50,
                "namespace_position": "Actions::displayPersonInfo(const Entities::Person & person)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Actions::displayCompanyInfo(const Entities::Company & company)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 51,
                "end_line": 51,
                "namespace_position": "Actions::displayCompanyInfo(const Entities::Company & company)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Actions::displayEmployeeInfo(const Entities::Company & company, CustomTypes::SizeType employeeIndex)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 52,
                "end_line": 52,
                "namespace_position": "Actions::displayEmployeeInfo(const Entities::Company & company, CustomTypes::SizeType employeeIndex)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#Actions::initializeAndDisplayPersonInfo(const Entities::Person & original)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 53,
                "end_line": 53,
                "namespace_position": "Actions::initializeAndDisplayPersonInfo(const Entities::Person & original)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/Include/test_code.h#transformPerson(const Entities::Person & original)",
                "decl_file": os.path.normpath("test_files/test_decl/src/../Include/test_code.h"),
                "start_line": 57,
                "end_line": 57,
                "namespace_position": "transformPerson(const Entities::Person & original)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 5,
                "end_line": 6,
                "namespace_position": "Entities::Person::Person(const CustomTypes::StringType & name, CustomTypes::IntegerType age)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::getName()",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 8,
                "end_line": 10,
                "namespace_position": "Entities::Person::getName()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::setName(const CustomTypes::StringType & newName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 12,
                "end_line": 14,
                "namespace_position": "Entities::Person::setName(const CustomTypes::StringType & newName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::getAge()",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 16,
                "end_line": 18,
                "namespace_position": "Entities::Person::getAge()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::setAge(CustomTypes::IntegerType newAge)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 20,
                "end_line": 22,
                "namespace_position": "Entities::Person::setAge(CustomTypes::IntegerType newAge)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::updateName(const CustomTypes::StringType & newName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 24,
                "end_line": 27,
                "namespace_position": "Entities::Person::updateName(const CustomTypes::StringType & newName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::updateAge(CustomTypes::IntegerType newAge)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 29,
                "end_line": 32,
                "namespace_position": "Entities::Person::updateAge(CustomTypes::IntegerType newAge)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Person::setFrom(const Person & other)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 34,
                "end_line": 37,
                "namespace_position": "Entities::Person::setFrom(const Person & other)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::Company(const CustomTypes::StringType & companyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 39,
                "end_line": 40,
                "namespace_position": "Entities::Company::Company(const CustomTypes::StringType & companyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::addEmployee(const Person & employee)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 42,
                "end_line": 44,
                "namespace_position": "Entities::Company::addEmployee(const Person & employee)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::getCompanyName()",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 46,
                "end_line": 48,
                "namespace_position": "Entities::Company::getCompanyName()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::getEmployees()",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 50,
                "end_line": 52,
                "namespace_position": "Entities::Company::getEmployees()",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::setCompanyName(const CustomTypes::StringType & newCompanyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 54,
                "end_line": 56,
                "namespace_position": "Entities::Company::setCompanyName(const CustomTypes::StringType & newCompanyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::updateCompanyName(const CustomTypes::StringType & newCompanyName)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 58,
                "end_line": 61,
                "namespace_position": "Entities::Company::updateCompanyName(const CustomTypes::StringType & newCompanyName)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::addEmployeeChain(const Person & employee)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 63,
                "end_line": 66,
                "namespace_position": "Entities::Company::addEmployeeChain(const Person & employee)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Entities::Company::setFrom(const Company & other)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 68,
                "end_line": 71,
                "namespace_position": "Entities::Company::setFrom(const Company & other)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Actions::displayPersonInfo(const Entities::Person & person)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 76,
                "end_line": 78,
                "namespace_position": "Actions::displayPersonInfo(const Entities::Person & person)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Actions::displayCompanyInfo(const Entities::Company & company)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 80,
                "end_line": 82,
                "namespace_position": "Actions::displayCompanyInfo(const Entities::Company & company)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Actions::displayEmployeeInfo(const Entities::Company & company, CustomTypes::SizeType employeeIndex)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 84,
                "end_line": 86,
                "namespace_position": "Actions::displayEmployeeInfo(const Entities::Company & company, CustomTypes::SizeType employeeIndex)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#Actions::initializeAndDisplayPersonInfo(const Entities::Person & original)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 88,
                "end_line": 92,
                "namespace_position": "Actions::initializeAndDisplayPersonInfo(const Entities::Person & original)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#transformPerson(const Entities::Person & original)",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 96,
                "end_line": 100,
                "namespace_position": "transformPerson(const Entities::Person & original)",
                "type": "DECL",
            },
            {
                "name": "test_files/test_decl/src/test_code.cpp#main()",
                "decl_file": os.path.normpath("test_files/test_decl/src/test_code.cpp"),
                "start_line": 102,
                "end_line": 113,
                "namespace_position": "main()",
                "type": "DECL",
            },
        ]
        self.assertEqual(found, expected, "Les déclarations de fonction trouvées ne correspondent pas au résultat attendu.")
 
if __name__ == '__main__':
    unittest.main()

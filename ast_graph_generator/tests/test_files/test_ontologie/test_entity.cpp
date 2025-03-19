// tests/sample_code/test_entity.cpp
#include <iostream>
#include <string>

namespace TestNS {
    // Définition d'une classe de base
    class Base {
    public:
        Base() {}
        virtual ~Base() {}
        virtual void baseMethod(int a) {
            std::cout << "Base method: " << a << std::endl;
        }
    };

    // Classe dérivée avec surcharge et méthode spécifique
    class Derived : public Base {
    public:
        Derived() : Base() {}
        ~Derived() {}
        // Surcharge de la méthode de base
        void baseMethod(int a) override {
            std::cout << "Derived baseMethod: " << a << std::endl;
        }
        // Méthode testMethod sans paramètre
        void testMethod() {
            std::cout << "Test method in Derived" << std::endl;
        }
        // Méthode testMethod surchargée avec des paramètres
        void testMethod(int a, double b) {
            std::cout << "Overloaded testMethod: " << a << ", " << b << std::endl;
        }
    };

    // Espace de noms imbriqué
    namespace InnerNS {
        class InnerClass {
        public:
            InnerClass() {}
            void innerMethod(const std::string &s) {
                std::cout << "Inner method: " << s << std::endl;
            }
        };
    } // namespace InnerNS

    // Fonction libre dans le namespace TestNS
    void freeFunction(float f, const char* s) {
        std::cout << "Free function: " << f << ", " << s << std::endl;
    }

    // Alias de types pour tester les types custom
    using CustomInt = int;
    typedef double CustomDouble;
} // namespace TestNS

// Fonction globale en dehors de tout namespace
void globalFunction() {
    std::cout << "Global function" << std::endl;
}

int main() {
    // Instanciation et utilisation des classes dans TestNS
    TestNS::Base baseObj;
    TestNS::Derived derivedObj;
    derivedObj.testMethod();
    derivedObj.testMethod(10, 3.14);

    // Utilisation de la classe imbriquée dans InnerNS
    TestNS::InnerNS::InnerClass innerObj;
    innerObj.innerMethod("Hello from InnerNS");

    // Appel de la fonction libre du namespace TestNS
    TestNS::freeFunction(1.23f, "Test Free Function");

    // Appel de la fonction globale
    globalFunction();

    return 0;
}

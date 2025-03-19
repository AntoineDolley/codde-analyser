// test_namespace.cpp
#include <iostream>

namespace OuterNS {
    void outerFunction() {
        std::cout << "Outer function" << std::endl;
    }
    
    namespace InnerNS {
        class InnerClass {
        public:
            void display() {
                std::cout << "Inner class method" << std::endl;
            }
        };

        void innerFunction(int x) {
            std::cout << "Inner function: " << x << std::endl;
        }
    }
}

int main() {
    OuterNS::outerFunction();
    OuterNS::InnerNS::InnerClass obj;
    obj.display();
    OuterNS::InnerNS::innerFunction(100);
    return 0;
}

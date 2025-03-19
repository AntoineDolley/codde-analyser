// test_function.cpp
#include <iostream>

void freeFunction(int a, double b) {
    std::cout << "Free function: " << a << ", " << b << std::endl;
}

class MyFunctionClass {
public:
    MyFunctionClass() {}  // constructeur
    void memberFunction(int x) {
        std::cout << "Member function: " << x << std::endl;
    }
};

int main() {
    freeFunction(1, 2.5);
    MyFunctionClass obj;
    obj.memberFunction(42);
    return 0;
}

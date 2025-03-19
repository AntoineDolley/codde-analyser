// test_class.cpp
#include <iostream>

class MyClass {
public:
    MyClass() {}
    void doSomething() {}
private:
    int value;
};

class Outer {
public:
    class Inner {
    public:
        Inner() {}
    };
};

int main() {
    MyClass obj;
    Outer::Inner inner;
    return 0;
}

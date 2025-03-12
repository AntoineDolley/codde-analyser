// test_struct.cpp
#include <iostream>

struct MyStruct {
    int a;
    float b;
};

struct OuterStruct {
    struct InnerStruct {
        double c;
    };
};

int main() {
    MyStruct s = {1, 2.0f};
    OuterStruct::InnerStruct inner = {3.14};
    return 0;
}

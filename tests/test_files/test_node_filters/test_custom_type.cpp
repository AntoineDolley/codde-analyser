// test_custom_type.cpp
#include <iostream>
#include <vector>
#include <string>

// Alias simple
using CustomInt = int;
typedef double CustomDouble;

// Alias dans un namespace
namespace AliasNS {
    using StringVector = std::vector<std::string>;
}

int main() {
    CustomInt a = 10;
    CustomDouble b = 3.14;
    AliasNS::StringVector vec;
    vec.push_back("test");
    std::cout << "Custom types tested: " << a << ", " << b << ", " << vec[0] << std::endl;
    return 0;
}

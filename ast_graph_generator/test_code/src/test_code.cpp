#include "../Include/test_code.h"

namespace Entities {

    // Définition de Person
    Person::Person(const CustomTypes::StringType& name, CustomTypes::IntegerType age)
        : name(name), age(age) {}

    CustomTypes::StringType Person::getName() const {
        return name;
    }

    void Person::setName(const CustomTypes::StringType& newName) {
        name = newName;
    }

    CustomTypes::IntegerType Person::getAge() const {
        return age;
    }

    void Person::setAge(CustomTypes::IntegerType newAge) {
        age = newAge;
    }

    // Définition de Company
    Company::Company(const CustomTypes::StringType& companyName)
        : companyName(companyName) {}

    void Company::addEmployee(const Person& employee) {
        employees.push_back(employee);
    }

    CustomTypes::StringType Company::getCompanyName() const {
        return companyName;
    }
}

namespace Actions {

    void displayPersonInfo(const Entities::Person& person) {
        std::cout << "Name: " << person.getName() << ", Age: " << person.getAge() << std::endl;
    }

    void displayCompanyInfo(const Entities::Company& company) {
        std::cout << "Company: " << company.getCompanyName() << ", Number of Employees: " << std::endl;
    }
}

int main() {
    Entities::Person alice("Alice Smith", 28);
    Entities::Company techCorp("Tech Corporation");

    techCorp.addEmployee(alice);

    Actions::displayPersonInfo(alice);
    Actions::displayCompanyInfo(techCorp);

    return 0;
}

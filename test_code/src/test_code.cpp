#include "../Include/test_code.h"

namespace Entities {

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

    Person& Person::updateName(const CustomTypes::StringType& newName) {
        name = newName;
        return *this;
    }

    Person& Person::updateAge(CustomTypes::IntegerType newAge) {
        age = newAge;
        return *this;
    }

    void Person::setFrom(const Person& other) {
        name = other.name;
        age = other.age;
    }

    Company::Company(const CustomTypes::StringType& companyName)
        : companyName(companyName) {}

    void Company::addEmployee(const Person& employee) {
        employees.push_back(employee);
    }

    CustomTypes::StringType Company::getCompanyName() const {
        return companyName;
    }

    std::vector<Person>& Company::getEmployees() {
        return employees;
    }

    void Company::setCompanyName(const CustomTypes::StringType& newCompanyName) {
        companyName = newCompanyName;
    }

    Company& Company::updateCompanyName(const CustomTypes::StringType& newCompanyName) {
        companyName = newCompanyName;
        return *this;
    }

    Company& Company::addEmployeeChain(const Person& employee) {
        employees.push_back(employee);
        return *this;
    }

    void Company::setFrom(const Company& other) {
        companyName = other.companyName;
        employees = other.employees;
    }
}

namespace Actions {

    void displayPersonInfo(const Entities::Person& person) {
        std::cout << "Name: " << person.getName() << ", Age: " << person.getAge() << std::endl;
    }

    void displayCompanyInfo(const Entities::Company& company) {
        std::cout << "Company: " << company.getCompanyName() << std::endl;
    }

    void displayEmployeeInfo(const Entities::Company& company, CustomTypes::SizeType employeeIndex) {
        // Implémentation éventuelle pour afficher un employé spécifique
    }

    void initializeAndDisplayPersonInfo(const Entities::Person& original) {
        // Utilisation de la fonction libre pour transformer le Person original
        Entities::Person newPerson = transformPerson(original);
        displayPersonInfo(newPerson);
    }
}

// Définition de la fonction libre qui transforme un Person
Entities::Person transformPerson(const Entities::Person& original) {
    // Exemple : on ajoute le préfixe "Transformed " au nom et on incrémente l'âge de 1
    Entities::Person transformed("Transformed " + original.getName(), original.getAge() + 1);
    return transformed;
}

int main() {
    Entities::Person alice("Alice Smith", 28);
    Entities::Company techCorp("Tech Corporation");

    techCorp.addEmployee(alice);

    Actions::displayPersonInfo(alice);
    Actions::displayCompanyInfo(techCorp);
    Actions::initializeAndDisplayPersonInfo(alice);

    return 0;
}

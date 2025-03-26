#include "Entities.h"

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

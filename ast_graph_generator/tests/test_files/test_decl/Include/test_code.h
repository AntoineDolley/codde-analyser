#ifndef TEST_CODE_H
#define TEST_CODE_H

#include <string>
#include <vector>
#include <iostream>

namespace CustomTypes {
    using StringType = std::string;
    using SizeType = std::size_t;
    using IntegerType = int;
}

namespace Entities {

    class Person {
    private:
        CustomTypes::StringType name;
        CustomTypes::IntegerType age;

    public:
        Person(const CustomTypes::StringType& name, CustomTypes::IntegerType age);
        CustomTypes::StringType getName() const;
        void setName(const CustomTypes::StringType& newName);
        CustomTypes::IntegerType getAge() const;
        void setAge(CustomTypes::IntegerType newAge);
        Person& updateName(const CustomTypes::StringType& newName);
        Person& updateAge(CustomTypes::IntegerType newAge);
        void setFrom(const Person& other);
    };

    class Company {
    private:
        CustomTypes::StringType companyName;
        std::vector<Person> employees;

    public:
        Company(const CustomTypes::StringType& companyName);
        void addEmployee(const Person& employee);
        CustomTypes::StringType getCompanyName() const;
        std::vector<Person>& getEmployees();
        void setCompanyName(const CustomTypes::StringType& newCompanyName);
        Company& updateCompanyName(const CustomTypes::StringType& newCompanyName);
        Company& addEmployeeChain(const Person& employee);
        void setFrom(const Company& other);
    };
}

namespace Actions {
    void displayPersonInfo(const Entities::Person& person);
    void displayCompanyInfo(const Entities::Company& company);
    void displayEmployeeInfo(const Entities::Company& company, CustomTypes::SizeType employeeIndex);
    void initializeAndDisplayPersonInfo(const Entities::Person& original);
}

// Déclaration d'une fonction libre (non associée à une classe)
Entities::Person transformPerson(const Entities::Person& original);

#endif // TEST_CODE_H

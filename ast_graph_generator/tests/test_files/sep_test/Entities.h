#ifndef ENTITIES_H
#define ENTITIES_H

#include "CustomTypes.h"
#include <vector>

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
        void setFrom(const Person& other); // Ajout de la fonction setFrom
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
        void setFrom(const Company& other); // Ajout de la fonction setFrom
    };
}

#endif // ENTITIES_H

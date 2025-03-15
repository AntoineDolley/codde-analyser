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
    };

    class Company {
    private:
        CustomTypes::StringType companyName;
        std::vector<Person> employees;

    public:
        Company(const CustomTypes::StringType& companyName);
        void addEmployee(const Person& employee);
        CustomTypes::StringType getCompanyName() const;
    };
}

namespace Actions {

    void displayPersonInfo(const Entities::Person& person);
    void displayCompanyInfo(const Entities::Company& company);
}

#endif // TEST_CODE_H

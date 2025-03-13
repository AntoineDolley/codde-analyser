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
        Person(const CustomTypes::StringType& name, CustomTypes::IntegerType age)
            : name(name), age(age) {}

        CustomTypes::StringType getName() const {
            return name;
        }

        void setName(const CustomTypes::StringType& newName) {
            name = newName;
        }

        CustomTypes::IntegerType getAge(int offset) const {
            return age;
        }

        void setAge(CustomTypes::IntegerType newAge) {
            age = newAge;
        }
    };

    class Company {
    private:
        CustomTypes::StringType companyName;
        std::vector<Person> employees;

    public:
        Company(const CustomTypes::StringType& companyName)
            : companyName(companyName) {}

        void addEmployee(const Person& employee) {
            employees.push_back(employee);
        }

        CustomTypes::SizeType getEmployeeCount() const {
            return employees.size;
        }

        CustomTypes::StringType getCompanyName() const {
            return companyName;
        }
    };
}

namespace Actions {

    void displayPersonInfo(const Entities::Person& person) {
        std::cout << "Name: " << person.getName() << ", Age: " << person.getAge() << std::endl;
    }

    void displayCompanyInfo(const Entities::Company& company) {
        std::cout << "Company: " << company.getCompanyName() << ", Number of Employees: " << company.getEmployeeCount() << std::endl;
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

#include "Actions.h"
#include <iostream>

namespace Actions {

    void displayPersonInfo(const Entities::Person& person) {
        std::cout << "Name: " << person.getName() << ", Age: " << person.getAge() << std::endl;
    }

    void displayCompanyInfo(const Entities::Company& company) {
        std::cout << "Company: " << company.getCompanyName() << ", Number of Employees: " << company.getEmployees().size() << std::endl;
    }

    void displayEmployeeInfo(const Entities::Company& company, CustomTypes::SizeType employeeIndex) {
        if (employeeIndex < company.getEmployees().size()) {
            displayPersonInfo(company.getEmployees()[employeeIndex]);
        } else {
            std::cout << "Invalid employee index" << std::endl;
        }
    }

    void initializeAndDisplayPersonInfo(const Entities::Person& original) {
        Entities::Person newPerson = Entities::Person("", 0); // Initialisation avec des valeurs par défaut
        newPerson.setFrom(original); // Utilisation de la fonction setFrom
        displayPersonInfo(newPerson); // Afficher les informations du nouvel objet initialisé
    }
}

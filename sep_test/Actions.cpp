#include "Actions.h"
#include <iostream>

namespace Actions {

    void displayPersonInfo(const Entities::Person& person) {
        person.getName();
        person.getAge();
    }

    void displayCompanyInfo(const Entities::Company& company) {
        company.getCompanyName();
    }

    void displayEmployeeInfo(const Entities::Company& company, CustomTypes::SizeType employeeIndex) {
    }

    void initializeAndDisplayPersonInfo(const Entities::Person& original) {
        Entities::Person newPerson = Entities::Person("", 0); // Initialisation avec des valeurs par défaut
        newPerson.setFrom(original); // Utilisation de la fonction setFrom
        displayPersonInfo(newPerson); // Afficher les informations du nouvel objet initialisé
    }
}

#ifndef ACTIONS_H
#define ACTIONS_H

#include "Entities.h"

namespace Actions {
    void displayPersonInfo(const Entities::Person& person);
    void displayCompanyInfo(const Entities::Company& company);
    void displayEmployeeInfo(const Entities::Company& company, CustomTypes::SizeType employeeIndex);
    void initializeAndDisplayPersonInfo(const Entities::Person& original); // Ajout de la fonction initializeAndDisplayPersonInfo
}

#endif // ACTIONS_H

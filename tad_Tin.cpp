#include "cantera/thermo.h"
#include <iostream>
#include <string.h>

using namespace Cantera;
using namespace std;

// The actual code is put into a function that
// can be called from the main program.
void simple_demo()
{
    // Create a new phase
    std::unique_ptr<ThermoPhase> gas(newPhase("JP10.yaml"));
    
    // declare the variable phi and initialise with some values
    double phi[] = { 0.5,1,1.5 };

    // gaseous fuel species
    string fuelSpecies = "C10H16";

    // declare an array for inlet temp
    double T[50];

    // initialise the array with values ranging from 500 to 1000
    for (int i = 0; i < 50; i++) {
        T[i] = 500 + (10.2 * i);
    }

    auto species = gas->nSpecies();

    // decalre variables to hold the data
    double Tad[50];
 
    for (int j = 0; j < 3; j++) {
        for (int i = 0; i < 50; i++) {
            // set the gas state
            gas->setState_TP(T[i], 101325);

            gas->setEquivalenceRatio(phi[j], fuelSpecies, "O2:1.0, N2:3.76");

            // equilibrate the mixture adiabatically at constant P
            gas->equilibrate("HP", "gibbs");

            Tad[i] = gas->temperature();

            cout << "phi = " << phi[j] << "\t Tad = " << Tad[i] << "\t T = " << T[i] << endl;
        }
    }
}


// the main program just calls function simple_demo within
// a 'try' block, and catches CanteraError exceptions that
// might be thrown
int main()
{
    try {
        simple_demo();
    }
    catch (CanteraError& err) {
        std::cout << err.what() << std::endl;
    }
}



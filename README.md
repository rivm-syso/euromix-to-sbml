# Euromix model to SBML

Model describing the efforts to convert euromix model to SBML

## Procedure

1. Manually convert model to antimony.
2. Use tellurium to convert antimony to sbml.

## Status

Two variants of the full model have been created:
* `model/euromix_man.sbml`: full model that uses a function to compute the concentrations and the `piecewise` operator to replace the ternary operator from the c code.
* `model/euromix_man_explicit.sbml`: full model with functions and `piecewise` operator replaced by explicit code.

Next to thee two, there is also a variant that only includes the liver, blood compartments and external compartements (`model/euromix_man_only_liver`).

Unfortunately, the simulations using the sbml model do not match the simulation results obtained with R. See the notebooks in `notebooks` for the comparisson.

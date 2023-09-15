# Euromix model to SBML

Model describing the efforts to convert euromix model to SBML

## Procedure

1. Manually convert model to antimony.
2. Use tellurium to convert antimony to sbml.

## Status

The results of the R simulation and the SBML simulation (using libroadrunner in Python) match.

Note that Libroadrunner returns concentrations, also if a species is declared to be `substanceOnly`. Therefore it is necessary to convert the output to amounts by multiplying the concentration with volume of the compartment the species is placed in.


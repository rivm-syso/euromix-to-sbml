# Euromix model to SBML

Model describing the efforts to convert euromix model to SBML.

## Procedure

1. Manually convert model to antimony.
2. Use tellurium to convert antimony to sbml.

## Notebooks

Notebook [test_full_model.ipynb](notebooks/text_full_model.ipynb) shows the results of the validation comparison with the results obtained by the R/MCSim/desolve implementation.

Notebook [test_full_model.ipynb](notebooks/getting_sbml_model_info.ipynb) shows how information can be retrieved from this model (e.g., differential equations, diagrams, semantic annotations) and how to run the SBML model.

## Status

The results of the R simulation and the SBML simulation (using libroadrunner in Python) match.

Note that Libroadrunner returns concentrations, also if a species is declared to be `substanceOnly`. Therefore it is necessary to convert the output to amounts by multiplying the concentration with volume of the compartment the species is placed in.

### TODO

* Add semantic annotation of units, compartments, substances, parameters, species, etc.
* ...

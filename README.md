# Euromix model to SBML

This repository contains a re-implementation of the EuroMix PBK model[^1] in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html) and demonstrates how this Antimony model implementation is automatically converted to an annotated Systems Biology Markup Language ([SBML](https://sbml.org/)) file using the [SBML PBK workflow](https://github.com/jwkruisselbrink/sbml-pbk-workflow). The purpose of this repository is to test/demonstrate how to create and publish interoperable PBK models using the EuroMix PBK model as example.

## Model diagram

![Model diagram of the EuroMix PBK model](euromix-pbk-model.png)

## Reimplementation in antimony

The model was reimplemented in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html), see file [euromix.ant](model/euromix.ant). The results of the R simulation and the SBML simulation (using libroadrunner in Python) match.

Notebook [validate_antimony_model.ipynb](notebooks/validate_antimony_model.ipynb) shows the results of the validation comparison with the results obtained by the R/MCSim/desolve implementation. Note that the [libRoadRunner](https://www.libroadrunner.org/) engine that is used for the python simulations returns concentrations, also if a species is declared to be `substanceOnly`. Therefore it is necessary to convert the output to amounts by multiplying the concentration with volume of the compartment the species is placed in in order to obtain amounts.

## SBML conversion and annotation

The [SBML PBK workflow](https://github.com/jwkruisselbrink/sbml-pbk-workflow) follows several steps. It first converts the Antimony model implementation to SBML. Then, it annotates this SBML file using the annotations specified in the file [euromix.annotations.csv](model/euromix.annotations.csv). After this, it runs (unit) validation scripts on the generated SBML file. Finally, it publishes the generated SBML file (and log files) as build artifacts and pushes the generated/updated sbml file ([euromix.sbml](model/euromix.sbml)) to the repository.

Notebook [get_model_info.ipynb](notebooks/get_model_info.ipynb) shows how information can be retrieved from the annotated model (e.g., units, differential equations, diagrams, semantic annotations). Notebook [run_sbml_model.ipynb](notebooks/run_sbml_model.ipynb) demonstrates how to run the SBML model.

## Running the Jupyter notebooks

To run the Jupyter notebook, install Jupyter notebook and the the required python packages.

Install notebook, using the command:

```
pip install notebook
```

Install the required python packages using the command:

```
pip install -r requirements.txt
```

[^1] Tebby, C., van der Voet, H., de Sousa, G., Rorije, E., Kumar, V., de Boer, W., Kruisselbrink, J. W., Bois, F. Y., Faniband, M., Moretto, A., and Brochot, C. A generic pbtk model implemented in the mcra platform: predictive performance and uses in risk assessment of chemicals. Food and Chemical Toxicology, 142:111440, 2020. URL: https://www.sciencedirect.com/science/article/pii/S0278691520303306.
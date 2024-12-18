# EuroMix model to SBML

[![Licence](https://img.shields.io/github/license/rivm-syso/euromix-to-sbml)](https://github.com/rivm-syso/euromix-to-sbml/blob/main/LICENSE)
[![Build](https://img.shields.io/github/actions/workflow/status/rivm-syso/euromix-to-sbml/build.yml?label=build)](https://github.com/rivm-syso/euromix-to-sbml/actions/workflows/build.yml)
[![Validate](https://img.shields.io/github/actions/workflow/status/rivm-syso/euromix-to-sbml/validate.yml?label=validate)](https://github.com/rivm-syso/euromix-to-sbml/actions/workflows/validate.yml)

This repository contains a re-implementation of the [EuroMix PBK model](https://doi.org/10.1016/j.fct.2020.111440) in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html) and demonstrates how this Antimony model implementation is automatically converted to an annotated Systems Biology Markup Language ([SBML](https://sbml.org/)) file using the [SBML PBK workflow](https://github.com/jwkruisselbrink/sbml-pbk-workflow). The purpose of this repository is to test/demonstrate how to create and publish interoperable PBK models using the EuroMix PBK model as example.

## Reimplementation in Antimony

The model was reimplemented in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html), see file [euromix.ant](model/euromix.ant). Notebook [validate_antimony_model.ipynb](notebooks/validate_antimony_model.ipynb) shows the results of the validation comparison with the results obtained by the R/MCSim/deSolve implementation. The results of the R simulation and the SBML simulation (using libroadrunner in Python) match.

![Model diagram of the EuroMix PBK model](euromix-pbk-model.png)

## Model annotation

Annotations of the model and its element are specified in the file [euromix.annotations.csv](model/euromix.annotations.csv). This annotations file links the different model elements (e.g., compartments and parameters) to ontological terms and specifies the units of measure. For the annotations of modelling terms, the [PBPK ontology](http://obofoundry.org/ontology/pbpko) is used. For the annotation of the units of measure, the [UCUM](https://ucum.org/) notation is adopted.

## SBML conversion and SBML model annotation

Conversion to an annotated SBML file is done automatically using the [SBML PBK workflow](https://github.com/jwkruisselbrink/sbml-pbk-workflow). This workflow follows several steps. It first converts the Antimony model implementation to SBML. Then, it annotates this SBML file using the annotations specified in the [euromix.annotations.csv](model/euromix.annotations.csv) file. After this, it runs validation scripts on the generated SBML file to check for consistency and completeness (e.g, of the units). Finally, it publishes the generated SBML file (and log files) as build artifacts and adds/updates the generated/updated SBML file ([euromix.sbml](model/euromix.sbml)) in this repository.

Notebook [get_sbml_model_info.ipynb](notebooks/get_sbml_model_info.ipynb) shows how information can be retrieved from the annotated SBML model file (e.g., units, differential equations, diagrams, semantic annotations). Notebook [run_sbml_model.ipynb](notebooks/run_sbml_model.ipynb) demonstrates how to run the SBML model.

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

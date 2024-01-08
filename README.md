# Euromix model to SBML

This repository contains a re-implementation of the EuroMix PBK model in antimony and demonstrates how this antimony model can be converted to SBML (using tellurium) and annotated (using sbmlUtils). The purpose of this repository is to test/demonstrate how to create and publish interoperable PBK models using the EuroMix PBK model as example.

## Status

### Reimplementation in antimony

The reimplmentation in antimony is done. The results of the R simulation and the SBML simulation (using libroadrunner in Python) match.

Note that Libroadrunner returns concentrations, also if a species is declared to be `substanceOnly`. Therefore it is necessary to convert the output to amounts by multiplying the concentration with volume of the compartment the species is placed in.

Notebook [test_full_model.ipynb](notebooks/text_full_model.ipynb) shows the results of the validation comparison with the results obtained by the R/MCSim/desolve implementation.

### SBML conversion

A python script to automatically create an SBML file from the Antimony file is created. For this, it uses the Python Tellurium package.

Notebook [test_full_model.ipynb](notebooks/getting_sbml_model_info.ipynb) shows how information can be retrieved from this model (e.g., differential equations, diagrams, semantic annotations) and how to run the SBML model.

### SBML annotation

In progress. Annotation can be done using a separate annotations Excel file. A python script to automatically create an annotated SBML file that combines the Excel file with the SBML file.

A first version of an annotations file is available, demonstrating how to annotate compartments, species and parameters. What remains to be done is to establish the vocabularies/ontologies to use for annotation and decide on the annotation requirements. I.e., what needs to be annotated?

Annotation of units remains to be done altogether. Also, it remains unclear how to distinguish different substances from species (in case of multiple-substance models).

Notebook [test_full_model.ipynb](notebooks/test_model_annotation.ipynb) shows how to annotate the model using an annotations file.

## Running the python code

To run the python code and notebooks, install Jupyter notebook and the the required python packages.

Install notebook, using the command:

```
pip install notebook
```

Install the required python packages using the command:

```
pip install -r requirements.txt
```

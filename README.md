# Euromix model to SBML

This repository contains a re-implementation of the EuroMix PBK model in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html) and demonstrates how this Antimony model implementation can be converted to the Systems Biology Markup Language ([SBML](https://sbml.org/)) using [Tellurium](https://tellurium.analogmachine.org/) and annotated using annotation scripts based on [sbmlUtils](https://github.com/matthiaskoenig/sbmlutils).

The purpose of this repository is to test/demonstrate how to create and publish interoperable PBK models using the EuroMix PBK model as example.

## Model diagram

![Model diagram of the EuroMix PBK model](euromix-pbk-model.png)

## Reimplementation in antimony

The model was reimplemented in [Antimony](https://tellurium.readthedocs.io/en/latest/antimony.html). The results of the R simulation and the SBML simulation (using libroadrunner in Python) match. Notebook [validate_antimony_model.ipynb](notebooks/validate_antimony_model.ipynb) shows the results of the validation comparison with the results obtained by the R/MCSim/desolve implementation.

Note that the [libRoadRunner](https://www.libroadrunner.org/) engine that is used for the python simulations returns concentrations, also if a species is declared to be `substanceOnly`. Therefore it is necessary to convert the output to amounts by multiplying the concentration with volume of the compartment the species is placed in in order to obtain amounts.

## SBML conversion

The python script [ant2sbml.py](src/python/ant2sbml.py) can be used to automatically create an SBML file from the Antimony file. For this, it uses the Python [Tellurium](https://tellurium.analogmachine.org/) package.

Notebook [get_model_info.ipynb](notebooks/get_model_info.ipynb) shows how information can be retrieved from this model (e.g., differential equations, diagrams, semantic annotations). Notebook [run_sbml_model.ipynb](notebooks/run_sbml_model.ipynb) demonstrates how to run the SBML model.

## SBML annotation of terms and units [in progress]

The converted SBML file does not yet contain annotations of terms and units. It is envisioned that this annotation should be done by providing an additional annotations file (either a csv or an Excel file) that describes the terms and units of the elements of the model. The converted SBML file and annotations file are then combined by another (Python) script to automatically create an annotated SBML.

An initial version of an annotations file is available (see, [euromix.annotations.csv](model/euromix.annotations.csv)). This demonstrates how elements of the model are related to ontology terms and units. The script [annotate_sbml_terms.py](src/python/annotate_sbml.py) combines the model file and annotations file to obtain an SBML file with annotated terms. The script [annotate_sbml_units.py](src/python/annotate_sbml_units.py) combines the model file and annotations file to obtain an SBML file with annotated units. Both scripts are heavily inspired by the [sbmlUtils](https://github.com/matthiaskoenig/sbmlutils) package. What remains to be done is to establish the vocabularies/ontologies to use for annotation and decide on the annotation requirements. I.e., what needs to be annotated? Also, it remains unclear how to distinguish different substances from species (in case of multiple-substance models).

## SBML validation [in progress]

Automatic validation can be included to check for model errors, model consistency, consitency of units, and also on more PBK-model specific aspects (such as mass balance). The script [validate_sbml.py](src/python/validate_sbml.py) can be run to run validation checks on the SBML file. This is a first version in which some rudimentary file and consistency checks are performed. This first version is inspired by the [example](https://synonym.caltech.edu/software/libsbml/5.18.0/docs/formatted/python-api/validate_s_b_m_l_8py-example.html) presented in the libSBML documentation.

## Workflow automation [in progress]

The steps to convert the Antimony model to SBML, annotate the SBML file and validate the SBML file are included in an automatic [GitHub workflow](https://docs.github.com/en/actions/using-workflows). This workflow show how automation can reduce the PBK model development to the development of the Antimony model and the annotations file.

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

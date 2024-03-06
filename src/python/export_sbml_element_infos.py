import sys
import argparse
import libsbml as ls
from pathlib import Path
import traceback
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Create a CSV file of the terms of an SBML model")
    parser.add_argument("sbml_file", help="Full path to the SBML file")
    parser.add_argument("-o", "--out", required=False, help="Output file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()
    f_in = Path(args.sbml_file)
    if not f_in.is_file():
        raise FileNotFoundError(f'File {f_in} does not exist.')
    if args.out:
        f_out = Path(args.out)
    else:
        f_out = Path(args.sbml_file).with_suffix('.csv')

    try:
        # Load the document
        document = ls.readSBML(f_in)
        # Get the model
        model = document.getModel()
    except Exception as e:
        print(f'Could not load SBML file {f_in}')
        traceback.print_exc()
        sys.exit(1)

    # Create terms datatable
    df = exportTerms(model)

    # Write data table to csv file
    if not f_out.exists() or args.force:
        df.to_csv(f_out, index=False)
        print(f'{f_in} converted to {f_out}')
    else:
        print(f'{f_out} exists, use -f to force conversion')

# Helper function to extract is-a resource URI
def getTerm(element):
    cvTerms = element.getCVTerms()
    if not cvTerms:
        return None

    for term in cvTerms:
      num_resources = term.getNumResources()
      for j in range(num_resources):
          if term.getQualifierType() == ls.BIOLOGICAL_QUALIFIER and \
              term.getBiologicalQualifierType() == ls.BQB_IS:
              return term.getResourceURI(j)

    return None 

def getUnitString(element):
    return ls.UnitDefinition.printUnits(element.getDerivedUnitDefinition())

def exportTerms(model):
    dt = []
    dt_compartments = getCompartmentTerms(model)
    dt.extend(dt_compartments)
    dt_species = getSpeciesTerms(model)
    dt.extend(dt_species)
    dt_parameters = getParameterTerms(model)
    dt.extend(dt_parameters)
    terms = pd.DataFrame(
        dt,
        columns=["Id", "Type", "Name", "Unit", "URI"]
    )
    return terms

def getCompartmentTerms(model):
    dt = []
    for i in range(0,model.getNumCompartments()):
        c = model.getCompartment(i)
        dt.append([
            c.getId(),
            "compartment",
            c.getName(),
            getUnitString(c),
            getTerm(c)
        ])
    return dt

def getSpeciesTerms(model):
    dt = []
    for i in range(0,model.getNumSpecies()):
        s = model.getSpecies(i)
        dt.append([
            s.getId(),
            "species",
            s.getName(),
            getUnitString(s),
            getTerm(s)
        ])
    return dt

def getParameterTerms(model):
    dt = []
    for i in range(0,model.getNumParameters()):
        s = model.getParameter(i)
        dt.append([
            s.getId(),
            "parameters",
            s.getName(),
            getUnitString(s),
            getTerm(s)
        ])
    return dt

if __name__ == "__main__":
    main()

import os
import sys
import argparse
import traceback
from pathlib import Path
from sbmlutils.metadata.annotator import annotate_sbml

def main():
    parser = argparse.ArgumentParser(description="Annotate the SBML file")
    parser.add_argument("sbml_file", help="Full path to SBML file")
    parser.add_argument("annotations_file", help="Full path to SBML file")
    parser.add_argument("out_file", help="Output file")
    args = parser.parse_args()
    f_in = Path(args.sbml_file)
    f_ann = Path(args.annotations_file)
    f_out = Path(args.out_file)
    if not f_in.is_file():
        raise FileNotFoundError(f'SBML file [{f_in}] does not exist.')
    if not f_ann.is_file():
        raise FileNotFoundError(f'Annotations file [{f_ann}] does not exist.')
    try:
        doc = annotate_sbml(
            source= f_in, 
            annotations_path= f_ann, 
            filepath=f_out
        )
        print(doc.getModel())
    except Exception as e:
        print(f'Error annotating SBML file {f_in}.')
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

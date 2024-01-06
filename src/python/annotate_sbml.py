import os
import sys
import argparse
import traceback
from pathlib import Path
from sbmlutils.metadata.annotator import annotate_sbml

def main():
    parser = argparse.ArgumentParser(description="Convert ant file to sbml")
    parser.add_argument("sbml_file", help="Full path to SBML file")
    args = parser.parse_args()
    f_in = Path(args.sbml_file)
    f_ann = Path(os.path.join(os.path.dirname(f_in), f"{Path(f_in).stem}.annotations.xlsx"))
    print(f_ann)
    f_out = Path(os.path.join(os.path.dirname(f_in), f"{Path(f_in).stem}.annotated.sbml"))
    if not f_in.is_file():
        raise FileNotFoundError(f'SBML file {f_in} does not exist.')
    if not f_ann.is_file():
        raise FileNotFoundError(f'Annotation file {f_ann} does not exist.')
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

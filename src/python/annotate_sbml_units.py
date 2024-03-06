import sys
import argparse
from pathlib import Path
import traceback
import sbml_units_annotator as ua

def main():
    parser = argparse.ArgumentParser(description="Annotate the units of the SBML file with the specifications of the annotations file")
    parser.add_argument("sbml_file", help="Full path to SBML file")
    parser.add_argument("annotations_file", help="Full path to SBML file")
    parser.add_argument("out_file", help="Output file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()
    f_in = Path(args.sbml_file)
    f_ann = Path(args.annotations_file)
    f_out = Path(args.out_file)
    if not f_in.is_file():
        raise FileNotFoundError(f'SBML file [{f_in}] does not exist.')
    if not f_ann.is_file():
        raise FileNotFoundError(f'Annotations file [{f_ann}] does not exist.')
    try:
        if not f_out.exists() or args.force:
            sbml_file = f_in
            annotations_file = f_ann
            out_file = f_out
            annotator = ua.sbmlUnitsAnnotator()
            annotator.annotateUnits(sbml_file, annotations_file, str(out_file))
        else:
            print(f'[{f_out}] already exists, use -f to force conversion')
    except Exception as e:
        print(f'Unit annotation failed')
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

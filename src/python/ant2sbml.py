import sys
import argparse
import tellurium as te
from pathlib import Path
import traceback

def main():
    parser = argparse.ArgumentParser(description="Convert ant file to sbml")
    parser.add_argument("ant_file", help="Full path to ant file")
    parser.add_argument("-f", "--force", action="store_true", help="Overwrite existing")
    args = parser.parse_args()
    f_in = Path(args.ant_file)
    if not f_in.is_file():
        raise FileNotFoundError(f'File {f_in} does not exist.')
    try:
        r = te.loada(args.ant_file)
    except Exception as e:
        print(f'Tellurium could not process {f_in}')
        traceback.print_exc()
        sys.exit(1)
    f_out = Path(args.ant_file).with_suffix('.sbml')
    if not f_out.exists() or args.force:
        r.exportToSBML(f_out)
        print(f'{f_in} converted to {f_out}')
    else:
        print(f'{f_out} exists, use -f to force conversion')

if __name__ == "__main__":
    main()

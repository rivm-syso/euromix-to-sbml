import os
import sys
import argparse
import traceback
import libsbml as ls
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Convert SBML file level and/or version.")
    parser.add_argument("sbml_file", help="Full path to SBML file.")
    level = 3
    version = 1
    args = parser.parse_args()
    f_in = Path(args.sbml_file)
    if not f_in.is_file():
        # Load the document
        raise FileNotFoundError(f'File [{f_in}] does not exist.')
    try:
        document = ls.readSBML(f_in)
        success = document.setLevelAndVersion(level, version)
        if not success:
            print('Error: conversion failed due to the following:')
            document.printErrors()
    except Exception as e:
        print(f'Error converting SBML file [{f_in}] to level {level} version {version}.')
        traceback.print_exc()
        sys.exit(1)
    f_out = os.path.join(os.path.dirname(f_in), f"{Path(f_in).stem}_l{level}_v{version}.sbml")
    ls.writeSBML(document, f_out)

if __name__ == "__main__":
    main()

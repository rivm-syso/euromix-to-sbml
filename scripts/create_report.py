"""
Description:
This script generates a markdown report for the annotated SBML file.

Usage:
Run the script from the command line with the following syntax:
  python scripts/create_report.py

Dependencies:
See requirements.txt (install using `pip install -r requirements.txt`).
"""

import os
from pathlib import Path
import libsbml as ls

from sbmlpbkutils import (
    PbkModelReportGenerator,
    DiagramCreator,
    NamesDisplay
)

MODEL_PATH = './model/'
REPORT_PATH = './docs/'
CITATION_FILE = './CITATION.cff'

def create_report():
    sbml_file = os.path.join(MODEL_PATH, 'euromix.sbml')

    # Load SBML file
    document = ls.readSBML(sbml_file)

    # Ensure report path
    os.makedirs(REPORT_PATH, exist_ok=True)

    # Create report
    sbml_basename = os.path.basename(sbml_file)
    report_file = os.path.join(REPORT_PATH, Path(sbml_basename).with_suffix('.report.md'))
    generator = PbkModelReportGenerator(document)
    generator.create_md_report(report_file)

    # Diagram creator instance
    generator = DiagramCreator()

    # Create diagram without annotations
    output_file = os.path.join(REPORT_PATH, Path(sbml_basename).with_suffix('.svg'))
    generator.create_diagram(
        document,
        output_file,
        names_display = NamesDisplay.ELEMENT_IDS,
        draw_species = True,
        draw_reaction_ids = False
    )

if __name__ == '__main__':
    create_report()

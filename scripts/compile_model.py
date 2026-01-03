"""
Description:
This script creates annotated SBML files from the Antimony PBK model
implementations located in the models folder.

Usage:
Run the script from the command line with the following syntax:
  python scripts/compile_models.py

Dependencies:
See requirements.txt (install using `pip install -r requirements.txt`).
"""

import logging
import os
from pathlib import Path
import uuid
import libsbml as ls
import tellurium as te

from sbmlpbkutils import PbkModelValidator
from sbmlpbkutils import AnnotationsTemplateGenerator
from sbmlpbkutils import PbkModelAnnotator
from sbmlpbkutils import ParametrisationsTemplateGenerator

MODEL_PATH = './model/'
CITATION_FILE = './CITATION.cff'

def create_file_logger(logfile: str) -> logging.Logger:
    logger = logging.getLogger(uuid.uuid4().hex)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(logfile, 'w+')
    formatter = logging.Formatter('[%(levelname)s] - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def compile_model():
    for file in os.listdir(MODEL_PATH):
        if file.endswith('.ant'):
            ant_file = os.path.join(MODEL_PATH, file)
            sbml_file = Path(ant_file).with_suffix('.sbml')

            print(f"Creating SBML file [{sbml_file}] from Antimony file [{ant_file}].")
            r = te.loada(ant_file)
            r.exportToSBML(sbml_file, current=False)

            document = ls.readSBML(sbml_file)

            annotations_file = Path(sbml_file).with_suffix('.annotations.csv')
            if not os.path.exists(annotations_file):
                # create annotations (csv) file if it does not exist
                print(f"Annotations file not found: creating annotations file [{annotations_file}].")
                model = document.getModel()
                annotations_template_generator = AnnotationsTemplateGenerator()
                annotations = annotations_template_generator.generate(model)
                annotations.to_csv(annotations_file, index=False)

            annotations_log_file = Path(sbml_file).with_suffix('.annotations.log')
            annotated_sbml_file = Path(sbml_file).with_suffix('.sbml')
            annotator = PbkModelAnnotator()
            logger = create_file_logger(str(annotations_log_file))
            print(f"Creating annotated SBML file [{annotated_sbml_file}] from SBML file [{sbml_file}] with annotations file [{annotations_file}].")
            annotator.annotate(
                document,
                str(annotations_file),
                CITATION_FILE,
                logger = logger
            )
            ls.writeSBML(document, str(annotated_sbml_file))

            validation_log_file = Path(sbml_file).with_suffix('.validation.log')
            validator = PbkModelValidator()
            logger = create_file_logger(str(validation_log_file))
            validator.validate(str(annotated_sbml_file), logger)

            parametrisations_file = f"./parametrisations/{ Path(sbml_file).stem}_default_params.csv"
            print(f"Creating default parametrisations file [{parametrisations_file}].")
            params_generator = ParametrisationsTemplateGenerator()
            default_params = params_generator.generate(document.getModel())[1]
            default_params.to_csv(parametrisations_file, index=False)

if __name__ == '__main__':
    compile_model()

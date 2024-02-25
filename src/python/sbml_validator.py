import os.path
import libsbml
from sbmlutils.log import get_logger

logger = get_logger(__name__)

class sbmlValidator:
  def __init__(self, ucheck):
    self.ucheck = ucheck

  def validate(self, file):
    if not os.path.exists(file):
      logger.error(f'File {file} does not exist.')
      return

    # Read SBML document
    sbmlDoc  = libsbml.readSBML(file)

    # Check for document errors
    errors = sbmlDoc.getNumErrors()
    seriousErrors = False
    if errors > 0:
      for i in range(errors):
        severity = sbmlDoc.getError(i).getSeverity()
        if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
          logger.error(sbmlDoc.getError(i).getMessage())
          seriousErrors = True
        else:
          logger.warning(sbmlDoc.getError(i).getMessage())

    # Skip consistency checks when serious errors were encountered
    if seriousErrors:
      return

    # Run consistency checks
    sbmlDoc.setConsistencyChecks(libsbml.LIBSBML_CAT_UNITS_CONSISTENCY, self.ucheck)
    failures = sbmlDoc.checkConsistency()
    if failures > 0:
      for i in range(failures):
        severity = sbmlDoc.getError(i).getSeverity()
        if (severity == libsbml.LIBSBML_SEV_ERROR) or (severity == libsbml.LIBSBML_SEV_FATAL):
          logger.error(sbmlDoc.getError(i).getMessage())
        else:
          logger.warning(sbmlDoc.getError(i).getMessage())

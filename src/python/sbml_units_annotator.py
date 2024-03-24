import libsbml as ls
import numpy as np
from sbmlutils.metadata.annotator import ModelAnnotator
from sbmlutils.log import get_logger

logger = get_logger(__name__)

class sbmlUnitsAnnotator:

    # Unit definitions, translating a unit string to the elementary unit
    # compositions following the SBML structure.
    # Unit IDs should comply with vocabulary of QUDT: https://qudt.org/2.1/vocab/unit
    unitDefinitions = [
        {
            "id" : "UNITLESS",
            "synonyms" : [
                "unitless",
                "dimensionless"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_DIMENSIONLESS, "exponent": 1, "multiplier": 1, "scale": 0 }
            ]
        },
        # Amount/volume units
        {
            "id" : "MOL",
            "synonyms" : [
                "mol"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliMOL",
            "synonyms" : [
                "mmol"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 }
            ]
        },
        {
            "id" : "KiloGM",
            "synonyms" : [
                "kg"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 3 }
            ]
        },
        {
            "id" : "GM",
            "synonyms" : [
                "g"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliGM",
            "synonyms" : [
                "mg"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 }
            ]
        },
        {
            "id" : "MicroGM",
            "synonyms" : [
                "ug"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 }
            ]
        },
        {
            "id" : "L",
            "synonyms" : [
                "L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliL",
            "synonyms" : [
                "mL"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -3 }
            ]
        },
        # Concentration units
        {
            "id" : "MicroGM-PER-KiloGM",
            "synonyms" : [
                "ug/kg",
                "ug_per_kg"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
            ]
        },
        {
            "id" : "MilliGM-PER-KiloGM",
            "synonyms" : [
                "mg/kg",
                "mg_per_kg"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
            ]
        },
        {
            "id" : "GM-PER-KiloGM",
            "synonyms" : [
                "g/kg",
                "g_per_kg"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
            ]
        },
        {
            "id" : "MicroGM-PER-GM",
            "synonyms" : [
                "ug/g",
                "ug_per_g"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliGM-PER-GM",
            "synonyms" : [
                "mg/g",
                "mg_per_g"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "GM-PER-GM",
            "synonyms" : [
                "g/g",
                "g_per_g"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MicroGM-PER-L",
            "synonyms" : [
                "ug_per_L",
                "ug/L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliGM-PER-L",
            "synonyms" : [
                "mg_per_L",
                "mg/L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "GM-PER-L",
            "synonyms" : [
                "g_per_L",
                "g/L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MOL-PER-L",
            "synonyms" : [
                "mol_per_L",
                "mol/L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        {
            "id" : "MilliMOL-PER-L",
            "synonyms" : [
                "mmol_per_L",
                "mmol/L"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
            ]
        },
        # Time units
        {
            "id" : "SEC",
            "synonyms" : [
                "seconds",
                "s"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 1, "scale": 1 }
            ]
        },
        {
            "id" : "HR",
            "synonyms" : [
                "hours",
                "h"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 3600, "scale": 1 }
            ]
        },
        {
            "id" : "DAY",
            "synonyms" : [
                "days",
                "d"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 24 * 3600, "scale": 1 }
            ]
        },
        # Rate units
        {
            "id" : "PER-SEC",
            "synonyms" : [
                "per_second",
                "1/sec",
                "1/s",
                "s-1"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 1, "scale": 1 }
            ]
        },
        {
            "id" : "PER-H",
            "synonyms" : [
                "per_hour",
                "1/h",
                "h-1"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
            ]
        },
        {
            "id" : "PER-DAY",
            "synonyms" : [
                "per_day",
                "1/day",
                "1/d",
                "d-1"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 24 * 3600, "scale": 1 }
            ]
        },
        {
            "id" : "MilliMOL-PER-HR",
            "synonyms" : [
                "mmol_per_hour",
                "mmol/h"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
            ]
        },
        {
            "id" : "MOL-PER-HR",
            "synonyms" : [
                "mol/h",
                "mol_per_hour"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
            ]
        },
        {
            "id" : "L-PER-HR",
            "synonyms" : [
                "L_per_h",
                "L/h"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
            ]
        },
        {
            "id" : "DeciM-PER-HR",
            "synonyms" : [
                "dm_per_hour",
                "dm/h"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
            ]
        },
        # Rate per mass units
        {
            "id" : "L-PER-KiloGM-HR",
            "synonyms" : [
                "L_per_kg_h",
                "L.kg-1.h-1"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 },
                { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 },
            ]
        },
        {
            "id" : "MilliMOL-PER-L-HR",
            "synonyms" : [
                "mM_per_L_h",
                "mM.L-1.h-1"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
                { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 },
                { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 3 },
            ]
        },
        # Area units
        {
            "id" : "DeciM2",
            "synonyms" : [
                "dm_square",
                "dm^2",
                "dm2"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_METRE, "exponent": 2, "multiplier": 1, "scale": -1 },
            ]
        },
        # Length units
        {
            "id" : "DeciM",
            "synonyms" : [
                "dm"
            ],
            "units": [
                { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
            ]
        }
    ]

    def annotateUnits(
        self,
        sbml_file,
        annotations_file,
        out_file
    ):
        """Annotate the units of the SBML file using the annotations
        file and write results to the specified out file."""

        # Open SBML document using libSBML
        document = ls.readSBML(sbml_file)
        model = document.getModel()

        # Read annotations file
        df = ModelAnnotator.read_annotations_df(annotations_file)
        df = df.replace(np.nan, None)

        # Read model units
        unitsDictionary = dict()
        for unitDef in model.getListOfUnitDefinitions():
            unitsDictionary[unitDef.getId()] = unitDef

        # Iterate over annotation records
        for index, row in df.iterrows():
            elementId = str(row["element_id"])
            if (elementId and row["unit"] is not None):
                self.setElementUnit(
                    document,
                    row["element_id"],
                    row["sbml_type"],
                    row["unit"],
                    unitsDictionary
                )

        # Write SBML file
        logger.info(f"Writing SBML to file [{out_file}].")
        ls.writeSBML(document, out_file)

    def findUnitDefinition(self, str):
        """Find unit definition matching the provided string."""
        res = None
        for index, value in enumerate(self.unitDefinitions):
            if any(val.lower() == str.lower() for val in value['synonyms']):
                res = value
                break
        return res

    def setElementUnit(
        self,
        doc,
        elementId,
        elementType,
        unitId,
        unitsDictionary
    ):
        """Set element unit of element with specified id and type to the specfied unit."""
        if (elementId):
            el = doc.getElementBySId(elementId)
            if (el is None):
                logger.error(f"Cannot set unit [{unitId}] for [{elementType}] [{elementId}]: element not found!")
                return
            if (not el.isSetUnits()):
                if (unitId not in unitsDictionary):
                    logger.info(f"Adding unit definition for {unitId}")
                    model = doc.getModel()
                    unitDef = self.findUnitDefinition(unitId)
                    if (unitDef is None):
                        logger.error(f"Cannot set unit [{unitId}] for [{elementType}] [{elementId}]: unknown unit definition!")
                        return
                    uDef = model.createUnitDefinition()
                    uDef.setId(unitDef["id"])
                    for unitPart in unitDef["units"]:
                        u = uDef.createUnit()
                        u.setKind(unitPart["kind"])
                        u.setExponent(unitPart["exponent"])
                        u.setMultiplier(unitPart["multiplier"])
                        u.setScale(unitPart["scale"])
                    unitsDictionary[unitId] = uDef
                logger.info(f"Setting unit [{unitId}] for [{elementType}] [{elementId}].")
                uDef = unitsDictionary[unitId]
                el.setUnits(uDef.getId())

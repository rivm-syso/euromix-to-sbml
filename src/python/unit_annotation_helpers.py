import libsbml as ls
import numpy as np
from sbmlutils.metadata.annotator import ModelAnnotator
from sbmlutils.log import get_logger

logger = get_logger(__name__)

# Unit definitions, translating a unit string to the elementary unit
# compositions following the SBML structure
unitDefinitions = [
    {
        "id" : "dimensionless",
        "aliases" : [
            "unitless"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_DIMENSIONLESS, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    # Amount/volume units
    {
        "id" : "mol",
        "aliases" : [
            "mol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mmol",
        "aliases" : [
            "mmol"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "kg",
        "aliases" : [
            "kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "g",
        "aliases" : [
            "g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mg",
        "aliases" : [
            "mg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    {
        "id" : "L",
        "aliases" : [
            "L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mL",
        "aliases" : [
            "mL"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": -3 }
        ]
    },
    # Concentration units
    {
        "id" : "ug_per_kg",
        "aliases" : [
            "ug/kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "mg_per_kg",
        "aliases" : [
            "mg/kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "g_per_kg",
        "aliases" : [
            "g/kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 }
        ]
    },
    {
        "id" : "ug_per_g",
        "aliases" : [
            "ug/g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mg_per_g",
        "aliases" : [
            "mg/g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "g_per_g",
        "aliases" : [
            "g/g"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "ug_per_L",
        "aliases" : [
            "ug/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -6 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mg_per_L",
        "aliases" : [
            "mg/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "g_per_L",
        "aliases" : [
            "g/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_GRAM, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mol_per_L",
        "aliases" : [
            "mol/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    {
        "id" : "mmol_per_L",
        "aliases" : [
            "mmol/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 0 }
        ]
    },
    # Time units
    {
        "id" : "seconds",
        "aliases" : [
            "s"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 1, "scale": 1 }
        ]
    },
    {
        "id" : "hours",
        "aliases" : [
            "h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 3600, "scale": 1 }
        ]
    },
    {
        "id" : "days",
        "aliases" : [
            "d"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": 1, "multiplier": 24 * 3600, "scale": 1 }
        ]
    },
    # Rate units
    {
        "id" : "per_hour",
        "aliases" : [
            "1/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
        ]
    },
    {
        "id" : "per_day",
        "aliases" : [
            "1/day"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 24 * 3600, "scale": 1 }
        ]
    },
    {
        "id" : "mmol_per_hour",
        "aliases" : [
            "mmol/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
        ]
    },
    {
        "id" : "mol_per_hour",
        "aliases" : [
            "mol/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
        ]
    },
    {
        "id" : "L_per_h",
        "aliases" : [
            "L/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
        ]
    },
    {
        "id" : "dm_per_hour",
        "aliases" : [
            "dm/h"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 }
        ]
    },
    # Rate per mass units
    {
        "id" : "L_per_h_per_kg",
        "aliases" : [
            "L/h/kg"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_LITRE, "exponent": 1, "multiplier": 1, "scale": 0 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 },
            { "kind": ls.UNIT_KIND_GRAM, "exponent": -1, "multiplier": 1, "scale": 3 },
        ]
    },
    {
        "id" : "mM_per_h_per_L",
        "aliases" : [
            "mM/h/L"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_MOLE, "exponent": 1, "multiplier": 1, "scale": -3 },
            { "kind": ls.UNIT_KIND_SECOND, "exponent": -1, "multiplier": 3600, "scale": 1 },
            { "kind": ls.UNIT_KIND_LITRE, "exponent": -1, "multiplier": 1, "scale": 3 },
        ]
    },
    # Area units
    {
        "id" : "dm_square",
        "aliases" : [
            "dm^2"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 2, "multiplier": 1, "scale": -1 },
        ]
    },
    # Length units
    {
        "id" : "dm",
        "aliases" : [
            "dm"
        ],
        "units": [
            { "kind": ls.UNIT_KIND_METRE, "exponent": 1, "multiplier": 1, "scale": -1 },
        ]
    }
]

def findUnitDefinition(str):
    """Find unit definition matching the provided string."""
    res = None
    for index, value in enumerate(unitDefinitions):
        if any(val.lower() == str.lower() for val in value['aliases']):
            res = value
            break
    return res


# 
def setElementUnit(
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
        if (not el.isSetUnits()):
            if (unitId not in unitsDictionary):
                logger.info(f"Adding unit definition for {unitId}")
                model = doc.getModel()
                unitDef = findUnitDefinition(unitId)
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
            el.setUnits(unitId)

def annotateUnits(
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
        print(unitDef)
        unitsDictionary[unitDef.getId()] = unitDef

    # Iterate over annotation records
    for index, row in df.iterrows():
        elementId = str(row["element_id"])
        if (elementId and row["unit"] is not None):
            setElementUnit(
                document,
                row["element_id"],
                row["sbml_type"],
                row["unit"],
                unitsDictionary
            )

    # Write SBML file
    logger.info(f"Writing SBML to file [{out_file}].")
    ls.writeSBML(document, out_file)

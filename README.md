# ColaWaterToolbox
An ArcGIS Pro toolbox for the City of Columbia Water GIS Team

# Tools

## Calculate Facility Identifiers

Automatically calculate the facility identifier fields according to the below table:

|     Layer      | Facility ID | Facility ID Index |
|----------------|-------------|-------------------|
| Casings        |     ✅     |         ✅        |
| Control Valves |     ✅     |         ✅        |
| Fittings       |     ✅     |         ✅        |
| Hydrants       |     ✅     |         ✅        |
| Service Lines  |     ✅     |         ❌        |
| Structures     |     ✅     |         ❌        |
| System Valves  |     ✅     |         ❌        |
| Water Mains    |     ✅     |         ✅        |

# Usage

Navigate to the `Catalog Pane` and open the `Toolboxes` dropdown.
Double click on the `ColaWater` toolbox or click the arrow,
then select whichever tool you would like to use from the toolbox's dropdown menu.

# Installation

[Add the toolbox](https://pro.arcgis.com/en/pro-app/latest/arcpy/functions/describe.htm) 
from the [latest release](https://github.com/felix-quark/ColaWaterToolbox/releases).

# Versioning

Versions will take the form `major.minor.patch`.
New tools, behavior changes, new parameters, etc. will result in a major version bump.
Modification of tool contents in a backwards-compatible way will result in a minor version bump.
Changes to documentation, wording, small backward-compatible bugfixes, etc. will result in patch number bump.

# Changes

See [CHANGELOG.md](https://github.com/felix-quark/ColaWaterToolbox/blob/main/CHANGELOG.md).

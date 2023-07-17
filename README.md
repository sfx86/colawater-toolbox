<h1 align="center">ColaWaterToolbox</h1>
<h2 align="center">An ArcGIS Pro toolbox for the City of Columbia Water GIS Team</h2>
<p align="center">
<a href="https://opensource.org/licenses/MPL-2.0"><img alt="License: MPL 2.0" src="https://img.shields.io/badge/license-MPL_2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000"></a>
<a href="https://github.com/felix-quark/ColaWaterToolbox/releases"><img alt="Latest release" src="https://img.shields.io/github/v/release/felix-quark/ColaWaterToolbox"></a>
<a href="https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm"><img alt="Docs: ArcPy reference" src="https://img.shields.io/badge/docs-ArcPy%20reference-purple"></a>
</p>

---

- [Usage](#usage)
- [Installation](#installation)
- [Tools](#tools)
    - [Calculate Facility Identifiers](#calculate-facility-identifiers)
- [Changes](#changes)
- [Roadmap](#roadmap)
- [Versioning](#versioning)

---

# Usage

Navigate to the `Catalog Pane` and open the `Toolboxes` dropdown.
Double click on the `ColaWater.pyt` toolbox or click the arrow,
then double click on whichever tool you would like to use from the toolbox's dropdown menu.

# Installation

Unzip the `ColaWaterToolbox.zip`
from the [latest release](https://github.com/felix-quark/ColaWaterToolbox/releases)
and [add the toolbox](https://pro.arcgis.com/en/pro-app/latest/help/projects/connect-to-a-toolbox.htm) 
to ArcGIS. Make sure all of the associated `.py` files are in the same directory as the `.pyt` file.

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

# Changes

See [CHANGELOG.md](https://github.com/felix-quark/ColaWaterToolbox/blob/main/CHANGELOG.md).

# Roadmap

- 🏗 Water Quality Control Tool
    - 🏗 Validate facility identifier format
    - Deduplicate facility identifiers
    - Ensure values conform to domains
    - Ensure integrated mains have an associated file

# Versioning

Versions will take the form `major.minor.patch`.
New tools, behavior changes, new parameters, etc. will result in a major version bump.
Major versions will always get a new release. 
Anything else is probably just refactoring and does not necessarily need a full release; 
some minor versions will get releases if necessary.
Modification of tool contents in a backwards-compatible way will result in a minor version bump.
Changes to documentation, wording, small backward-compatible bugfixes, etc. will result in patch number bump.

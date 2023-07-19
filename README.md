<h1 align="center">ColaWaterToolbox</h1>
<h2 align="center">ArcGIS geoprocessing tools for Columbia Water</h2>
<p align="center">
<a href="https://opensource.org/licenses/MPL-2.0"><img alt="License: MPL 2.0" src="https://img.shields.io/badge/license-MPL_2.0-brightgreen"></a>
<a href="https://github.com/felix-quark/ColaWaterToolbox/releases"><img alt="Latest release" src="https://img.shields.io/github/v/release/felix-quark/ColaWaterToolbox"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000"></a>
<a href="https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm"><img alt="Docs: ArcPy reference" src="https://img.shields.io/badge/docs-ArcPy%20reference-purple"></a>
</p>

---

- [Usage](#usage)
- [Installation](#installation)
- [Documentation](#documentation)
- [Tools](#tools)
    - [Calculate Facility Identifiers](#calculate-facility-identifiers)
    - [Water Quality Control](#water-quality-control)
- [Changes](#changes)
- [Roadmap](#roadmap)
- [Versioning](#versioning)

---

# Usage

Navigate to the `Catalog Pane` and open the `Toolboxes` dropdown.
Open the `ColaWater.pyt` toolbox, then select a tool from the toolbox's dropdown menu.

# Installation

Download and unzip the `ColaWaterToolbox.zip` from the [latest release][releases]
and [add the toolbox][add-a-toolbox] to ArcGIS. 
Make sure all of the associated `.py` files are in the same directory as the `.pyt` file.

# Documentation

Internal documentation is coming, but for now, see the [ArcPy reference][arcpy-reference].

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

## Water Quality Control

Available quality control checks:
- Check if the associated file exists for all integrated water mains 
- Check if the data source is set and not unknown for all integrated water mains 
- Find incorrectly formatted facility identifiers for all layers

# Changes

See [CHANGELOG.md][changelog].

# Roadmap

- 🏗 Quality Control Tool
    - 🏗 Deduplicate facility identifiers
    - Ensure values conform to domains
    - ✅ Ensure integrated mains have a data source that is not missing or unknown 
    - ✅ Ensure integrated mains have an associated file that exists
    - ✅ Validate facility identifier format
- Documentation (Sphinx)
    - top-level usage instructions
    - coverage of internal APIs

# Versioning

Versions will take the form `major.minor.patch`.
New tools, behavior changes, new parameters, etc. will result in a major version bump and a release.
Modification of tool contents in a backwards-compatible way will result in a minor version bump.
Some minor versions will get releases if necessary.
Changes to documentation, wording, small backward-compatible bugfixes, etc. will result in patch number bump.

[add-a-toolbox]: https://pro.arcgis.com/en/pro-app/latest/help/projects/connect-to-a-toolbox.htm
[arcpy-reference]: https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm
[changelog]: https://github.com/felix-quark/ColaWaterToolbox/blob/main/CHANGELOG.md
[releases]: https://github.com/felix-quark/ColaWaterToolbox/releases

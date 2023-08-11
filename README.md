<h1 align="center">colawater-toolbox</h1>
<h2 align="center">ArcGIS geoprocessing tools for Columbia Water</h2>
<p align="center">
<a href="https://sfx86.github.io/colawater-toolbox/"><img alt="Docs: colawater-toolbox" src="https://img.shields.io/badge/docs-colawater--toolbox-purple"></a>
<a href="https://github.com/sfx86/colawater-toolbox/releases/"><img alt="Latest release" src="https://img.shields.io/github/v/release/sfx86/colawater-toolbox"></a>
<a href="https://opensource.org/licenses/MPL-2.0"><img alt="License: MPL 2.0" src="https://img.shields.io/badge/license-MPL_2.0-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000"></a>
</p>

---

* [Usage](#usage)
* [Installation](#installation)
* [Documentation](#documentation)
* [Tools](#tools)
* [Changes](#changes)
* [Roadmap](#roadmap)
* [Versioning](#versioning)

---

# Usage

Navigate to the `Catalog Pane` and open the `Toolboxes` dropdown.
Open the `colawater.pyt` toolbox, then select a tool from the toolbox's dropdown menu.

# Installation

Download and unzip the `colawater-toolbox.zip` from the [latest release][releases]
and [add the toolbox][add-a-toolbox] named `colawater.pyt` to ArcGIS. 
Make sure to not alter the file structure; the toolbox will not work otherwise.

# Documentation

Documentation for colawater-toolbox is hosted on GitHub pages [here][docs].
Also see the [ArcPy reference][arcpy-reference] for arcpy specific information.

# Tools

<details>
<summary>Append to ART</summary>
Appends new water mains to the Asset Reference Drawing Table using this
field mapping:

| Source      | ART Destination    |
|-------------|--------------------|
| city_file   | FILELOCATIONCITY   |
| DATASOURCE  | DRAWINGTYPE        |
| INSTALLDATE | DRAWINGDATE        |
| FACILIITYID | ASSETFACILITYID    |
| COMMENTS    | SCANNAME           |
| cw2020_file | FILELOCATIONCW2020 |
</details>

<details>
<summary>Calculate Facility Identifiers</summary>
Automatically calculate the facility identifier fields according to the below table:

| Layer          | Facility ID | Facility ID Index |
|----------------|-------------|-------------------|
| Casings        | ✅          | ✅                |
| Control Valves | ✅          | ✅                |
| Fittings       | ✅          | ✅                |
| Hydrants       | ✅          | ✅                |
| Service Lines  | ✅          | ❌                |
| Structures     | ✅          | ❌                |
| System Valves  | ✅          | ❌                |
| Water Mains    | ✅          | ✅                |
</details>

<details>
<summary>Water Quality Control</summary>
Available quality control checks:

* Check if the associated file exists for all integrated water mains 
* Check if the data source is set and not unknown for all integrated water mains 
* Find incorrectly formatted facility identifiers for all layers
</details>

# Changes

See [CHANGELOG.md][changelog].

# Roadmap
* ✅ Calculate Facility Identifiers Tool
* ✅ Append to Art Tool
* 🏗 Quality Control Tool
    * 🏗 Ensure values conform to domains
    * ✅ Deduplicate facility identifiers
    * ✅ Ensure integrated mains have a data source that is not missing or unknown 
    * ✅ Ensure integrated mains have an associated file that exists
    * ✅ Validate facility identifier format

# Versioning

Versions will take the form `major.minor.patch`.
New tools, behavior changes, new parameters, etc. will result in a major version bump and a release.
Modification of tool contents in a backwards-compatible way will result in a minor version bump.
Some minor versions will get releases if necessary.
Changes to documentation, wording, small backward-compatible bugfixes, etc. will result in patch number bump.

[add-a-toolbox]: https://pro.arcgis.com/en/pro-app/latest/help/projects/connect-to-a-toolbox.htm
[arcpy-reference]: https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm
[changelog]: https://github.com/sfx86/colawater-toolbox/blob/main/CHANGELOG.md
[releases]: https://github.com/sfx86/colawater-toolbox/releases
[docs]: https://sfx86.github.io/colawater-toolbox
.. raw:: html

    <h1 align="center">ColaWaterToolbox</h1>
    <h2 align="center">ArcGIS geoprocessing tools for Columbia Water</h2>
    <p align="center">
    <a href="https://opensource.org/licenses/MPL-2.0"><img alt="License: MPL 2.0" src="https://img.shields.io/badge/license-MPL_2.0-brightgreen"></a>
    <a href="https://github.com/felix-quark/ColaWaterToolbox/releases"><img alt="Latest release" src="https://img.shields.io/github/v/release/felix-quark/ColaWaterToolbox"></a>
    <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000"></a>
    <a href="https://pro.arcgis.com/en/pro-app/latest/arcpy/main/arcgis-pro-arcpy-reference.htm"><img alt="Docs: ArcPy reference" src="https://img.shields.io/badge/docs-ArcPy%20reference-purple"></a>
    </p>

----

.. toctree::
    :maxdepth: 2

----

.. include:: docs/source/usage_and_installation.rst

.. include:: docs/source/tools.rst

Documentation
=============

Documentation for ColaWaterToolbox is hosted on GitHub pages at:
https://felix-quark.github.io/ColaWaterToolbox/

.. include:: docs/source/resources.rst

Changes
=======

See [CHANGELOG.md][changelog].

Roadmap
=======

* 🏗 Quality Control Tool
    * 🏗 Deduplicate facility identifiers
    * Ensure values conform to domains
    * ✅ Ensure integrated mains have a data source that is not missing or unknown 
    * ✅ Ensure integrated mains have an associated file that exists
    * ✅ Validate facility identifier format

Versioning
==========

Versions will take the form ``major.minor.patch``.
New tools, behavior changes, new parameters, etc. will result in a major version bump and a release.
Modification of tool contents in a backwards-compatible way will result in a minor version bump.
Some minor versions will get releases if necessary.
Changes to documentation, wording, small backward-compatible bugfixes, etc. will result in patch number bump.

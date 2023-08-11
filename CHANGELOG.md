# 3.2.0

# Minor Changes

* Added duplicate facility identifier check to Water Quality Control

* Fixes to tool behavior:
    * Fix SQL error in Append to ART
    * Fix row update length in Calculate Facility Identifiers
    * Index object IDs properly in duplicate FID qc

* Fixes to API implementation:
    * Fix workspace generation
    * Catch more exceptions in fallible decorator
    * Make attr.process work with more types

# Patch Changes

* Update error messages
Tools
=====

Append to ART
-------------

Appends new water mains to the Asset Reference Drawing Table using this 
field mapping:

=========== ==================
Source      ART Destination
=========== ==================
city_file   FILELOCATIONCITY
DATASOURCE  DRAWINGTYPE
INSTALLDATE DRAWINGDATE
FACILIITYID ASSETFACILITYID
COMMENTS    SCANNAME
cw2020_file FILELOCATIONCW2020
=========== ==================

Calculate Facility Identifiers
------------------------------

Automatically calculate the facility identifier fields according to the
below table:

============== =========== =================
Layer          Facility ID Facility ID Index
============== =========== =================
Casings        ✅          ✅
Control Valves ✅          ✅
Fittings       ✅          ✅
Hydrants       ✅          ✅
Service Lines  ✅          ❌
Structures     ✅          ❌
System Valves  ✅          ❌
Water Mains    ✅          ✅
============== =========== =================

Water Quality Control
---------------------

Available quality control checks: 

* Check if the associated file exists for all integrated water mains 
* Check if the data source is set and not unknown for all integrated water mains 
* Find duplicate facility identifiers
* Find incorrectly formatted facility identifiers for all layers

Tools
=====

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
* Find incorrectly formatted facility identifiers for all layers

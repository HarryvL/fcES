# fcES-workbench
Finite element analysis of beams on elastic foundation and axi-symmetrically loaded cylindrical tanks and silos in [FreeCAD](https://freecad.org)

### Background
fcES is based on an exact finite element for the bending of beams on elastic foundation as described in the documentation included in this repository.

<img src="https://github.com/HarryvL/fcES/blob/main/pictures/fcES_window.png" height="400"/>

### Prerequisites
* FreeCAD >= v0.19

### Installation
1. Create a fcES-workbench directory in the FreeCAD Mod directory, the location of which can be found by typing App.getUserAppDataDir() in the FreeCAD python console.
1. Copy the entire fcES-workbench repository into this new fcES-workbench directory.
1. Restart FreeCAD
1. If all went well, the fcES workbench should now be an option in the FreeCAD workbench dropdown menu

```bash
App.getUserAppDataDir()
├── Mod
│   ├── fcES-workbench
│   │   ├── control files
│   │   │   ├── case_19a.inp
│   │   │   └── etc.
│   │   ├── documentation
│   │   │   └── Beam_on_Elastic_Foundation.pdf
│   │   ├── freeCAD files
│   │   │   ├── test1.FCStd
│   │   │   └── etc.
│   │   ├── icons
│   │   │   └── fcFEM.svg
│   │   ├── output files
│   │   │   ├── test1.es
│   │   │   └── etc.
│   │   ├── pictures
│   │   │   ├── beam_results.png
│   │   │   └── etc.
│   │   ├── source code
│   │   │   ├── .gitignore
│   │   │   └── fcES.FCMacro
│   │   ├── user_interface
│   │   │   └── fcES.ui
│   │   ├── .gitignore
│   │   │
│   │   ├── Init.py
│   │   │
│   │   └── etc.
│   │
```

<img src="https://github.com/HarryvL/fcES/blob/main/pictures/beam_results.png" height="600"/><img>

### Dependencies
fcES only imports numpy and matplotlib, which are already available in the FreeCAD environment.

### Documentation
See the document entitled Beam_on_Elastic_Foundation.pdf in the documentation folder of this repository.

<img src="https://github.com/HarryvL/fcES/blob/main/pictures/tank_results.png" height="600"/><img>

### Current Limitations
N/A 

### Licence information

Copyright (c) 2024 - Harry van Langen <hvlanalysis@gmail.com>  


This program is free software; you can redistribute it and/or modify  
it under the terms of the GNU Lesser General Public License (LGPL)    
as published by the Free Software Foundation; either version 2 of     
the License, or (at your option) any later version.                   
for detail see the LICENCE text file.                                 
                                                                         
This program is distributed in the hope that it will be useful,       
but WITHOUT ANY WARRANTY; without even the implied warranty of        
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         
GNU Library General Public License for more details.                  
                                                                         
You should have received a copy of the GNU Library General Public     
License along with this program; if not, write to the Free Software   
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  
USA                                                                   

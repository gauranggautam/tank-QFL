
Information on the LabView examples
-----------------------------------



0. About the README.txt file

This file was last modified on February the 2nd of 2005.
The LabView examples here described were created with LabView 6.1.



1. Installation for Windows

Copy the following files into a directory of your choice:
 - ShamrockCIF.dll               (the Shamrock SDK interface library)
 - usbi2cio.dll                  (USB dynamic library)
 - UsbI2cIoDep.dll               (USB dynamic library)
 - ATMCD32D.DLL                  (Andor PCI card dynamic library)
 - ExampleShamrockBasic.vi       (example 1)
 - ExampleGratingsWavelength.vi  (example 2)
 - ExampleAll.vi                 (example 3)

The examples look, by default, for DETECTOR.INI in the previous 
directory ("..\"):

This file is needed to successfully locate any Shamrock connected through the
Andor PCI card. They can be copied to any location as long as the path passed 
into "ShamrockInitialize(char * IniPath)" is updated accordingly. The specific 
.cof and .rbf files depend on what Andor PCI card has been installed.

Copy the VI libraries into your ".\user.lib" library/directory under your LabView 
directory (e.g. "C:\Program Files\National Instruments\LabVIEW 6.1\user.lib"), so 
that on the Diagram panel you have access to the Shamrock libraries under the 
"User Libraries" in the "Function Palette". The VI library files are:
 - Shamrock.llb                  (LabView library)
 - ShamrockActions.llb           (LabView library)
 - AndorUtils.llb                (LabView library)

Copy the following file into "root:\WINDOWS\system32":
 - atshamrock.dll                (the Shamrock SDK dynamic library)



2. The examples

ExampleShamrockBasic: initializes the Shamrock, reads the spectrometer's parameters 
and shuts the system down.

ExampleGratingsWavelength: includes ExampleShamrockBasic and the gratings and 
wavelength functions.

ExampleAll: includes ExampleShamrockBasic and all the Shamrock SDK functions.



3. LabView libraries

The examples here supplied do not call any functions in the interface library 
directly (ShamrockCIF.dll). The calls are done through the three LabView library 
files supplied with the examples (AndorUtils.llb, Shamrock.llb and 
ShamrockActions.llb). The libraries can be accessed through a right click on the 
Diagram window, and "Functions">>"User Libraries". 

Under "User Libraries" there are 3 submenus: 
 - AndorUtils: 2 subroutines, one for translating the return value of the 
   Shamrock SDK functions into a string describing the return value, and the other 
   to translate 0 or 1 (int) into TRUE or FALSE (string);
 - Shamrock: information retrieval subroutines; 
 - ShamrockAction: subroutines to send commands to the Shamrock. 

The "Context Help" can be used to see an overview of the inputs and outputs of the 
different functions. 

The Shamrock VI libraries are not locked so that the user has access to the 
examples building blocks' details.

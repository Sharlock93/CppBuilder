**Welcome**

This is my fist plugin
A very Simple plugin to make Makefiles, still in pre-Alpha testing

makes simple make files..

**Keys**

Ctrl+Alt+M while a C++ file is open will run the command on windows, Haven't tested it on Mac or Linux yet...
the command will make a Makefile in the same directory of the C++ file.

For now, make a copy of the CppBuilder.sublime-settings file in your User folder (Accessed through Prefrences > Browse Packages) and make changes to the files and test it out...

**Goals**  

-Add per project setting handling.  

-Gather the different files under different folders, i.e.: .o into obj folder, .cpp into src...etc.  

-Helpful tool.  




**Update History**

v 0.0.4 (New)
-Added a Default main_file name if one is not give. (output.exe on windows, ouput.out on others)
-removed some code, and it looks cleaner now.
-Tested on Mac & Linux...working but fine.

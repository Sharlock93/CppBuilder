**Note**: as a university student, work on this project will be slow, sorry.

Welcome
======
This is my fist plugin
A very Simple plugin to make Makefiles, still in pre-Alpha testing
makes simple make files..

Install
========
1. Use Package Control
    - Search for **CppBuilder**
2. or git clone the repo, and copy it to Packages/CppBuilder

Use
======
<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>M</kbd> <br/>While a C++ file is open will run the command on windows, Haven't tested it on Mac or Linux yet...
the command will make a Makefile in the same directory of the C++ file.

#####settings
You have some options that you can change, either per project (I will explain down below) or for single files:


If you change the settings in ***project*.sublime-project** file, then the settings only apply to that project only, however if you change the **CppBuilder.sublime-settings**, the changes apply to every file. i.e: a file outside a project.

**Note**: please set the workspace setting before anything else, this is required, for the New C++ Project command to work.

These are the basic settings you can change:
```javascript
    //per project settings (can also be set to apply to every file)
    
    //library directories (prefixed by -L in Makefile)
    "lib_dir": [
    "path/to/some/lib/folder",
    "path/to/someother/lib/folder"
    ],

    //library names used in your project, ORDER matters
    //(prefixed with -l in the makefile)
    "lib_names": [
    "somelibname",
    "anotherlibname"
    ],

    //header directory, .h/hpp files
    //(for projects this is set to the header folder created with the 
    //New C++ project command, so put your headers there if using a project)
    "include_dir": [
    "path/to/header",
    "path/another/header"
    ],

    //where to get the .cpp files
    //(set to src when in a project)
    "src_dir": "",

    //output folders
    //the name of the file to generate (the final executable )
    //(for project named after the project)
    "main_file": "",
    
    //where to put the intermediate .o files
    //this is to make sure we don't recompile everything from scratch
    //if not needed
    //(set to obj folder while in project)
    "obj_dir": "",

    //where to build the final executable
    //by default is in the same folder for a single .CPP file
    //(for project set to the build folder)
    "build_dir": "",


    //compiler
    "cc": "g++",

//============================================================

    //additional flags for the compiler
    "additional_flags": [
        "Wall",
        "std=gnu++11",
        "D__USE_MINGW_ANSI_STDIO=1"
    ],

    //Default Project Settings
    //this should only be set by using CppBuilder.sublime-settings
    //this is where all your Projects are made
    //SET THIS or the plugin will not work, or it can even mess up stuff
    "workspace_dir":""
```

#Goals 
- Running the Project after compiling.
- Just getting peole to use it and work out any bugs found ;)

##Update History
- v 0.0.11(New)
    -   lost local git folder, rebuild from scratch 
    -   added folder management.

- v 0.0.8  

    - Added a simple message test when installing package.  
    - Added an option to make a folder for the object files.  
    - fixed some bugs.  
    - should be able to make simple makefiles without errors.  


- v 0.0.4
    - Added a Default main_file name if one is not give. (output.exe on windows, ouput.out on others)
    - removed some code, and it looks cleaner now.
    - Tested on Mac & Linux...working but fine.

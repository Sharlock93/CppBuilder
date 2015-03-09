**Note**: as a university student, work on this project will be slow, sorry.

Welcome
======
This is my fist plugin so there might be bugs :)
I have only tested this one windows thus far, Linux and Mac come later.

This is a simple plugin that will generate a project folder for you, and will also generate a Makefile to use with GNU Make.
It can also **Run** your project.

This meant as a very simple project management system, there are bugs, and it can only handle one generated binary file.
(Does that even make sense?!)

Install
========
1. Use Package Control
    - Search for **CppBuilder**
2. or git clone the repo, and copy it to Packages/CppBuilder

Use
======
<kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>M</kbd> <br/>While a C++ file is open will run the command on windows, Haven't tested it on Mac or ~~Linux~~ yet...
the command will make a Makefile in the same directory of the C++ file.
**Note**: so far I can only compile and run while in a project, i will add single file compile and run some other time.

#####Project
goto **Project > C++ Builder > New C++ Project** to create a new project, an Input panel will come up and you can type in the name of your project, Then it will make the list of folders (build, header, obj, src), it will prompt you to agree for each folder, just click Yes to all of them. (This might be removed later.)

######Keys (While new project is open)
1. <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>N</kbd> : Generate Makefile (There must be at least one cpp file in your src folder).
2. <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>Z</kbd> : Build the Project (This will just run make in the folder).
3. <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>C</kbd> : Build & Run Project (No Input) (Running the project assuming there is no input required from the keyboard, useful for simple stuff).
4. <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>X</kbd> : Build & Run (Console) (Running the project assuming it requires input, the output from the program is not captured by Sublime text, the Console window will pause).
5. <kbd>Ctrl</kbd>+<kbd>Alt</kbd>+<kbd>V</kbd> : Clean Project (Will run make clean).

#####settings
You have some options that you can change, either per project (I will explain down below) or for single files:


If you change the settings in ***project*.sublime-project** file, then the settings only apply to that project only, however if you change the **CppBuilder.sublime-settings**, the changes apply to every file. i.e: a file outside a project.

**Note**: please set the workspace setting before anything else, this is required, for the New C++ Project command to work.

**Note**: For Linux you must also set **terminal_emu** and **terminal_opts** for your own linux distro

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
    
    //what to remove, example 'obj\*.o'
    //this just a simple way to clean up, you can add
    //more as required, remember, only supply what to delete
    //the delete command is added internally based on platform
    "clean" : [], 

//============================================================

//Linux Specific options:

    //command that opens a new terminal
    "terminal_emu":"x-terminal-emulator",
    "terminal_opts": [
        "-x"
    ],

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
- Running the Project after compiling. (Done)
- Building & Running a single C++ file. (New)
- Just getting peole to use it and work out any bugs found ;)


##Update History
- v 0.2.3 (New)
    - Now should support Linux.
    - Removed a few commands and Keyboard shortcuts as the where not required.

##Update History
- v 0.2.00 (Old)
    - Added Project Creation.
    - Added Project Building.
    - Added Project Execution.
    - This could be the first version that has some uses. :D ( I will build it as I go along)

- v 0.0.11
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

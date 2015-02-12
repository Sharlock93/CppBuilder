import sys
import os
import glob
import sublime


class Makerfile():

    def __init__(self, settings, src=None, obj=None, build=None, header=None):
        self.makefile = ""

        self.variables = {}
        self.output_file = "output"
        self.string_template = ""

        if sys.platform == "win32":
            self.output_file += ".exe"

        self.src = src
        self.obj = obj
        self.build = build
        self.header = header
        self.sources = self.get_source_files(self.src)
        self.settings = settings

    def make_file(self):

        if not self.sources:
            print("No souces provided")
            return None

        self.makefile += self.handle_variable(self.settings)
        self.make_string_template()

        self.makefile += "\n"

        self.makefile += self.str_main_file()

        self.makefile += "\n\n{}\n".format(self.str_recipe_target())

        self.makefile += self.str_make_clean()
        return self.makefile

    def handle_variable(self, settings):  # variable
        var_string = ""
        if self.header:
            string = " ".join(self.settings.get("include_dir"))
            header = "$(addprefix -I,$(HDR_DIR))"
            self.variables["HDR_DIR"] = string
            self.variables["HEADER"] = header

            var_string += "HDR_DIR = {}\nHEADER = {}\n".format(string, header)

        if settings.get("lib_dir") and settings.get("lib_names"):
            lib_dir = " ".join(settings.get("lib_dir"))
            lib = "$(addprefix -L, $(LIB_DIR))"
            self.variables["LIB_DIR"] = lib_dir
            self.variables["LIB"] = lib

            libnames = " ".join(settings.get("lib_names"))
            libn = "$(addprefix -l,$(LIB_NAMES))"
            self.variables["LIB_NAMES"] = libnames
            self.variables["Library"] = libn

            var_string += "LIB_DIR = {}\nLIB = {}\n".format(lib_dir, lib)
            var_string += "LIB_NAMES = {}\nLIBRARY = {}\n".format(
                libnames, libn)

        if settings.get("additional_flags"):
            self.variables["CCOPTION"] = " ".join(
                settings.get("additional_flags"))
            self.variables["FLAGS"] = "$(addprefix -,$(FLAGS))"

            var_string += "CCOPTION = {}\n".format(
                self.variables.get("CCOPTION"))
            var_string += "FLAGS = $(addprefix -,$(CCOPTION))\n"

        if settings.get("cc"):
            self.variables["CC"] = settings.get("cc")
            var_string += "CC = {}\n".format(settings.get("cc"))
        else:
            var_string += "CC = {}\n".format("g++")

        if settings.get("projec_name"):
            if sys.platform == "win32":
                self.variables["main_file"] = settings.get(
                    "main_file") + ".exe"
            else:
                self.variables["main_file"] = settings.get(
                    "main_file") + ".out"

        elif settings.get("main_file"):
            if sys.platform == "win32":
                self.variables["main_file"] = settings.get(
                    "main_file") + ".exe"
            else:
                self.variables["main_file"] = settings.get(
                    "main_file") + ".out"
        else:
            if sys.platform == "win32":
                self.variables["main_file"] = "output.exe"
            else:
                self.variables["main_file"] = "output.out"

        if self.obj:
            var_string += "OBJ_DIR = {}\n".format(self.obj)

        if self.sources:
            self.variables["OBJ"] = ""
            for x in self.sources:
                self.variables["OBJ"] += x.replace(".cpp", ".o") + " "

            var_string += "OBJ = {}\n".format(self.variables.get("OBJ"))

        if self.build:
            self.variables["BUILD_DIR"] = self.build
            var_string += "BUILD_DIR = {}\n".format(self.build)

        if self.src:
            self.variables["SRC_DIR"] = self.src
            var_string += "SRC_DIR = {}\n".format(self.src)

        return var_string

    def str_main_file(self):
        string = ""
        if self.build:
            string += "{2}\\"  # build dir

        string += "{0}: {1} \n\t $(CC) "

        if self.variables.get("FLAGS"):
            string += "$(FLAGS) "

        if self.build:
            string += "{1} -o {2}\\{0} "
        else:
            string += "{1} -o {0} "

        if self.variables.get("LIB"):
            string += "$(LIB) $(LIBRARY)"

        if self.obj:
            objs = "$(addprefix $(OBJ_DIR)\,$(OBJ))"
        else:
            objs = "$(OBJ)"

        main_exe = string.format(
            self.variables.get("main_file"), objs, "$(BUILD_DIR)")
        return main_exe

    def str_make_clean(self):
        temp = "clean: \n\t"

        print(temp)

        del_command = "rm "

        if sublime.platform() == 'windows':
            del_command = "del /Q "

        print(bool(self.settings.get("clean")))
        if bool(self.settings.get("clean")):
            for i in self.settings.get("clean"):
                if sublime.platform() != 'windows':
                    i = i.replace('\\', '\\/')
                temp += del_command + i + "\n\t"
        else:
            print('hello')
            if sublime.platform() != 'windows':
                print('hello2')
                temp += del_command + "$(OBJ_DIR)'\/'*.o\n\t"
                temp += del_command + "$(BUILD_DIR)'\/'*.exe\n"
            else:
                temp += del_command + "$(OBJ_DIR)\\*.o\n\t"
                temp += del_command + "$(BUILD_DIR)\\*.exe\n"

        return temp

    def get_source_files(self, src_dir):
        back_out = False
        if src_dir:
            try:
                print(os.getcwd())
                os.chdir(src_dir)
                back_out = True
            except FileNotFoundError:
                print("Couldn't find the Folder: ", src_dir)

        file_sources = glob.glob("*.cpp")

        if back_out:
            os.chdir("..")
        return file_sources

    def str_recipe_target(self):
        tempmk = ""
        if self.sources:
            for x in self.sources:
                tempmk += self.string_template.format(
                    x.replace(".cpp", ".o"), x, "$(OBJ_DIR)", "$(SRC_DIR)")
                tempmk += "\n\n"
            return tempmk
        else:
            print("No Source files found")
            return None

    # generate a template string based on the variables passed for the object
    def make_string_template(self):
        tmp = ""
        if self.obj:
            tmp += "{2}\\"  # obj dir

        tmp += "{0}: "  # object .o

        if self.src:
            tmp += "{3}\\"  # src dir

        tmp += "{1} \n\t $(CC) $(FLAGS) -c "  # recipe for object

        # print(self.src)

        if self.src:
            tmp += "{3}\\"

        tmp += "{1} "

        if self.obj:
            tmp += "-o {2}\\{0} "
        else:
            tmp += "-o {0} "

        if self.variables.get("HEADER"):
            tmp += "$(HEADER)"

        self.string_template = tmp

    # setter methods
    def set_src(self, src_dir):
        self.src = src_dir

    def set_obj(self, obj_dir):
        self.obj = obj_dir

    def set_build(self, build_dir):
        self.build = build_dir

    def set_header(self, header_dir):
        self.header = header_dir

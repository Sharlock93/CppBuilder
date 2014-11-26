import sublime
import sublime_plugin
import os
import glob
import fileinput
import sys
import shutil
import zipfile


class Makerfile():
    target = {}  # for targets
    recipe = {}
    variables = {}
    output_file = "output"

    def __init__(self):
        Makerfile.target = {}
        Makerfile.recipe = {}
        Makerfile.variables = {}
        Makerfile.output_file = "output"

        if sys.platform == "win32":
            Makerfile.output_file += ".exe"
        else:
            Makerfile.output_file += ".out"

    def insert_target(self, rule_name, *rule_values):
        Makerfile.target[rule_name] = rule_values

    def get_rule(self, rule_name):
        try:
            return Makerfile.target[rule_name]
        except KeyError:
            print("couldn't find a key with that name")
            return None

    def __str__(self):
        pass

    def getrange(self, lists):
        for i, k in enumerate(lists):
            if k.endswith(".h"):
                return i
            if k.endswith(".hpp"):
                return i

    def generate_make(self):
        f = open("Makefile", "w")
        f.write(self.makestr())
        f.close()

    def insert_variable(self, var_name, var_value):
        var_name = var_name.upper()
        if Makerfile.variables.get(var_name) != None:
            if Makerfile.variables[var_name] == var_value:
                return
            Makerfile.variables[var_name] += var_value
        else:
            Makerfile.variables[var_name] = var_value

    def insert_command(self, tar, command):

        # check for existence & no duplication for the commands
        if (Makerfile.recipe.get(tar) != None and (Makerfile.recipe.get(tar).find(command) == -1)):
            Makerfile.recipe[tar] += " " + command
            return

        Makerfile.recipe[tar] = command

    def makestr(self):
        settings = sublime.load_settings("CppBuilder.sublime-settings")

        make = ""

        # insert varibales
        for x in Makerfile.variables:
            if x == "SOURCE":
                make += x + " = " + "$(wildcard *.cpp)"
            else:
                make += x + " = " + Makerfile.variables[x]

            make += "\n"

        obj_dir = settings.get("obj_dir")

        if obj_dir:
            make += "OBJ = $(subst .cpp,.o,$(addprefix " + \
                obj_dir + "/,$(SOURCE)))\n"
        else:
            make += "OBJ = $(subst .cpp,.o,$(SOURCE))\n"

        make += "\n"

        # if Makerfile.output_file:
        mf = settings.get("main_file")  # main file

        if mf:
            make += mf + ": $(OBJ) \n\t$(CC) $(FLAGS) $(OBJ) -o " + mf
        else:
            make += Makerfile.output_file + \
                ": $(OBJ) \n\t$(CC) $(FLAGS) $(OBJ) -o " + \
                Makerfile.output_file

        if Makerfile.variables.get("LIBS"):
            make += " $(LIBS)"

        if Makerfile.variables.get("LIBS_DIR"):
            make += " $(LIBS_DIR)"

        make += "\n\n"

        # insert the rules
        for targ in Makerfile.target:
            strtmp = " ".join(Makerfile.target[targ])
            if obj_dir:
                make += obj_dir + "/" + targ + ": " + strtmp
            else:
                make += targ + ": " + strtmp

            if Makerfile.recipe.get(targ) != None:
                make += "\n\t " + Makerfile.recipe[targ]

            make += "\n\n"

        return make

    def generate_recipe(self, var_list):
        if type(var_list) != list:
            cmd = ["g++", "-MM", "-MG", "-std=gnu++11", var_list]
            output = s.check_output(cmd)
            return output

    def process_cpp(self, list_cpp):

        print(list_cpp)

        obj_dir = sublime.load_settings(
            "CppBuilder.sublime-settings").get("obj_dir")

        for l in list_cpp:
            mktarg = l.replace(".cpp", ".o")

            self.insert_target(mktarg, l)
            self.insert_command(mktarg, "$(CC) $(FLAGS) -c " + l)

            if obj_dir:
                self.insert_command(mktarg, "-o " + obj_dir + "/" + mktarg)

            if Makerfile.variables.get("HDRDIR"):
                self.insert_command(mktarg, "$(HDRDIR)")

    def variable_process(self, settings):

        if settings.get("include_dir"):
            self.insert_variable(
                "HDRDIR", "-I" + " -I".join(settings.get("include_dir")))

        self.insert_variable("CC", "g++")

        if settings.get("lib_names"):
            self.insert_variable(
                "LIBS", "-l" + " -l".join(settings.get("lib_names")))

        if settings.get("additional_flags"):
            self.insert_variable(
                "FLAGS", "-" + " -".join(settings.get("additional_flags")) + " ")

        if settings.get("lib_dir"):
            self.insert_variable(
                "LIBS_DIR", "-L" + " -L".join(settings.get("lib_dir")))


class CppBuilderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        stgname = "CppBuilder.sublime-settings"
        settings = sublime.load_settings(stgname)
        maker = Makerfile()
        source_files = glob.glob("*.cpp")

        os.chdir(os.path.dirname(self.view.file_name()))

        print(os.path.isdir(settings.get("obj_dir")))

        if not os.path.isdir(settings.get("obj_dir")):
            os.mkdir(settings.get("obj_dir"))

        maker.insert_variable("source", source_files)
        maker.variable_process(settings)
        maker.process_cpp(source_files)
        maker.generate_make()
        oas = sublime.active_window().open_file("Makefile")


def plugin_loaded():
    ls = sublime.packages_path()
    p = os.path.isfile(ls + "//User//CppBuilder.sublime-settings")
    if not p:
        k = os.chdir(ls)
        os.chdir("..")
        os.chdir("Installed Packages")
        t = zipfile.ZipFile("CppBuilder.sublime-package")
        out = t.extract("CppBuilder.sublime-settings", path=ls + "//User//")

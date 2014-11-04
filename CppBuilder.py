import sublime
import sublime_plugin
import re
import os
import glob
import fileinput
import sys
import subprocess as s


class Makerfile():
    target = {}  # for targets
    recipe = {}
    variables = {}

    def __init__(self):
        Makerfile.target = {}
        Makerfile.recipe = {}
        Makerfile.variables = {}

    def insert_rule(self, rule_name, *rule_values):
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

    def _generate_make(self):
        f = open("Makefile", "w")
        f.write(self.test())
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

    def test(self):
        make = ""

        # insert varibales
        for x in Makerfile.variables:
            if(type(Makerfile.variables[x]) is list):
                if x == "HDRDIR":
                    make += x + " = -I" + " -I".join(Makerfile.variables[x])
                else:
                    make += x + " = " + " ".join(Makerfile.variables[x])

            else:
                make += x + " = " + Makerfile.variables[x]

            make += "\n"

        # woot.insert_variable("OBJ", "$(subst .cpp,.o,$(SOURCE))")
        make += "OBJ = $(subst .cpp,.o,$(SOURCE))\n"

        make += "\n"

        settings = sublime.load_settings("CppBuilder.sublime-settings")

        mf = settings.get("main_file")  # main file
        make += mf + ": $(OBJ) \n\t$(CC) $(FLAGS) $(OBJ) -o " + mf

        if Makerfile.variables.get("LIBS"):
            make += " $(LIBS)"

        if Makerfile.variables.get("LIBS_DIR"):
            make += " $(LIBS_DIR)"

        make += "\n\n"

        # insert the rules
        for l in Makerfile.target:
            make += l + ": " + " ".join(Makerfile.target[l])
            if Makerfile.recipe.get(l) != None:
                make += "\n\t" + Makerfile.recipe[l]

            make += "\n\n"

        return make

    def generate_recipe(self, var_list):
        if type(var_list) != list:
            cmd = ["g++", "-MM", "-MG", "-std=gnu++11", var_list]
            output = s.check_output(cmd)
            return output

    def process_cpp(self, list_cpp):

        print(list_cpp)

        for l in list_cpp:
            mktarg = l.replace(".cpp", ".o")

            self.insert_rule(mktarg, l)
            self.insert_command(mktarg, "$(CC) $(FLAGS) -c " + l)

            if Makerfile.variables.get("HDRDIR"):
                self.insert_command(mktarg, "$(HDRDIR)")


class CppBuilderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        test = sublime.load_settings("CppBuilder.sublime-settings")

        os.chdir(os.path.dirname(self.view.file_name()))

        res = glob.glob("*.cpp")
        if res:
            print(res)

        woot = Makerfile()
        name = test.get("main_file")

        woot.insert_variable("source", res)

        if test.get("include_dir"):
            woot.insert_variable("HDRDIR", test.get("include_dir"))

        if test.get("lib_names"):
            woot.insert_variable(
                "LIBS", "-l" + " -l".join(test.get("lib_names")))

        if test.get("additional_flags"):
            woot.insert_variable(
                "FLAGS", "-" + " -".join(test.get("additional_flags")) + " ")

        woot.insert_variable("CC", "g++")

        woot.insert_variable(
            "FLAGS", "-std=gnu++11 -D__USE_MINGW_ANSI_STDIO=1")

        if test.get("lib_dir"):
            woot.insert_variable(
                "LIBS_DIR", "-L" + " -L".join(test.get("lib_dir")))

        woot.process_cpp(res)
        woot._generate_make()


class TestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print(Makerfile.target)
        print("\nrec>>>>\n")
        print(Makerfile.recipe)
        print("\nvar>>>>\n")
        print(Makerfile.variables)

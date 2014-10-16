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
        pass

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
        test = 0
        lea = "dh"

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
        if Makerfile.target.get(tar) != None:
            Makerfile.recipe[tar] = command

    def test(self):
        make = ""

        # insert varibales
        for x in Makerfile.variables:
            if(type(Makerfile.variables[x]) is list):
                if x == "HDRDIR":
                    make += x + " = -I" + " -I".join(Makerfile.variables[x])
                    # print(" -I".join(Makerfile.variables[x]))
                else:
                    make += x + " = " + " ".join(Makerfile.variables[x])

            else:
                make += x + " = " + Makerfile.variables[x]

            make += "\n"

        make += "\n"

        settings = sublime.load_settings("Example.sublime-settings")

        make += settings.get("main_file") + \
            " : $(OBJ) \n\t g++ $(OBJ) -o " + \
            settings.get("main_file") + "\n\n"

        # insert the rules
        for l in Makerfile.target:
            make += l + ": " + " ".join(Makerfile.target[l])

            if Makerfile.recipe.get(l) != None:
                make += "\n\t" + Makerfile.recipe[l]

            make += "\n\n"

        return make

    def generate_recipe(self, var_list):
        if type(var_list) != list:
            cmd = ["g++", "-MM", "-MG", var_list]
            output = s.check_output(cmd)
            return output

    def process_cpp(self, list_cpp):
        for l in list_cpp:
            les = self.generate_recipe(
                l).decode().replace(" \\\r\n", "").strip().split(":")[1].strip()
            les = les.split(" ")
            mach = self.getrange(les)
            les = " ".join(les[0:mach])

            self.insert_rule(l.replace(".cpp", ".o"), les)
            if Makerfile.variables.get("HDRDIR"):
                self.insert_command(
                    l.replace(".cpp", ".o"), "$(COMMANDC) " + les + " $(HDRDIR)")
            else:
                self.insert_command(
                    l.replace(".cpp", ".o"), "$(COMMANDC) " + les)


class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        test = sublime.load_settings("Example.sublime-settings")

        os.chdir(os.path.dirname(self.view.file_name()))

        res = glob.glob("*.cpp")
        woot = Makerfile()
        name = test.get("main_file")
        print(res)
        woot.insert_variable("source", res)
        woot.insert_variable("OBJ", "$(subst .cpp,.o,$(SOURCE))")
        print(test.get("include_dir"))
        if test.get("include_dir"):
            woot.insert_variable("HDRDIR", test.get("include_dir"))
        woot.insert_variable("commandC", "g++ -c -std=gnu++11")
        woot.process_cpp(res)
        woot._generate_make()


class TestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        print(Makerfile.target)

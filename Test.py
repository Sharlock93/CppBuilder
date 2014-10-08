import sublime
import sublime_plugin
import re
import os
import glob
import fileinput
import sys
import subprocess as s


def wtf(file_name):
    cmdline = ["g++", "-MM", "-MG", file_name]
    cmd = s.Popen(
        cmdline, stdout=s.PIPE, universal_newlines=True, stderr=s.PIPE, shell=True)
    stdo, stder = cmd.communicate()

    if(stdo == None):
        print("hello")
    if(stder == None):
        print("woot")
    print(stdo.strip())
    print(stder.strip(), end='')


def insertrule(rule_name, *args):
    rule_name += " : "
    for arg in args:
        rule_name += arg + " "

    print(rule_name)


class Makerfile():
    target = {}  # for targets
    # commands = {}
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

    def _generate_make(self):
        f = open("Makefile", "w")

        strings = ""

        for x in Makerfile.variables:
            var_list = Makerfile.variables[x]
            strings += x
            if(type(var_list) is list):
                for i in var_list:
                    strings += '"' + i + '"' + " "

                strings += "\n"
            else:
                strings += var_list + "\n"

        # strings += "\n#=================targets=========================\n\n"

        for i in Makerfile.target:
            # print(i)
            print("".join(Makerfile.target[i]))
            strings += i + ": " + "".join(Makerfile.target[i]) + "\n"

        return strings

        f.flush()
        f.close()

    # def generate_target(self, file_name):
    #     cmdline = ["g++", "-MM", "-MG", file_name]
    #     fliesa = s.check_output(cmdline)
    #     fliesa = fliesa.decode().split(":")
    #     self.insert_rule(fliesa[0], fliesa[1].replace("\\\r\n", "").strip())

    def insert_variable(self, var_name, var_value):
        var_name = "$(" + var_name.upper() + ")"
        if Makerfile.variables.get(var_name) != None:
            Makerfile.variables[var_name] += var_value
        else:
            Makerfile.variables[var_name] = var_value


class ExampleCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        test = sublime.load_settings("Example.sublime-settings")

        os.chdir(os.path.dirname(self.view.file_name()))

        res = glob.glob("*.cpp")
        woot = Makerfile()
        name = test.get("main_file")
        print(name)

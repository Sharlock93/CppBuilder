import sublime
import sublime_plugin
import os
import glob
import fileinput
import sys
import shutil
import zipfile

from CppBuilder.MakerClass import Makerfile


class CppBuilderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        stgname = "CppBuilder.sublime-settings"
        settings = sublime.load_settings(stgname)
        maker = Makerfile()
        os.chdir(os.path.dirname(self.view.file_name()))

        source_files = glob.glob("*.cpp")

        if (settings.get("obj_dir") and not os.path.isdir(settings.get("obj_dir"))):
            os.mkdir(settings.get("obj_dir"))

        maker.insert_variable("source", source_files)
        maker.variable_process(settings)
        maker.process_cpp(source_files)
        maker.generate_make()
        oas = sublime.active_window().open_file("Makefile")
        os.access

class TestCommand(sublime_plugin.TextCommand):

    def run(self, edit):
       tes = os.path.expandvars("$USERPROFILE//CppBuilder//").replace("\\", "//")
       os.chdir(tes)
       print(os.listdir())
       print("hello world")

def plugin_loaded():
    #check if settigns file exists if not, extract one from the package file downloaded.
    ls = sublime.packages_path()
    p = os.path.isfile(ls + "//User//CppBuilder.sublime-settings")
    if not p:
        k = os.chdir(ls)
        os.chdir("..")
        os.chdir("Installed Packages")
        t = zipfile.ZipFile("CppBuilder.sublime-package")
        out = t.extract("CppBuilder.sublime-settings", path=ls + "//User//")

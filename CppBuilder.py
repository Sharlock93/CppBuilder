import sublime
import sublime_plugin
import os
import glob
import fileinput
import sys
import shutil
import zipfile
import threading
import functools

from CppBuilder.MakerClass import Makerfile
from CppBuilder.ProjectHandler import ProjectHandler

class CppBuilderCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        stgname = "CppBuilder.sublime-settings"
        settings = sublime.load_settings(stgname)

        file_path = os.path.dirname(self.view.file_name())

        obj = settings.get("obj_dir")
        header = settings.get("include_dir")
        build = settings.get("build_dir")
        
        print(obj, header, build)

        maker = Makerfile(settings, file_path, obj, build, header)
        f = open(file_path + "//Makefile", "w")
        f.write(maker.make_file())
        f.close()
        oas = sublime.active_window().open_file("Makefile")


class NewCppCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().show_input_panel(
            "Enter Project Name: ", "", make_project, None, None
        )


def plugin_loaded():
    # check if settigns file exists if not, extract one from the package file
    # downloaded.
    ls = sublime.packages_path()
    p = os.path.isfile(ls + "//User//CppBuilder.sublime-settings")
    if not p:
        k = os.chdir(ls)
        os.chdir("..")
        os.chdir("Installed Packages")
        t = zipfile.ZipFile("CppBuilder.sublime-package")
        out = t.extract("CppBuilder.sublime-settings", path=ls + "//User//")


def make_project(test):
    proj = ProjectHandler(test)
    proj.create_base_project()

class MakeProjectCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        stgname = "CppBuilder.sublime-settings"
        settings = self.view.settings()
        default_settings = sublime.load_settings(stgname)

        proj_base = default_settings.get("workspace_dir")
        proj_base += "\\{}".format(settings.get('main_file'))
                
        maker = Makerfile(settings, "src", "obj", "build", "header")
        makefile = proj_base + "\\Makefile"
        
        f = open(makefile, "w")
        f.write(maker.make_file())
        f.close()
        
        sublime.active_window().open_file(makefile)

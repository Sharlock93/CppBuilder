import sublime
import sublime_plugin
import os

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

        maker = Makerfile(settings, file_path, obj, build, header)
        f = open(file_path + "//Makefile", "w")
        f.write(maker.make_file())
        f.close()
        sublime.active_window().open_file("Makefile")


class NewCppCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().show_input_panel(
            "Enter Project Name: ", "", make_project, None, None
        )


def make_project(test):
    proj = ProjectHandler(test)
    proj.create_base_project()

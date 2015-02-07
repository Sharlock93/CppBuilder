import sublime
import sublime_plugin
import os
import json

from CppBuilder.MakerClass import Makerfile


class MakeProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = self.get_settings().get("settings")
        proj_base = self.view.window().folders()[0]

        src = proj_base + "\\src"

        maker = Makerfile(settings, src, "obj", "build", "header")
        makefile = proj_base + "\\Makefile"

        f = open(makefile, "w")
        f.write(maker.make_file())
        f.close()

        sublime.active_window().open_file(makefile)

    def get_settings(self):
        if self.view.settings().get('main_file'):
            return self.view.settings()
        else:
            project_folder = self.view.window().folders()[0]
            proj_name = os.path.basename(project_folder)
            setting_name = "\\{}.sublime-project".format(proj_name)

            return self.load_json(project_folder + setting_name)

    def load_json(self, json_file):
        f = open(json_file)
        j = json.load(f)

        print()

        f.close()
        return j

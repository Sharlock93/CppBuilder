import sublime
import sublime_plugin
import os
import json
import sys
from CppBuilder.MakerClass import Makerfile


class MakeProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        settings = self.get_settings()
        if settings:
            proj_base = self.view.window().folders()[0]

            src = proj_base
            makefile = proj_base

            if sys.platform.startswith('linux'):
                src += "/src"
                makefile += "/Makefile"
            else:
                 src += "\\src"
                 makefile += "\\Makefile"

            maker = Makerfile(settings, src, "obj", "build", "header")

            make_string = maker.make_file()

            if sys.platform.startswith('linux'):
                make_string = make_string.replace('\\', '/')
            f = open(makefile, "w")
                
            f.write(make_string)

            f.close()

            sublime.active_window().open_file(makefile)
        sublime.status_message("Error in settings file")

    def get_settings(self):
        project_folder = self.view.window().folders()[0]
        proj_name = os.path.basename(project_folder)
        setting_name = "\\{}.sublime-project".format(proj_name)

        if sys.platform.startswith('linux'):
            setting_name = setting_name.replace('\\', '/')

        print(project_folder + setting_name)
        return self.load_json(project_folder + setting_name)

    def load_json(self, json_file):
        f = open(json_file)
        j = None
        try:
            j = json.load(f).get('settings')

        except Exception:
            print("Error Parsing Project File, there is a bug in the file")
        finally:
            f.close()

        return j

import sublime
import sublime_plugin
import subprocess
import os
from subprocess import CalledProcessError

class BuildProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.edit_token = edit.edit_token
        # i think you have to keep the edit object alive, what?
        sublime.set_timeout_async(self.build(edit)) 

    def build(self, edit):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        os.chdir(p)
        try:
            output = subprocess.check_output("make", universal_newlines = True, stderr = subprocess.STDOUT, shell = True)
            self.show_output(output)
        except CalledProcessError as e:
            self.show_output(e.output)
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        
        panel = self.view.window().create_output_panel("CppBuilder")
        edit = panel.begin_edit(self.edit_token, "")
        panel.insert(edit, 0, message)
        panel.end_edit(edit)
        self.view.window().run_command('show_panel', {'panel': 'output.CppBuilder'})


class RunProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.edit_token = edit.edit_token
        # i think you have to keep the edit object alive, what?
        sublime.set_timeout_async(self.run_proj(edit)) 

    def run_proj(self, edit):
        p = self.view.window().folders()[0]

        proj_name = os.path.basename(p)

        if sublime.platform() == 'windows':
            proj_name += '.exe'
        else:
            proj_name += '.out'

        curdir = os.getcwd()
        os.chdir(p)
        
        try:
            subprocess.call("build\\" + proj_name, universal_newlines = True, stderr = subprocess.STDOUT)
        except CalledProcessError as e:
            self.show_output(e.output)
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        edit = panel.begin_edit(self.edit_token, "")
        panel.insert(edit, 0, message)
        panel.end_edit(edit)
        self.view.window().run_command('show_panel', {'panel': 'output.CppBuilder'})

class CleanProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.edit_token = edit.edit_token
        # i think you have to keep the edit object alive, what?
        sublime.set_timeout_async(self.clean(edit)) 

    def clean(self, edit):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        os.chdir(p)
        try:
            output = subprocess.check_output("make clean", universal_newlines = True, stderr = subprocess.STDOUT, shell = True)
            self.show_output(output)
        except CalledProcessError as e:
            self.show_output(e.output)
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        
        panel = self.view.window().create_output_panel("CppBuilder")
        edit = panel.begin_edit(self.edit_token, "")
        panel.insert(edit, 0, message)
        panel.end_edit(edit)
        self.view.window().run_command('show_panel', {'panel': 'output.CppBuilder'})

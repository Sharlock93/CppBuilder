import sublime
import sublime_plugin
import subprocess
import os
import shutil
import zipfile
from subprocess import CalledProcessError, Popen, PIPE

try:
    from .edit import Edit as Edit
except:
    from edit import Edit as Edit


class BuildProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.output = ''
        sublime.set_timeout_async(self.build)
        sublime.set_timeout_async(self.printoutput)

    def build(self):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        os.chdir(p)
        try:
            self.output = output = subprocess.check_output(
                "make", universal_newlines=True, stderr=subprocess.STDOUT, shell=True)
        except CalledProcessError as e:
            self.show_output(e.output)
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        with Edit(panel) as edit:
            edit.insert(0, message)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.CppBuilder'})

    def printoutput(self):
        self.show_output(self.output)


class BuildRunProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.output = ''
        sublime.set_timeout_async(self.buildrun)
        sublime.set_timeout_async(self.printoutput)

    def buildrun(self):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        proj_name = os.path.basename(p)

        if sublime.platform() == 'windows':
            proj_name += '.exe'
        else:
            proj_name += '.out'

        os.chdir(p)

        self.proj_name = proj_name

        try:
            self.output = "====================Build====================\n"
            self.output += subprocess.check_output(
                "make", universal_newlines=True, stderr=subprocess.STDOUT, shell=True)
            process = Popen(
                ["build\\" + self.proj_name], shell=False, creationflags=subprocess.CREATE_NEW_CONSOLE)
        except CalledProcessError as e:
            self.output = "====================Error====================\n"
            self.output += e.output + "\n" + e.returncode
        except FileNotFoundError as e:
            self.show_output(
                "Could Not Excute File: " + e.strerror + " [{}]".format(self.proj_name))
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        with Edit(panel) as edit:
            edit.insert(0, message)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.CppBuilder'})

    def printoutput(self):
        self.show_output(self.output)


class BuildRunCheckProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.output = ''
        sublime.set_timeout_async(self.buildruncheck)
        sublime.set_timeout_async(self.printoutput)

    def buildruncheck(self):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        proj_name = os.path.basename(p)

        if sublime.platform() == 'windows':
            proj_name += '.exe'
        else:
            proj_name += '.out'

        os.chdir(p)

        self.proj_name = proj_name

        try:
            self.output = "====================Build====================\n"
            self.output += subprocess.check_output(
                "make", universal_newlines=True, stderr=subprocess.STDOUT, shell=True)
            self.output += "==================== Run ====================\n"
            self.output += subprocess.check_output(
                ["build\\" + self.proj_name], universal_newlines=True, shell=True, stderr=subprocess.STDOUT)
        except CalledProcessError as e:
            self.output = "====================Error====================\n"
            self.output += e.output + "\n" + e.returncode
        except FileNotFoundError as e:
            self.show_output(
                "Could Not Excute File: " + e.strerror + " [{}]".format(self.proj_name))
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        with Edit(panel) as edit:
            edit.insert(0, message)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.CppBuilder'})

    def printoutput(self):
        self.show_output(self.output)


class RunProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.set_timeout_async(self.run_proj)

    def run_proj(self):
        p = self.view.window().folders()[0]
        proj_name = os.path.basename(p)
        curdir = os.getcwd()
        os.chdir(p + "\\build")

        if sublime.platform() == 'windows':
            proj_name += '.exe'
        else:
            proj_name = './' + proj_name + '.out'

        self.proj_name = proj_name

        try:
            process = Popen(
                [proj_name], creationflags=subprocess.CREATE_NEW_CONSOLE)
            sublime.status_message("Run.....DONE")
        except FileNotFoundError as e:
            self.show_output(
                "Could Not Excute File: " + e.strerror + " [{}]".format(self.proj_name))
            process.terminate()
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        with Edit(panel) as edit:
            edit.insert(0, message)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.CppBuilder'})


class CleanProjectCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.output = ''
        sublime.set_timeout_async(self.clean)
        sublime.set_timeout_async(self.printoutput)

    def clean(self):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        os.chdir(p)
        try:
            self.output = "====================Clean====================\n"
            self.output += subprocess.check_output(
                "make clean", universal_newlines=True, stderr=subprocess.STDOUT, shell=True)

        except CalledProcessError as e:
            self.output = "====================Error====================\n"
            self.output += e.output + "\n" + e.returncode
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")
        with Edit(panel) as edit:
            edit.insert(0, message)
        self.view.window().run_command(
            'show_panel', {'panel': 'output.CppBuilder'})

    def printoutput(self):
        self.show_output(self.output)


class RunFileOutCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.sharex = ''
        sublime.set_timeout_async(self.run_single_output)
        sublime.set_timeout_async(self.remove_ex, 1000)

    def run_single_output(self):
        p = self.view.window().folders()[0]
        p += "\\build\\{}".format(os.path.basename(p))
        self.sharex = self.get_bat_ex()

        try:
            command = ["cmd", "/C", self.sharex, p]
            subprocess.Popen(command, shell=False, universal_newlines=True,
                             creationflags=subprocess.CREATE_NEW_CONSOLE)
        except CalledProcessError as e:
            print(e.output)
            process.terminate()

    def remove_ex(self):
        os.remove(self.sharex)

    def get_bat_ex(self):
        ls = sublime.packages_path()
        curdir = os.getcwd()
        os.chdir(ls)
        os.chdir("..")
        os.chdir("Installed Packages")
        t = zipfile.ZipFile("CppBuilder.sublime-package")
        out = t.extract("sharEx.bat")
        os.chdir(curdir)
        return out

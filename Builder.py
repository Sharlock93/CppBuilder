import sublime
import sublime_plugin
import subprocess
import os
import sys
import zipfile

from subprocess import CalledProcessError

try:
    from subprocess import CREATE_NEW_CONSOLE
except Exception as e:
    pass

try:
    from .edit import Edit as Edit
except:
    from edit import Edit as Edit


class BuildProjectCommand(sublime_plugin.TextCommand):

    # build the project by running make

    def run(self, edit):
        self.output = ''
        sublime.set_timeout_async(self.build)
        sublime.set_timeout_async(self.printoutput)

    def build(self):
        p = self.view.window().folders()[0]
        curdir = os.getcwd()
        os.chdir(p)
        try:

            self.output = subprocess.check_output(
                                                "make",
                                                universal_newlines=True,
                                                stderr=subprocess.STDOUT,
                                                shell=True
                                                )
        except CalledProcessError as e:
            self.output = e.output
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")

        with Edit(panel) as edit:
            edit.insert(0, message)

        self.view.window().run_command(
                                    'show_panel',
                                    {'panel': 'output.CppBuilder'}
                                    )

    def printoutput(self):
        self.show_output(self.output)


class CleanProjectCommand(sublime_plugin.TextCommand):

    # clean the project by running 'make clean'

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
                                                "make clean",
                                                universal_newlines=True,
                                                stderr=subprocess.STDOUT,
                                                shell=True
                                                )

        except CalledProcessError as e:
            self.output = "====================Error====================\n"
            self.output += str(e.output) + "\nExit Code: " + str(e.returncode)
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

    # Build the project then run it, assuming the project doesn't need input
    # from the terminal/command-line

    def run(self, edit):
        self.output = ''

        # async run the build so sublime doesn't hang

        sublime.set_timeout_async(self.buildruncheck)
        sublime.set_timeout_async(self.printoutput)

    def buildruncheck(self):

        # get the folder so we can also retrive the name of the project
        p = self.view.window().folders()[0]

        curdir = os.getcwd()
        proj_name = os.path.basename(p)

        if sublime.platform() == 'windows':
            proj_name += '.exe'
        else:
            proj_name += '.out'

        os.chdir(p)  # go to our project folder

        self.proj_name = proj_name

        try:
            self.output = "====================Build====================\n"

            self.output += subprocess.check_output(
                                                "make",
                                                universal_newlines=True,
                                                stderr=subprocess.STDOUT,
                                                shell=True
                                                )

            self.output += "==================== Run ====================\n"

            if sublime.platform() == 'windows':
                self.output += subprocess.check_output(
                                                ["build\\" + self.proj_name],
                                                universal_newlines=True,
                                                shell=True,
                                                stderr=subprocess.STDOUT)
            else:
                self.output += subprocess.check_output(
                                                ["build/" + self.proj_name],
                                                universal_newlines=True,
                                                shell=True,
                                                stderr=subprocess.STDOUT)

        except CalledProcessError as e:

            self.output = "====================Error====================\n"
            self.output += str(e.output) + "\nExit Code: " + str(e.returncode)

        except Exception as e:

            self.show_output(
                            "Could Not Excute File: " +
                            str(e.strerror) +
                            " [{}]".format(self.proj_name)
                            )
        finally:
            os.chdir(curdir)

    def show_output(self, message):
        panel = self.view.window().create_output_panel("CppBuilder")

        with Edit(panel) as edit:
            edit.insert(0, message)

        self.view.window().run_command(
                                    'show_panel',
                                    {'panel': 'output.CppBuilder'}
                                    )

    def printoutput(self):
        self.show_output(self.output)


class RunFileOutCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.set_timeout_async(self.run_single_output)
        sublime.set_timeout_async(self.remove_ex, 1000)

    def run_single_output(self):
        p = self.view.window().folders()[0]

        if sublime.platform() == 'windows':
            p += "\\build\\{}.exe".format(os.path.basename(p))
        else:
            p += "/build/{}.out".format(os.path.basename(p))

        self.sharex = self.get_bat_ex()
        command = self.get_shell_command()

        command.append(self.sharex)
        command.append(p)
        process = 0

        try:
            if sublime.platform() == 'window':

                process = subprocess.Popen(
                                        command,
                                        shell=False,
                                        universal_newlines=True,
                                        creationflags=CREATE_NEW_CONSOLE
                                        )
            else:
                # go to the build directory and run the command
                curdir = os.curdir
                os.chdir(os.path.dirname(p))
                process = subprocess.Popen(command)
                os.chdir(curdir)

        except CalledProcessError as e:
            print(e.output)
            process.terminate()

    def remove_ex(self):
        os.remove(self.sharex)

    def get_bat_ex(self):
        # the zip file will have scripts for running the executable
        # so we have to extract them based on the platform

        ls = sublime.packages_path()
        curdir = os.getcwd()
        os.chdir(ls)
        os.chdir("..")
        os.chdir("Installed Packages")
        t = zipfile.ZipFile("CppBuilder.sublime-package")

        if sublime.platform() == 'windows':
            out = t.extract("sharEx.bat")
        else:
            # course on linux based system we have to change the permission
            out = t.extract("sharEx.sh")
            os.chmod(out, 0o777)  # this an over kill for a simple script

        os.chdir(curdir)
        return out

    def get_shell_command(self):
        if sublime.platform() == 'windows':
            return ["cmd", "/C"]
        else:
            settings = sublime.load_settings("CppBuilder.sublime-settings")
            options = settings.get('terminal_opts')
            options.insert(0, settings.get('terminal_emu'))
            return options

        # p = self.view.window().folders()[0]
        # if sublime.platform() == 'windows':
        #     p += "/" + os.path.basename(p) + ".sublime-project"
        # else:
        #     p += "\\" + os.path.basename(p) + ".sublime-project"

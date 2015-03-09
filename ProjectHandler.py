import sublime
import os
import json
import sys

class ProjectHandler:
    # contains the workspace folder defined in settings file

    def __init__(self, project_name="temp"):
        self.project_data = {
            "folders": [],
            "settings": {
                "include_dir": ["header"],
                "lib_dir": [],
                "lib_names": [],
                "main_file": project_name,
                "cc": "g++",
                "additional_flags": [
                    "Wall",
                    "std=gnu++11",
                    "D__USE_MINGW_ANSI_STDIO=1"
                ],
            },
            "build_systems": []
        }

        self.workspace_folder = sublime.load_settings(
            "CppBuilder.sublime-settings").get("workspace_dir")
        self.project_base_folder = project_name

    def create_base_project(self):
        folders = {"header", "src", "obj", "build"}
        self.chmk_workspace_dir()

        for i in folders:
            self.add_folder(i)

        self.project_data["folders"].append({"path": self.get_project_dir()})
        sublime.active_window().set_project_data(self.project_data)
        self.mk_subl_proj()

    def add_folder(self, folder):
        folder_full_path = self.get_project_dir() + "\\" + folder

        if sys.platform.startswith('linux'):
            folder_full_path = folder_full_path.replace('\\', '/')

        print(folder_full_path)
        self.make_dir(folder_full_path)

    def chmk_workspace_dir(self):
        return self.make_dir(self.workspace_folder)

    # make a folder(can be a path, creates everything that doesn't exist)
    def make_dir(self, dir_name):
        dir_exist = self.check_dirs(dir_name)


        if type(dir_exist) is str:
            makes =  sublime.ok_cancel_dialog(
                "The directory '{}' doesnt exist.\
                \n Want me to create the path?".format(dir_exist)
            )

            if makes:
                os.makedirs(dir_name)
                mkdir_success = self.check_dirs(dir_name)
                if type(mkdir_success) is str:
                    sublime.status_message(
                        "Could Not create folder {},\
                        possible permission problems.".format(dir_exist)
                    )
                    sublime.error_message(
                        "Directory creation failed.\n Possible permission error."
                    )
                    
                    return False
                else:
                    sublime.status_message(
                        "Done Creating Workspace {}.".format(dir_name)
                    )
                    return True

            else:
                sublime.status_message("User Cancelled.")
                return False

        return False

    # check if the dirpath exists
    def check_dirs(self, dirpath):
        # lets test every part of the path and check where we stop having a
        # folder
        split_path = self.split_paths(dirpath)

        # an absoulte path, must start at root drive, (this needs more testing)
        if sys.platform.startswith('linux'):
            os.chdir('//')
        elif sys.platform.startswith('win'):
            os.chdir('\\')

        # returns true or folder name where the path stops existing
        if os.path.isdir(dirpath):
            return True
        else:
            for i in split_path:
                try:
                    os.chdir(i)
                except Exception:
                    return i

    def get_wrkspc_dir(self):
        return self.workspace_folder

    def get_project_dir(self):
        wrkspacedir = self.workspace_folder + "\\" + self.project_base_folder
        if sys.platform.startswith('linux'):
            wrkspacedir = wrkspacedir.replace('\\', '/')

        return wrkspacedir

    def mk_subl_proj(self):
        project_file_name = self.project_base_folder + ".sublime-project"
        project_file_name = self.get_project_dir() + "\\" + project_file_name

        if sys.platform.startswith('linux'):
            project_file_name = project_file_name.replace('\\', '/')


        with open(project_file_name, "w") as f:
            json.dump(self.project_data, f, indent=4, sort_keys=True)
    
    def split_paths(self, path):
        if sys.platform.startswith('linux'):
            split = path.split('/')
            split.remove('')
            return split
        
        if sys.platform.startswith('win'):
            split = path.split('\\')
            return split

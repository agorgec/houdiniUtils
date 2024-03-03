import hou
import sys, json, getpass, os

sys.path.append("/usr/lib/python3/dist-packages/")
import yaml

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from pydrive import files


class Publisher:

    data_path = "/mnt/Projects/py_dev/rnd/g_drive/hip/geo/" + "data.json"

    def _create_drive_instance(self):

        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        return drive

    def _get_file(self):

        file_path = hou.parm("file").evalAsString()
        if os.path.isfile(file_path):
            return file_path
        else:
            hou.ui.displayMessage("File doesn't exist")
            return None

    def upload(self):

        file_path = self._get_file()

        if file_path is not None:
            drive = self._create_drive_instance()
            file_name = file_path.split("/")[-1]
            file = drive.CreateFile({"title": file_name})
            file.SetContentFile(file_path)
            file.Upload()

            data = dict()
            new_data = {
                file_name: {
                    "title": file["title"],
                    "id": file["id"],
                    "author": getpass.getuser(),
                }
            }

            if os.path.isfile(self.data_path):
                with open(self.data_path, "r") as file:
                    data = json.load(file)
                    data.update(new_data)
                with open(self.data_path, "w") as file:
                    json.dump(data, file, indent=4)
            else:
                data = {
                    file_name: {
                        "title": file["title"],
                        "id": file["id"],
                        "author": getpass.getuser(),
                    }
                }
                with open(self.data_path, "w") as file:
                    json.dump(data, file, indent=4)

    def download(self):

        index = hou.parm("asset").eval()
        asset = hou.parm("asset").menuLabels()[index]
        download_dir = hou.parm("download_dir").eval()

        print(download_dir)
        data = dict()

        with open(self.data_path, "r") as file:
            data = json.load(file)

        id = data[asset]["id"]

        drive = self._create_drive_instance()
        file = drive.CreateFile({"id": id})
        file.GetContentFile(download_dir + asset)

        geo = hou.node("/obj").createNode("geo", asset.split(".")[1])
        read = geo.createNode("file")
        read.parm("file").set(download_dir + asset)

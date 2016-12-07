from __future__ import absolute_import, print_function
from builtins import input

from os import path
import getpass
import pyosf

class OSFSync(object):
    """High-level class for synchronizing subfolders with OSF project files"""

    def __init__(self, osf_project_file = "osfsync.proj"):
        """ If project file exists, use this & connect.
        """
        self.osf_project_file = path.realpath(osf_project_file)
        if path.isfile(osf_project_file):
            try:
                self._project = pyosf.Project(project_file=self.osf_project_file)
            except pyosf.AuthError:
                self._project = None
        else:
            self._project = None

        if self._project is not None:
            print("Connected to OSF project '{0}'.".format(self._project.project_id))

        self.osf_username = None
        self.osf_project_id = None
        self.sync_folder = None

    def is_connected(self):
        """Returns True if connected to project"""

        return self._project is not None


    def set_connection_details(self,osf_username=None, osf_project_id=None, sync_folder=None):
        """Ask via command line for all required details that are specified.
        """

        if osf_username is None:
            osf_username = input("OSF Username: ")
        self.osf_username = osf_username

        if osf_project_id is None:
            osf_project_id = input("OSF project id: ")
        self.osf_project_id = osf_project_id

        if sync_folder is None:
            sync_folder = input("Sync subfolder [default='data']: ")
            if len(sync_folder)<1:
                sync_folder = 'data'
        self.sync_folder = path.realpath(sync_folder)


    def get_auth_token(self, password=None):
        """Gets the auth token

        see also pyosf documentation"""

        if password is None:
            password = getpass.getpass()
        try:
            session = pyosf.Session(username=self.osf_username, password=password)
        except pyosf.AuthError:
            print("Could not login to OSF.")
            return False

    def connect(self):
        """connect with OSF project"""

        if self.osf_username is None:
            self.set_connection_details()

        try:
            session = pyosf.Session(username=self.osf_username)
        except pyosf.AuthError:
            print("Could not login to OSF. Auth token might be required.")
            self._project = None
            return False

        try:
            osf_proj = session.open_project(self.osf_project_id)
            self._project = pyosf.Project(project_file=self.osf_project_file,
                                      root_path=self.sync_folder,
                                      osf=osf_proj)
        except:
            print("Could not connect to OSF project '{0}'.".format(
                            self.osf_project_id))
            self._project = None
            return False

        print("Connected to OSF project '{0}'.".format(self.osf_project_id))


    def sync(self):
        """returns the changes"""
        changes = self._project.get_changes()
        changes.apply()
        return changes

def osf_sync_files():
    """High-level OSF sync function to be used via command line.
    """

    osf = OSFSync()

    if not osf.is_connected():
        osf.connect()
        if not osf.is_connected():
            osf.get_auth_token()
            osf.connect()

    sync_info = osf.sync()
    print(sync_info)


if __name__ == "__main__":
    osf_sync_files()

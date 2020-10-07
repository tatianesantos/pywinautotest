"""Generic utilities that are used throughout the framework."""
import json
import os
import random
import re
import string
import uuid

from PIL import ImageGrab

import psutil

# pywinauto packages
from pywinauto import handleprops, timings
from pywinauto.application import Application


class Utils:
    """Utilities module."""

    def __init__(self, logger):
        self.logger = logger

    def random_string(self, length=32):
        """Generate a string randomly.

        Parameters
        ----------
        length
            Length of the string to be generated. Default: 32

        Returns
        -------
        string
            A random string with given length.
        """
        letters = string.ascii_lowercase + string.ascii_uppercase
        return "".join(random.choice(letters) for i in range(length))

    def delete_file(self, file_path):
        """Delete the specified file.

        Parameters
        ----------
        path : str
            Full path to file to be deleted.

        """
        try:
            os.unlink(file_path)
        except Exception as e:
            raise type(e)(str(e))

    def take_screenshot(self, file_name=uuid.uuid1()):
        """Save image of entire screen.

        File name is constructed of test method name. File is saved to the
        same dir where log file is created.
        """
        try:
            image_path = os.path.join(os.getcwd(), f"{file_name}.png")
            ImageGrab.grab().save(image_path)
            self.logger.info(f"Screenshot image saved to file {image_path}.")
            return image_path

        except Exception as e:
            self.logger.warning(type(e)(str(e)))

    def kill_app(self, pid):
        """Terminate a running process, specified by the process id (pid).

        Parameters
        ----------
        pid : int
            The process id

        """
        try:
            p = psutil.Process(pid)
            p.kill()
        except Exception as e:
            self.logger.warning(type(e)(str(e)))

    def kill_processes_by_name_filter(self, name_filter):
        """Kill all processes (except for services).

        Parameters
        ----------
        name_filter : str
            A regex to filter process names by, for example: '^Alteryx' for
            all names starting with 'Alteryx'.

        Returns
        -------
        list
            List of processes matching the name filter, which were attempted
            to be killed.
        """
        processes = self.get_process_list(name_filter=name_filter)

        try:
            self.logger.debug(f"Attempting to kill process: {processes}")
            for process in processes:
                pid = process["pid"]
                self.kill_app(pid)

        except Exception as e:
            self.logger.warning(type(e)(str(e)))

        return processes

    def get_process_list(self, name_filter="", flags=re.IGNORECASE):
        """Get a list of processes that matches the criteria.

        Parameters
        ----------
        name_filter : str, optional
            Regex (either form, with or without forward slashes) on which to
            filter the list of processes.
        flags : int, optional
            Flags excepted by python re.search and re.match.

        """
        pattern = re.compile(self.trim_regex_chars(name_filter), flags)

        process_list = [
            p.info
            for p in psutil.process_iter(attrs=["pid", "name"])
            if pattern.match(p.info["name"]) is not None
        ]

        return process_list

    def load_json(self, path):
        """Load json file to a dict (in file io safe manner) and return it.

        Parameters
        ----------
        path : str
            Full path to the json file to load

        Returns
        -------
        dict
        Dictionary that represents the contents of the json file. Meaning of
        that dict depends on what json file is being loaded.

        Returns empty dict if it can't load for any reason (e.g. file isn't
        there, can't parse the json, etc.)

        """
        dict = {}
        try:
            with open(path) as source:
                dict = json.loads(source.read())
        except FileNotFoundError:
            pass

        return dict

    def get_pid(self, app=None, handle=None):
        """Get the process id (pid) for the specified element.

        Parameters
        ----------
        app: object, optional
            Pywinauto application object.
        handle: int, optional
            Window handle.

        Returns
        -------
        int
            Process ID for the application or process that conrols the
            specified window.

        """
        if app:
            handle = app.window().handle
        pid = handleprops.processid(handle)
        return pid

    def start_application(self, exe_path):
        """Start he application at the specified executable path.

        Parameters
        ----------
        exe_path: str
            Full path the executable (or executable that can be found in the
            windows path), possibly together with cmd line parameters

        Returns
        -------
        app : obj
            Pywinauto application object for the process that was started

        """
        timings.TimeConfig().Slow()
        app = Application(backend="uia").start(exe_path)
        timings.TimeConfig().Defaults()
        return app

    def trim_regex_chars(self, s):
        """Trim forward slashes surrounding regex, alternate re form."""
        return s.lstrip("/").rstrip("/")

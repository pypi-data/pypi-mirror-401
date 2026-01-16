######################################################################
#
# Image Velocimetry Python API
# Copyright (C) 2025 EDF
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details :
# <http://www.gnu.org/licenses/>.
#
######################################################################

import json
from enum import Enum
from os import path
import sys
from ctypes import cdll
from abc import ABC, abstractmethod

# Progress bar using optional package
try:
    from progress.bar import Bar
except ImportError:
    # Simple class Bar if package progress not available
    class Bar:
        def __init__(self, message, max: int = 0, suffix: str = ""):
            self.n_iter = max
            self.suffix = suffix
            print(message, end="")

        @staticmethod
        def next():
            print(".", end="")

        @staticmethod
        def finish():
            print("Ok")


# CLI function to load a global JSON parameter file
def read_parameter_file(parameter_file: str) -> dict:
    with open(parameter_file, "r") as json_file:
        param_dict = json.load(json_file)
    return param_dict


class MessageLevel(Enum):
    INFO = 0  # Information message
    WARNING = 1  # Warning message (current process still running)
    ERROR = 2  # Error message (current process stopped)


class ComInterface(ABC):

    @abstractmethod
    def display(self, message: str, level: MessageLevel = MessageLevel.INFO, end: str = "\n"):
        pass

    @abstractmethod
    def start_progress(self, message: str, n_iter: int):
        pass

    @abstractmethod
    def progress(self, iteration: int, total: int):
        pass

    @abstractmethod
    def end_progress(self):
        pass


class ComInterfaceCLI(ComInterface):
    """ Communication interface functions for Command Line Interface """

    def __init__(self):
        """ CLI Communication interface constructor """
        self.bar = None

    def display(self, message: str, level: MessageLevel = MessageLevel.INFO, end: str = "\n"):
        """ Display information to user

        :param message: Message to display
        :param level: Level of message (0: Info, 1: Warning, 2: Error)
        :param end: string to end
        """
        if level == MessageLevel.INFO:
            print(message, end=end)
        elif level == MessageLevel.WARNING:
            print("Warning: " + message, end=end)
        elif level == MessageLevel.ERROR:
            raise Exception(message)

    def start_progress(self, message: str, n_iter: int):
        """ Open a progress bar

        :param message: Process message
        :param n_iter: Number of process iterations
        """
        self.bar = Bar(message, max=n_iter, suffix="%(index)d/%(max)d | %(elapsed)ds / %(eta)ds")

    def progress(self, iteration: int, total: int):
        """ Set the progress bar

        :param iteration: Current iteration
        :param total: Number of iterations
        """
        self.bar.next()

    def end_progress(self):
        """ Close the progress bar"""
        self.bar.finish()


communication: ComInterfaceCLI = ComInterfaceCLI()


def load_lib(name: str):
    """ Load a dynamic library from a file with OS detection

    :param name: name of the library
    :return: dynamic library
    """
    if sys.platform[:3].lower() == "win":
        lib_name = name + "_win11.dll"
    else:
        lib_name = name + "_gfort13.3.so"
    print("library = ", lib_name)
    lib_path = path.join(path.dirname(path.dirname(__file__)), "lib_fortran", lib_name)
    if path.exists(lib_path):
        print("arrive ici")
        return cdll.LoadLibrary(str(lib_path))
    else:
        raise FileNotFoundError(lib_path)

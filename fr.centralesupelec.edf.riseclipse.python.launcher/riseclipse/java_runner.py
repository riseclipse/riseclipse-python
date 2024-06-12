# *************************************************************************
# **  Copyright (c) 2024 CentraleSupélec & EDF.
# **  All rights reserved. This program and the accompanying materials
# **  are made available under the terms of the Eclipse Public License v2.0
# **  which accompanies this distribution, and is available at
# **  https://www.eclipse.org/legal/epl-v20.html
# ** 
# **  This file is part of the RiseClipse tool
# **  
# **  Contributors:
# **      Computer Science Department, CentraleSupélec
# **      EDF R&D
# **  Contacts:
# **      dominique.marcadet@centralesupelec.fr
# **      aurelie.dehouck-neveu@edf.fr
# **  Web site:
# **      https://riseclipse.github.io
# *************************************************************************

from abc import ABC
from subprocess import run
from shutil import which

class JavaRunner(ABC):
    """
    Abstract class that carry out the execution of a .jar file.
    
    Attributes
    ----------
    java_command : str
        The path to the java command used to execute the jar file.
    jar_file : str
        The path to the jar file that will be executed.
    result_code : None or int
        The result code after execution of the jar file.
    """
        
    def __init__(self, jar_path: str):
        """
        Initialize the JavaRunner object.
        The java command that will be used is initialized with shutil.which().
        
        Parameters
        ----------
        jar_path : str
            The path to the jar file.
        """
        self.jar_file = jar_path
        self.java_command = which("java")
        self.result_code = None
    
    def set_jar_file(self, jar_path: str):
        """
        Change the jar file that will be executed.

        Parameters
        ----------
        jar_path : str
            The path to the jar file.

        Returns
        -------
        None
        """
        self.jar_file = jar_path
    
    def set_java_command(self, command: str):
        """
        TChange the java command that will be used to execute the jar file.

        Parameters
        ----------
        command : str
            The path to the java command.

        Returns
        -------
        None
        """
        self.java_command = command
    
    def get_result_code(self):
        """
        Returns the result code after execution of the jar file.
        Before execution, None is returned.
        
        Returns
        -------
        int or None
            The result code or None.
        """
        return self.result_code
    
    def run(self, arguments: list[str]) -> int:
        """
        Executes the jar file using the given arguments.
        
        Parameters
        ----------
        arguments : list[str]
            The arguments that are added to the command line.

        Returns
        -------
        str
            The text displayed on stdout while the jar executes.
        """
        command = [self.java_command, '-jar', self.jar_file] + [a for a in arguments]
        result = run(command, capture_output=True, text=True)
        self.result_code = result.returncode

        return result.stdout

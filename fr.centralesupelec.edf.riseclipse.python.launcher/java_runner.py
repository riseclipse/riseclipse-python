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
    
    def __init__(self, jar_path):
        self.jar_file = jar_path
        self.java_command = which("java")
        self.result_code = None
    
    def set_jar_file(self, jar_path):
        self.jar_file = jar_path
    
    def set_java_command(self, command):
        self.java_command = command
    
    def get_result_code(self):
        return self.result_code
    
    def run(self, arguments):
        command = [self.java_command, '-jar', self.jar_file] + [a for a in arguments]
        result = run(command, capture_output=True, text=True)
        self.result_code = result.returncode

        return result.stdout

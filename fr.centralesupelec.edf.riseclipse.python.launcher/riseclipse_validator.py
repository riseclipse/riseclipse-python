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

from java_runner import JavaRunner
from riseclipse_output import RiseClipseOutput


class RiseClipseValidator(JavaRunner) :

    DO_NOT_DISPLAY_COPYRIGHT_OPTION = "--do-not-display-copyright"

    def __init__(self, jarPath: str):
        super().__init__(jarPath)
        # 
        self.options = []
        # specific field for output level
        self.level = "--warning"
        # --format-string must not be used if the output is processed
        self.format_string = ""
        # --use-color only meaningful for validate_to_stdout
        self.use_color = False
        # path to files must be at the end
        self.files = []

    def get_output_level(self) -> str:
        return self.level
    
    def set_output_level(self, level: str) -> None:
        match level:
            case "debug" | "info" | "notice" | "warning" | "error":
                self.level = "--" + level
    
    def get_output_format(self) -> str:
        return self.format_string
        
    def set_output_format(self, format: str) -> None:
        # not checked
        self.format_string = format
    
    def get_use_color(self) -> bool:
        return self.use_color
    
    def set_use_color(self, use=True) -> None:
        self.use_color = use
    
    def get_display_copyright(self) -> bool:
        return self.DO_NOT_DISPLAY_COPYRIGHT_OPTION not in options

    def set_display_copyright(self, display=True) -> None:
        if display:
            options.remove(self.DO_NOT_DISPLAY_COPYRIGHT_OPTION)
        elif self.get_display_copyright():
            options.append(self.DO_NOT_DISPLAY_COPYRIGHT_OPTION)

    def add_file(self, file: str) -> None:
        self.files.append(file)
    
    def add_option(self, opt, value=None) -> None:
        if opt in self.options:
            if value != None:
                self.options[self.options.index(opt) + 1] = value
        else:
            self.options.append(opt)
            if value != None:
                self.options.append(value)

    def remove_option(self, opt, has_value=False) -> None:
        if opt in self.options:
            pos = self.options.index(opt)
            self.options.pop(pos)
            if has_value:
                self.options.pop(pos)
    
    def compute_arguments(self, display_copyright=True, use_format=True, set_color=False):
        arguments = [self.level]
        if not display_copyright:
            arguments.append(self.DO_NOT_DISPLAY_COPYRIGHT_OPTION)
        if use_format and self.format_string != "":
            arguments.append("--format-string")
            arguments.append(self.format_string)
        if set_color:
            if self.use_color:
                arguments.append("--use-color")            
        for option in self.options:
            arguments.append(option)
        for file in self.files:
            arguments.append(file)

        return arguments
    
    
         
    def validate(self):
        arguments = self.compute_arguments(display_copyright=False, use_format=False)
        return RiseClipseOutput(self.run(arguments).split('\n'))
    
    def validate_to_str(self):
        arguments = self.compute_arguments()
        return self.run(arguments)
    
    def validate_to_stdout(self):
        arguments = self.compute_arguments(set_color=True)
        print(self.run(arguments))

    def validate_to_txt(self, outputFile: str="riseclipse_output.txt") -> None:
        arguments = self.compute_arguments()
        result = self.run(arguments)
        output_file = open(outputFile, "w")
        output_file.write(result)
        output_file.close()

    def get_current_version(self):
        copyright = self.run(["--help"]).split('\n')[16]
        version_pos = copyright.find("version: ")
        version = copyright[version_pos + len("version: "):]
        version = version.split()[0]
        version = version.split('.')
        for i in range(len(version)):
            version[i] = int(version[i])
        return version


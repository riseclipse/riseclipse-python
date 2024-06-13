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
    """
    Base class for RiseClipse validators. It takes care of common options.
    
    Attributes:
        options (list[str]): The set of options that will be added when the validation is launched.
        level (str): The level of displayed messages, initialized to ``"warning"``.
        format_string (str): The format string used by the ``java.util.Formatter``.
        use_color (bool): Whether colors are used when result is displayed on stdout, initialized to ``False``.
        files (list[str]): The files that will be given to the validator.
    """

    def __init__(self, jarPath: str):
        """
        Initialize the RiseClipseValidator object.
        
        Args:
            jar_path: The path to the validator ``jar`` file
        """
        super().__init__(jarPath)
        # 
        self.options = []
        # specific field for output level
        self.level = "warning"
        # --format-string must not be used if the output is processed
        self.format_string = ""
        # --use-color only meaningful for validate_to_stdout
        self.use_color = False
        # path to files must be at the end
        self.files = []

    def get_output_level(self) -> str:
        """
        Returns:
            the current output level, one of ``"debug"``, ``"info"``, ``"notice"``, ``"warning"`` or ``"error"``.
        """
        return self.level
    
    def set_output_level(self, new_level: str) -> None:
        """
        Set the current output level.
        
        Args:
            new_level: The new output level.
                Must be ``"debug"``, ``"info"``, ``"notice"``, ``"warning"`` or ``"error"``.
        """
        match level:
            case "debug" | "info" | "notice" | "warning" | "error":
                self.level = new_level
    
    def get_output_format(self) -> str:
        """
        Returns the current format string used for output.
        
        Returns:
            The current format string.
        """
        return self.format_string
        
    def set_output_format(self, format: str) -> None:
        """
        Set the current format string used for output.
        
        Args:
            format: The new format string, its validity is not checked.
        """
        # not checked
        self.format_string = format
    
    def get_use_color(self) -> bool:
        """
        Returns whether color is used.
        
        Returns:
            True if color will be used, False Otherwise.
        """
        return self.use_color
    
    def set_use_color(self, use: bool=True) -> None:
        """
        Set whether color will be used for output.
        
        Args:
            use: If True, color will be used.
        """
        self.use_color = use
    
    DO_NOT_DISPLAY_COPYRIGHT_OPTION = "--do-not-display-copyright"

    def get_display_copyright(self) -> bool:
        """
        Returns whether the copyright is displayed.
        
        Returns:
            True if the copyright is displayed, False Otherwise.
        """
        return self.DO_NOT_DISPLAY_COPYRIGHT_OPTION not in self.options

    def set_display_copyright(self, display: bool=True) -> None:
        """
        Set whether the copyright is displayed.
        
        Args:
            display: If True, copyright will be displayed.
        """
        if display:
            self.options.remove(self.DO_NOT_DISPLAY_COPYRIGHT_OPTION)
        elif self.get_display_copyright():
            self.options.append(self.DO_NOT_DISPLAY_COPYRIGHT_OPTION)

    def add_file(self, file: str) -> None:
        """
        Add a file to be processed by the validator.
        
        Args:
            file: The path to the file or directory to be processed.
        """
        self.files.append(file)
    
    def _add_option(self, opt: str, value: str=None) -> None:
        """
        Add an option to the command line. An associated value may be specified.
        
        Note:
            This method is intended to be used by subclasses
                
        Args:
            opt: The option to be added.
            value: The value to be added after the option.
        """
        if opt in self.options:
            if value != None:
                self.options[self.options.index(opt) + 1] = value
        else:
            self.options.append(opt)
            if value != None:
                self.options.append(value)

    def _remove_option(self, opt:str, has_value=False) -> None:
        """
        Remove an option from the command line.
        
        Note:
            This method is intended to be used by subclasses
                
        Args:
            opt: The option to be removed.
            has_value: Whether there was also an associated value.
        """
        if opt in self.options:
            pos = self.options.index(opt)
            self.options.pop(pos)
            if has_value:
                self.options.pop(pos)
    
    def _compute_arguments(self, display_copyright: bool=True, use_format: bool=True, set_color: bool=False) -> list[str]:
        """
        Returns the arguments that will be passed to the run() method.
        
        Note:
            This method is intended to be internal
                
        Args:
            display_copyright: Whether the display_copyright setting must be taken into account. Default is True.
            use_format: Whether the format_string setting must be taken into account. Default is True.
            set_color: Whether the use_color setting must be taken into account. Default is False.

        Returns:
            The list of strings that will be passed to the run() method.
        """
        arguments = ['--' + self.level]
        if use_format and self.format_string != "":
            arguments.append("--format-string")
            arguments.append(self.format_string)
        if set_color:
            if self.use_color:
                arguments.append("--use-color")            
        if not display_copyright:
            self.set_display_copyright(False)
        for option in self.options:
            arguments.append(option)
        for file in self.files:
            arguments.append(file)

        return arguments
    
    
         
    def validate(self) -> RiseClipseOutput:
        """
        Runs the validator with the current set of arguments and files.
        
        Returns:
            An object representing the result of validation.
        """
        arguments = self._compute_arguments(display_copyright=False, use_format=False)
        return RiseClipseOutput(self.run(arguments).split('\n'))
    
    def validate_to_str(self) -> str:
        """
        Runs the validator with the current set of arguments and files.
        
        Returns:
            The result of validation as a string.
        """
        arguments = self._compute_arguments()
        return self.run(arguments)
    
    def validate_to_stdout(self) -> None:
        """
        Runs the validator with the current set of arguments and files.
        Display the result on stdout.
        """
        arguments = self._compute_arguments(set_color=True)
        print(self.run(arguments))

    def validate_to_txt(self, outputFile: str="riseclipse_output.txt") -> None:
        """
        Runs the validator with the current set of arguments and files.
        Save the result in the given file.
        
        Args:
            outputFile: The path to the file where the result will be saved.
        """
        arguments = self._compute_arguments()
        result = self.run(arguments)
        output_file = open(outputFile, "w")
        output_file.write(result)
        output_file.close()

    def get_current_version(self) -> list[int]:
        """
        Returns the current version of the ``jar`` file used by this object.
        
        Returns:
            A list of three integers giving the current version.
        """
        copyright = self.run(["--help"]).split('\n')[16]
        version_pos = copyright.find("version: ")
        version = copyright[version_pos + len("version: "):]
        version = version.split()[0]
        version = version.split('.')
        for i in range(len(version)):
            version[i] = int(version[i])
        return version


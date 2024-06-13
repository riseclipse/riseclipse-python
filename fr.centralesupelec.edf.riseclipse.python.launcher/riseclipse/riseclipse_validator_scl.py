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

from pathlib import Path
from sys import argv

from riseclipse_validator import RiseClipseValidator
from riseclipse_download import RiseClipseDownload


RISECLIPSE_VALIDATOR_SCL_JAR = "RiseClipseValidatorSCL.jar"


class RiseClipseValidatorSCL(RiseClipseValidator) :
    """
    This class is a launcher for the ``RiseClipseValidatorSCL.jar`` tool.
    
    It offers specific options for this validator.
        
    Note:
        The script ``riseclipse_validator_scl.py`` can also be executed directly, it allows to donwload or update the
        validator ``jar`` file needed for this API.
    """

    def __init__(self):
        """
        Initialize the RiseClipseValidatorSCL object.

        In the initial state, one can considered that the following methods have been called:
            * :py:meth:`set_output_level("warning") <riseclipse_validator.RiseClipseValidator.set_output_level>`
            * :py:meth:`set_output_format('%6$s%1$-7s%7$s: [%2$s] %4$s (%5$s:%3$d)') <riseclipse_validator.RiseClipseValidator.set_output_format>`
            * :py:meth:`set_use_color(False) <riseclipse_validator.RiseClipseValidator.set_use_color>`
            * :py:meth:`set_display_copyright(True) <riseclipse_validator.RiseClipseValidator.set_display_copyright>`
            * :py:meth:`set_make_explicit_links`
            * :py:meth:`unset_xml_schema`
            * :py:meth:`unset_display_nsd_messages`
            * :py:meth:`unset_use_different_exit_codes`
            * :py:meth:`unset_use_filenames_starting_with_dot`
        
        """
        super().__init__(RISECLIPSE_VALIDATOR_SCL_JAR)
        # by default, explicit links are created
        self._add_option("--make-explicit-links")

    def set_make_explicit_links(self):
        """
        Build explicit links before doing validation.
        """
        self._add_option("--make-explicit-links")

    def unset_make_explicit_links(self):
        """
        Don't build explicit links before doing validation.
        """
        self.__remove_option("--make-explicit-links")

    def set_xml_schema(self, schema_path: str):
        """
        Do an XMLSchema validation.
        
        Args:
            schema_path: The path to the XML Schema file
        """
        self._add_option("--xml-schema", schema_path)

    def unset_xml_schema(self):
        """
        Don't do an XMLSchema validation.
        """
        self._remove_option("--xml-schema", True)

    def set_display_nsd_messages(self):
        """
        Display messages concerning the loading of NSD files.
        """
        self._add_option("--display-nsd-messages")

    def unset_display_nsd_messages(self):
        """
        Don't display messages concerning the loading of NSD files.
        """
        self._remove_option("--display-nsd-messages")

    def set_use_different_exit_codes(self):
        """
        Returns different exit codes according to the higher severity in messages.
        """
        self._add_option("--use-different-exit-codes")

    def unset_use_different_exit_codes(self):
        """
        Don't returns different exit codes according to the higher severity in messages.
        """
        self._remove_option("--use-different-exit-codes")

    def set_use_filenames_starting_with_dot(self):
        """
        Take into account files starting with a dot.
        """
        self._add_option("--use-filenames-starting-with-dot")

    def unset_use_filenames_starting_with_dot(self):
        """
        Don't take into account files starting with a dot.
        """
        self._remove_option("--use-filenames-starting-with-dot")



if __name__ == '__main__':
    if len(argv) == 1:
        jar = Path(RISECLIPSE_VALIDATOR_SCL_JAR)
        
        if not jar.exists():
            print("It seems that the validator is missing.")
            print("You can download one using '--download latest' command line option (or use a specific version instead of latest).")
            exit(0)
        
        validator = RiseClipseValidatorSCL()
        current_version = validator.get_current_version()
        download = RiseClipseDownload()
        print("Your version is: %d.%d.%d" % (current_version[0], current_version[1], current_version[2]))
        latest_version = download.get_latest_version("riseclipse-validator-scl2003")
        if current_version < latest_version:
            print("A new version is available: %d.%d.%d" % (latest_version[0], latest_version[1], latest_version[2]))
            print("You can download it using '--download latest' command line option")
        if current_version == latest_version:
            print("Your version is the latest one")

    if len(argv) == 3:
        if argv[1] == "--download":
            download = RiseClipseDownload()
            if argv[2] == "latest":
                version = download.get_latest_version("riseclipse-validator-scl2003")
                if version == None:
                    exit()
                version_str = "%d.%d.%d" % (version[0], version[1], version[2])
                print("Latest version is ", version_str)
            else:
                version = argv[2].split('.')
                for i in range(len(version)):
                    version[i] = int(version[i])
        
            download.download_version("riseclipse-validator-scl2003", "RiseClipseValidatorSCL", version, RISECLIPSE_VALIDATOR_SCL_JAR)





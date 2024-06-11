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

    def __init__(self):
        super().__init__(RISECLIPSE_VALIDATOR_SCL_JAR)
        # by default, explicit links are created
        self.add_option("--make-explicit-links")

    def set_make_explicit_links(self):
        self.add_option("--make-explicit-links")

    def unset_make_explicit_links(self):
        self.remove_option("--make-explicit-links")

    def set_xml_schema(self, schema_path):
        self.add_option("--xml-schema", schema_path)

    def unset_xml_schema(self):
        self.remove_option("--xml-schema", True)

    def set_display_nsd_messages(self):
        self.add_option("--display-nsd-messages")

    def unset_display_nsd_messages(self):
        self.remove_option("--display-nsd-messages")

    def set_use_different_exit_codes(self):
        self.add_option("--use-different-exit-codes")

    def unset_use_different_exit_codes(self):
        self.remove_option("--use-different-exit-codes")

    def set_use_filenames_starting_with_dot(self):
        self.add_option("--use-filenames-starting-with-dot")

    def unset_use_filenames_starting_with_dot(self):
        self.remove_option("--use-filenames-starting-with-dot")



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





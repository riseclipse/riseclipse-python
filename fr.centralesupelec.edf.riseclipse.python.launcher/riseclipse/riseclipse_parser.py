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

import copy

class RiseClipseParser:
    """
    A class used to parse messages from RiseClipseValidator.
    This class is used to convert raw messages into a structured format that can be easily 
    processed or displayed.
    """
    def __init__(self, list_of_messages: list[str]):
        """
        Constructs all the necessary attributes for the RiseClipseParser object.
        
        Args:
            list_of_messages: The list of messages to be parsed
        """
        self.list_of_messages = list_of_messages
        self.parsed_messages = []
        if self.list_of_messages != None and len(self.list_of_messages) > 0:
            self.parse_messages()
        else:
            print("No messages to parse.")
    
    def get_parsed_messages(self) -> list[str]:
        """
        Returns the list of parsed messages.
        """
        return self.parsed_messages
        
    def parse_messages(self):
        """
        Iterates over each message in the list and parses it using the parse_message method.
        Appends the parsed message to the parsed_messages attribute.
        """
        for message in self.list_of_messages:
            if len(message) > 0:
                self.parsed_messages.append(self.parse_message(message))
    
    def parse_message(self, message: str) -> dict:
        """
        Parses a single message into a dictionary with keys for ``message``, ``category``, ``line``, ``data``, ``filename``, and ``severity``.
        Each key's value is extracted from the message by splitting the message string on commas and selecting the appropriate element.
        
        Args:
            message: A single message to be parsed i.e. a line from the standard output of the validator
        
        Returns:
            A dictionary containing the parsed message.
            Keys of the dictionary are ``message``, ``category``, ``line``, ``data``, ``filename``, and ``severity``:
            
            * the field ``message`` contains the original non-parsed message
            * the field ``category`` contains the category of the message
            * the field ``line`` contains the line number in the file targetted by the message
            * the field ``data`` contains the part of the message that contains the actual error/warning/notice/info
            * the field ``filename`` contains the name of the file targetted by the message
            * the field ``severity`` contains the severity of the message (ERROR, WARNING, NOTICE, INFO, DEBUG)
        
        """
        import re
        #print("Parsing message: " + message)
        parsed_message = {}
        parsed_message["message"] = message

        regex_end = r'\((\w|\W)*\)'
        regex_middle = r'\[(\w|\W)*\]'
        match = re.search(regex_end, message)
        filename = match[0].strip()[1:-1].split(":")[0]
        line = match[0].strip()[1:-1].split(":")[1]
        message = re.sub(regex_end, '', message)
        match = re.search(regex_middle, message)
        category = match[0].strip()[1:-1]
        message = re.sub(regex_middle, '', message)
        severity = message[:8].strip()
        message = copy.copy(message[9:].strip())
        data = message.strip()

        parsed_message["category"] = category
        parsed_message["line"] = line
        parsed_message["data"] = data
        parsed_message["filename"] = filename
        parsed_message["severity"] = severity
        return parsed_message

    

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

from riseclipse_parser import RiseClipseParser
import json

class RiseClipseOutput:
    """
    A class used to parse and categorize messages from the Validator in order to use them in Python scripts.

    ...

    Methods
    -------
    get_errors():
        Returns a list of parsed error messages.
    get_warnings():
        Returns a list of parsed warning and error messages.
    get_notices():
        Returns a list of parsed notice, warning and error messages.
    get_infos():
        Returns a list of parsed info, notice, warning and error messages.
    get_only_warnings():
        Returns a list of only parsed warning messages.
    get_only_notices():
        Returns a list of only parsed notice messages.
    get_only_infos():
        Returns a list of only parsed info messages.
    get_all_messages():
        Returns a list of all parsed messages.
    get_messages_by_category(category):
        Returns a list of messages, filtered by category.
    def get_messages_by_specific_message(data):
        Returns a list of messages, filtered by a specific part of message, named data.
    get_messages_by_filename(filename):
        Returns a list of messages, filtered by the file containing the error/warning/info.
    def get_messages_with_filter(self, filtering_dict):
        Returns a list of messages, filtered with a dictionnary containing informations on which we want to filter messages in the file containing the error/warning/notice/info.
    to_csv(path):
        Writes the parsed messages to a CSV file and returns the CSV as a string.
    to_json(path):
        Writes the parsed messages to a JSON file and returns the JSON as a dictionary.
    to_dataframe():
        Returns a pandas DataFrame of the parsed messages.
    
    See Also
    --------
    PyClipseParser : A class used to parse messages from the Validator in order to use them in Python scripts.
    """

    def __init__(self, list_of_messages):
        """
        Constructs all the necessary attributes for the PyClipseOutput object.

        Parameters
        ----------
            list_of_messages : list
                a list of messages to be parsed and categorized
        """
        self.errors = []
        self.warnings = []
        self.notices = []
        self.infos = []
        self.only_warnings = []
        self.only_notices = []
        self.only_infos = []
        self.parsed_messages = RiseClipseParser(list_of_messages).parsed_messages

    def get_errors(self):
        """
        Returns a list of parsed error messages (dictionaries), to see the exact format, see PyClipseParser.

        If the list of errors is not empty, it returns the list. Otherwise, it parses the messages and appends any error messages to the list.

        Returns
        -------
        list
            a list of parsed error messages
        
        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.errors) > 0:
            return self.errors
        for message in self.parsed_messages:
            if message["severity"] == "ERROR":
                self.errors.append(message)
        return self.errors

    def get_warnings(self):
        """
        Returns a list of parsed warning and error messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of warnings and errors is not empty, it returns the list. Otherwise, it parses the messages and appends any warning or error messages to the list.

        Returns
        -------
        list
            a list of parsed warning and error messages
        
        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.warnings) > 0:
            return self.warnings
        for message in self.parsed_messages:
            if message["severity"] in ["WARNING","ERROR"]:
                self.warnings.append(message)
        return self.warnings
    
    def get_notices(self):
        """
        Returns a list of parsed notice, warning and error messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of notices, warnings and errors is not empty, it returns the list. Otherwise, it parses the messages and appends any notice, warning and error messages to the list.

        Returns
        -------
        list
            a list of parsed notice, warning and error messages

        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.notices) > 0:
            return self.notices
        for message in self.parsed_messages:
            if message["severity"] in ["WARNING","ERROR","NOTICE"]:
                self.notices.append(message)
        return self.notices

    def get_infos(self):
        """
        Returns a list of parsed info, notices, warnings and errors messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of infos, notices, warnings and errors is not empty, it returns the list. Otherwise, it parses the messages and appends any info, notice, warning and error messages to the list.

        Returns
        -------
        list
            a list of parsed info, notice, warning and error messages

        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.infos) > 0:
            return self.infos
        for message in self.parsed_messages:
            if message["severity"] in ["WARNING","ERROR","INFO","NOTICE"]:
                self.infos.append(message)
        return self.infos

    def get_only_warnings(self):
        """
        Returns a list of parsed warning messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of warnings is not empty, it returns the list. Otherwise, it parses the messages and appends any warning messages to the list.

        Returns
        -------
        list
            a list of parsed warning messages
        
        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.only_warnings) > 0:
            return self.only_warnings
        for message in self.parsed_messages:
            if message["severity"] == "WARNING":
                self.only_warnings.append(message)
        return self.only_warnings
    
    def get_only_notices(self):
        """
        Returns a list of parsed notice messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of notices is not empty, it returns the list. Otherwise, it parses the messages and appends any notice messages to the list.

        Returns
        -------
        list
            a list of parsed notice messages

        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.notices) > 0:
            return self.only_notices
        for message in self.parsed_messages:
            if message["severity"] == "NOTICE":
                self.only_notices.append(message)
        return self.only_notices

    def get_only_infos(self):
        """
        Returns a list of parsed info messages (dictionaries), to see the exact format, see PyClipseParser

        If the list of infos is not empty, it returns the list. Otherwise, it parses the messages and appends any info messages to the list.

        Returns
        -------
        list
            a list of parsed info messages

        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        if len(self.only_infos) > 0:
            return self.only_infos
        for message in self.parsed_messages:
            if message["severity"] == "INFO":
                self.only_infos.append(message)
        return self.only_infos
    
    def get_all_messages(self):
        """
        Returns a list of all parsed messages (dictionaries), to see the exact format, see PyClipseParser.

        Returns
        -------
        list
            a list of all parsed messages
        
        See Also
        --------
        PyClipseParser.parse_message : Parses a single message into a dictionary with keys for 'message', 'category', 'line', 'data', 'filename', and 'severity'.
        """
        return self.parsed_messages
    
    def get_messages_by_category(self, category):
        """
        Returns a list of messages, filtered by category.
        The category does not have to be an exact match, it can be a substring of the category.
        
        Parameters
        ----------
        category : str
            the category to filter the messages by
        
        Returns
        -------
        list
            a list of parsed messages filtered by category
        """
        messages = []
        for message in self.parsed_messages:
            if category in message["category"]:
                messages.append(message)
        return messages
    
    def get_messages_by_specific_message(self, data):
        """
        Returns a list of messages, filtered by a specific part of message, named data.
        The data does not have to be an exact match, it can be a substring of the message.
        
        Parameters
        ----------
        data : str
            the "data" e.g. specific message to filter the messages by
        
        Returns
        -------
        list
            a list of parsed messages filtered by specific message
        """
        messages = []
        for message in self.parsed_messages:
            if data in message["data"]:
                messages.append(message)
        return messages
    
    def get_messages_by_filename(self, filename):
        """
        Returns a list of messages, filtered by the file containing the error/warning/notice/info.
        
        Parameters
        ----------
        filename : str
            the filename to filter the messages by
        
        Returns
        -------
        list
            a list of parsed messages filtered by filename
        """
        messages = []
        for message in self.parsed_messages:
            if message["filename"] == filename:
                messages.append(message)
        return messages
    
    def get_messages_by_line(self, line):
        """
        Returns a list of messages, filtered by the line number in the file containing the error/warning/notice/info.
        
        Parameters
        ----------
        line : int
            the line number to filter the messages by
        
        Returns
        ----------
        list
            a list of parsed messages filtered by line number
        """
        messages = []
        for message in self.parsed_messages:
            if message["line"] == line:
                messages.append(message)
        return messages
    
    def get_messages_with_filter(self, filtering_dict):
        """
        Returns a list of messages, filtered with a dictionnary containing informations on which we want to filter messages in the file containing the error/warning/notice/info.
        
        Parameters
        ----------
        filtering_dict : dict
            the filter itself, fields of the dictionary are the the same as a parsed message
        
        Returns
        ----------
        list
            a list of parsed messages filtered according to the filter
        """
        messages = []
        for message in self.parsed_messages:
            b = True
            for filt in filtering_dict:
                if filt == "category" or filt == "data":
                    b = b and (filtering_dict[filt] in message[filt])
                else:
                    b = b and (filtering_dict[filt] == message[filt])


            
            if b :
                messages.append(message)
        return messages
    
    def to_csv(self, path, separator=","):
        """
        Writes the parsed messages to a CSV file and returns the CSV as a string.
        
        Parameters
        ----------
        path : str
            the path to write the CSV file to
        separator : str
            the separator to use in the csv file
        
        Returns
        -------
        str
            a string of the CSV file
        """
        if len(self.parsed_messages) == 0:
            print("No messages to write to CSV.")
            return ""
        
        csv = ""
        message = self.parsed_messages[0]
        for key in message:
            if key != "message":
                csv += key + separator
        csv += "message\n"
        for message in self.parsed_messages:
            for key in message:
                if key != "message":
                    csv += message[key] + separator
            csv += message["message"] + "\n"
        with open(path, "w") as f:
            f.write(csv)
        return csv
    
    def to_json(self,path):
        """
        Writes the parsed messages to a JSON file and returns the JSON as a dictionary.
        
        Parameters
        ----------
        path : str
            the path to write the JSON file to
        
        Returns
        -------
        dict
            a dictionary of the JSON file
        """
        json_dump = {}
        for i in range(len(self.parsed_messages)):
            json_dump[i] = self.parsed_messages[i]
        with open(path, "w") as f:
            json.dump(json_dump, f)
        return json_dump
    
    def to_dataframe(self):
        """
        Returns a pandas DataFrame of the parsed messages.
        
        Returns
        -------
        DataFrame
            a pandas DataFrame of the parsed messages
        """
        import pandas as pd
        dict_columns = {'message':[],'category':[],'line':[],'data':[],'filename':[],'severity':[]}
        for message in self.parsed_messages:
            dict_columns['message'].append(message['message'])
            dict_columns['category'].append(message['category'])
            dict_columns['line'].append(message['line'])
            dict_columns['data'].append(message['data'])
            dict_columns['filename'].append(message['filename'])
            dict_columns['severity'].append(message['severity'])
        return pd.DataFrame.from_dict(dict_columns)
    
    
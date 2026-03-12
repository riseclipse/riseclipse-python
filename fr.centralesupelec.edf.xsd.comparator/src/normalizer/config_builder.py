# *************************************************************************
# **  Copyright (c) 2024-2026 CentraleSupélec & EDF.
# **  All rights reserved. This program and the accompanying materials
# **  are made available under the terms of the Eclipse Public License v2.0
# **  which accompanies this distribution, and is available at
# **  https://www.eclipse.org/legal/epl-v20.html
# ** 
# **  This file is part of the RiseClipse tool
# **  
# **  Authors:
# **      Etienne Parent
# **      Jérémy Wang
# **  Contributors:
# **      Computer Science Department, CentraleSupélec
# **      EDF R&D
# **  Contacts:
# **      dominique.marcadet@centralesupelec.fr
# **      aurelie.dehouck-neveu@edf.fr
# **  Web site:
# **      https://riseclipse.github.io
# *************************************************************************

import configparser

DEFAULT_CONFIG = {
    'schema': {
        'id': True,
        'attributeFormDefault': False,
        'elementFormDefault': False,
        'blockDefault': False,
        'finalDefault': False,
        'targetNamespace': True,
        'version': True,
        'xmlns': True,
    },
    'element': {
        'abstract': True,
        'block': True,
        'default': True,
        'final': True,
        'fixed': True,
        'form': True,
        'id': True,
        'minOccurs': True,
        'maxOccurs': True,
        'name': True,
        'nillable': True,
        'type': True,
        'index_in_sequence': True,
    },
    'any element': {
        'id': True,
        'minOccurs': True,
        'maxOccurs': True,
        'namespace': True,
        'process_contents': True,
        'index_in_sequence': True,
    },
    'attribute': {
        'default': True,
        'fixed': True,
        'form': True,
        'id': True,
        'name': True,
        'type': True,
        'use': True,
    },
    'any attribute': {
        'id': True,
        'namespace': True,
        'process_contents': True,
    }
}


def get_default_config() -> dict:
    """
    Returns default config, with True on all possible attributes.
    """
    return DEFAULT_CONFIG


def createconfig(config_obj: configparser.ConfigParser) -> dict:
    """
    Returns a dict representing the configuration for the analysis to run.
    """
    res = get_default_config()

    for section in res:
        for option in res[section]:
            try:
                res[section][option] = config_obj.getboolean(section, option)
            except configparser.NoOptionError as e:
                continue

    return res

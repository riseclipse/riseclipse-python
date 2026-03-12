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

import argparse
import configparser

import xmlschema

from normalizer.config_builder import createconfig, get_default_config
from normalizer.xsd2tree import build_xsd_graph
from xsd_graphs.graph_manipulations import ask_and_delete_root_elements
from xsd_graphs.tree_isomorphism import xsd_rooted_tree_isomorphism


def compare_xsds(src_xsd_path1, src_xsd_path2, compare_all_root_elements, root_element, verbose_level, config):
    schema1 = xmlschema.XMLSchema(src_xsd_path1)
    schema2 = xmlschema.XMLSchema(src_xsd_path2)

    full_graph1, first_node1, _label_dict1 = build_xsd_graph(schema1, config)
    full_graph2, first_node2, _label_dict2 = build_xsd_graph(schema2, config)

    if not compare_all_root_elements:
        ask_and_delete_root_elements(
            full_graph1, first_node1,
            full_graph2, first_node2,
            root_element
        )

    isomorphism = xsd_rooted_tree_isomorphism(
        full_graph1, first_node1, full_graph2, first_node2, verbose_level)

    if isomorphism == []:
        print("XSD are not equivalent")
        return False
    else:
        print("XSD are equivalent")
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("XSD_1", help="File path for XSD 1.", type=str)
    parser.add_argument("XSD_2", help="File path for XSD 2.", type=str)

    parser.add_argument(
        "-a", "--all-root-elements",
        help="Compare XSD taking all root elements in account.",
        action="store_true",
    )

    parser.add_argument(
        "-r", "--root-element",
        help="Compare XSD taking only this root element in account.",
        type=str,
    )

    parser.add_argument(
        "-v", "--verbose-level",
        help="Select how verbose the results are, from 0 to 2. Default is 1",
        type=int,
    )

    parser.add_argument(
        "-c", "--config",
        help="Path to configuration file.",
    )

    args = parser.parse_args()

    if args.config:
        config_obj = configparser.ConfigParser()
        config_obj.read(args.config)
        config = createconfig(config_obj)
    else:
        config = get_default_config()
    if args.verbose_level == None:
        args.verbose_level = 1

    compare_xsds(
        src_xsd_path1=args.XSD_1,
        src_xsd_path2=args.XSD_2,
        compare_all_root_elements=args.all_root_elements,
        root_element=args.root_element,
        verbose_level=args.verbose_level,
        config=config
    )

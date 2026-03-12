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

import unittest

from main import compare_xsds
from normalizer.config_builder import get_default_config


class TestExamplesXsd(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = get_default_config()

    @classmethod
    def compare_xsds_test(cls, name_test):
        src_xsd_path1 = f'./xsd/exemples/test_{name_test}1.xsd'
        src_xsd_path2 = f'./xsd/exemples/test_{name_test}2.xsd'
        return compare_xsds(src_xsd_path1, src_xsd_path2, False, None, 0, cls.config)

    def test_all_order(self):
        self.assertEqual(self.compare_xsds_test('all_order'), True)

    def test_attribute_type_name(self):
        self.assertEqual(self.compare_xsds_test('attribute_type_name'), True)

    def test_attribute_type_restriction(self):
        self.assertEqual(self.compare_xsds_test(
            'attribute_type_restriction'), False)

    def test_attributeGroup(self):
        self.assertEqual(self.compare_xsds_test('attributeGroup'), True)

    def test_choice_or_all(self):
        self.assertEqual(self.compare_xsds_test('choice_or_all'), False)

    def test_default_attribute(self):
        self.assertEqual(self.compare_xsds_test('default_attribute'), True)

    def test_empty_or_none_attribute(self):
        self.assertEqual(self.compare_xsds_test(
            'empty_or_none_attribute'), False)

    def test_empty_or_none_element(self):
        self.assertEqual(self.compare_xsds_test(
            'empty_or_none_element'), False)

    def test_extension_attributes(self):
        self.assertEqual(self.compare_xsds_test('extension_attributes'), True)

    def test_extension_sequence(self):
        self.assertEqual(self.compare_xsds_test('extension_sequence'), True)

    def test_nillable(self):
        self.assertEqual(self.compare_xsds_test('nillable'), False)

    def test_sequence(self):
        self.assertEqual(self.compare_xsds_test('sequence'), False)

    def test_basic_type(self):
        self.assertEqual(self.compare_xsds_test('basic_type'), False)

    def test_simpleType_restriction(self):
        self.assertEqual(self.compare_xsds_test(
            'simpleType_restriction'), False)

    def test_simpleType_list(self):
        self.assertEqual(self.compare_xsds_test(
            'simpleType_list'), False)

    def test_simpleType_union(self):
        self.assertEqual(self.compare_xsds_test(
            'simpleType_union'), False)

    def test_simpleContent_attribute(self):
        self.assertEqual(self.compare_xsds_test(
            'simpleContent_attribute'), False)

    def test_simpleContent_complexType(self):
        self.assertEqual(self.compare_xsds_test(
            'simpleContent_complexType'), False)

    def test_mixed(self):
        self.assertEqual(self.compare_xsds_test(
            'mixed'), False)

    def test_complexContent_extension(self):
        self.assertEqual(self.compare_xsds_test(
            'complexContent_extension'), False)

    def test_complexContent_restriction(self):
        self.assertEqual(self.compare_xsds_test(
            'complexContent_restriction'), False)


if __name__ == '__main__':
    unittest.main()

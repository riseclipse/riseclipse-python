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

from xmlschema import XsdElement


class AtomicNode:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class SimpleTypeTree:
    def __init__(self, simple_type):
        assert simple_type.is_simple()

        self.name = simple_type.name

        if simple_type.is_restriction():
            self.inner = RestrictionNode(
                simple_type.base_type, simple_type.facets)
        elif simple_type.is_union():
            self.inner = UnionNode(simple_type.member_types)
        elif simple_type.is_atomic():
            self.inner = AtomicNode(simple_type.name)
        elif simple_type.is_list():
            self.inner = ListNode(simple_type.item_type)
        else:
            self.inner = simple_type.name

    def __str__(self):
        return f"{str(self.inner)}"

    def __hash__(self):
        return hash(self.__str__())


class UnionNode:
    def __init__(self, union_list):
        # Sort member types by alphabetical order to make them appear in a stable order
        self.union_list = sorted(
            [get_simple_type_tree(t) for t in union_list],
            key=str
        )

    def __str__(self):
        if len(self.union_list) == 1:
            # If there is only one member in the union, put it directly
            return str(self.union_list[0])
        else:
            return f"union of types (" + ", ".join([str(t) for t in self.union_list]) + ")"


class ListNode:
    def __init__(self, baseType):
        self.typ = get_simple_type_tree(baseType)

    def __str__(self):
        return f"list of type({(self.typ)})"


class RestrictionNode:
    def __init__(self, baseType, facets):
        self.base_type = get_simple_type_tree(baseType)
        self.facets = facets

    def __str__(self):
        if len(self.facets) == 0:
            # If there are no restriction facets, put baseType directly
            return str(self.base_type)
        else:
            # Sort facets to make them appear in a stable order
            sorted_dict = '{' + ' '.join([str(k) + ': ' + str(v)
                                          for k, v in sorted(self.facets.items())]) + '}'
            return f"restriction on {str(self.base_type)} (" + sorted_dict + ")"


def get_simple_type_tree(simple_type):
    if simple_type.is_simple():
        return SimpleTypeTree(simple_type)
    elif simple_type.has_simple_content():
        return SimpleTypeTree(simple_type.content)
    else:
        raise NotImplementedError(
            f"met unsupported simple type : {simple_type}")

    return SimpleTypeTree(simple_type)

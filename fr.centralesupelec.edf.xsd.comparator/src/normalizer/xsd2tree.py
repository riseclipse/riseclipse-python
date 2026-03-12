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

import re
import sys
from typing import List, Tuple, Union

import networkx as nx
import xmlschema

from normalizer.simple_types import get_simple_type_tree


def get_differences(obj1, obj2):
    """
    `get_differences(obj1, obj2)` returns a list of two dictionnaries containing the pairs
    of keys that have different values in `obj1` and `obj2`.
    """

    return [
        {
            attr[1:]: obj1.__dict__[attr] for attr in obj1.__dict__ if obj1.__dict__[attr] != obj2.__dict__[attr]
        },
        {
            attr[1:]: obj2.__dict__[attr] for attr in obj1.__dict__ if obj1.__dict__[attr] != obj2.__dict__[attr]
        }
    ]


class GraphNodeSchema:
    _component_name = 'schema'

    def __init__(self,
                 config: dict,
                 xmlns: str,
                 id='',
                 attributeFormDefault='unqualified',  # qualified|unqualified
                 elementFormDefault='unqualified',  # qualified|unqualified
                 # (#all|list of (extension|restriction|substitution))
                 blockDefault='',
                 # (#all|list of (extension|restriction|list|union))
                 finalDefault='',
                 targetNamespace='',
                 version='',
                 ):
        self._id = id if config['schema']['id'] else None
        self._attributeFormDefault = attributeFormDefault if config[
            'schema']['attributeFormDefault'] else None
        self._elementFormDefault = elementFormDefault if config[
            'schema']['elementFormDefault'] else None
        self._blockDefault = blockDefault if config['schema']['blockDefault'] else None
        self._finalDefault = finalDefault if config['schema']['finalDefault'] else None
        self._targetNamespace = targetNamespace if config['schema']['targetNamespace'] else None
        self._version = version if config['schema']['version'] else None
        self._xmlns = xmlns if config['schema']['xmlns'] else None

    def __str__(self):
        attr_list = [
            f" id=\"{self._id}\"" if self._id != None else "",
            f" attributeFormDefault=\"{self._attributeFormDefault}\"" if self._attributeFormDefault != None else "",
            f" elementFormDefault=\"{self._elementFormDefault}\"" if self._elementFormDefault != None else "",
            f" blockDefault=\"{self._blockDefault}\"" if self._blockDefault != None else "",
            f" finalDefault=\"{self._finalDefault}\"" if self._finalDefault != None else "",
            f" targetNamespace=\"{self._targetNamespace}\"" if self._targetNamespace != None else "",
            f" version=\"{self._version}\"" if self._version != None else "",
            f" xmlns=\"{' '.join([str(k) + '=' + str(v) for k, v in sorted(self._xmlns.items())])}\"" if self._xmlns != None else "",
        ]

        return "<schema" + "".join(attr_list) + ">"

    def compare(self, node_element) -> list:
        if type(node_element) != GraphNodeSchema:
            return None
        return get_differences(self, node_element)


class GraphNodeElement:
    _component_name = 'element'

    def __init__(self,
                 config: dict,
                 abstract=False,
                 # (#all | List of (extension | restriction | substitution))
                 block='',
                 default='',  # Inutile?
                 final='',  # (#all | List of (extension | restriction))
                 fixed='',
                 form='',
                 id='',
                 minOccurs=1,
                 maxOccurs=1,
                 name='',
                 nillable=False,
                 typ='',
                 # ref ='',
                 # substitutionGroup = ''
                 ):

        self._abstract = abstract if config['element']['abstract'] else None
        self._block = block if config['element']['block'] else None
        self._default = default if config['element']['default'] else None
        self._final = final if config['element']['final'] else None
        self._fixed = fixed if config['element']['fixed'] else None
        self._form = form if config['element']['form'] else None
        self._id = id if config['element']['id'] else None
        self._minOccurs = minOccurs if config['element']['minOccurs'] else None
        self._maxOccurs = maxOccurs if config['element']['maxOccurs'] else None
        self._name = name if config['element']['name'] else None
        self._nillable = nillable if config['element']['nillable'] else None
        self._type = typ if config['element']['type'] else None
        self._index_in_sequence = None
        self._parent_type = None

    def __str__(self):
        attr_list = [
            f" name=\"{self._name}\"" if self._name != None else "",
            f" type=\"{self._type}\"" if self._type != None else "",
            f" abstract=\"{self._abstract}\"" if self._abstract != None else "",
            f" block=\"{self._block}\"" if self._block != None else "",
            f" default=\"{self._default}\"" if self._default != None else "",
            f" final=\"{self._final}\"" if self._final != None else "",
            f" fixed=\"{self._fixed}\"" if self._fixed != None else "",
            f" form=\"{self._form}\"" if self._form != None else "",
            f" id=\"{self._id}\"" if self._id != None else "",
            f" minOccurs=\"{self._minOccurs}\"" if self._minOccurs != None else "",
            f" maxOccurs=\"{self._maxOccurs}\"" if self._maxOccurs != None else "",
            f" nillable=\"{self._nillable}\"" if self._nillable != None else "",
            f" index_in_sequence=\"{self._index_in_sequence}\"" if self._index_in_sequence != None else "",
            f" parent_type=\"{self._parent_type}\"" if self._parent_type != None else "",
        ]

        return "<element" + "".join(attr_list) + ">"

    def get_name_without_any_ns(self) -> str:
        return removeAnyNamespace(self._name)

    def compare(self, node_element) -> list:
        if type(node_element) != GraphNodeElement:
            return None
        if self._name != node_element._name:
            return None
        return get_differences(self, node_element)


class GraphNodeAnyElement:
    _component_name = 'any'

    def __init__(self,
                 config: dict,
                 id='',
                 minOccurs=1,
                 maxOccurs=1,
                 namespace: Union[Tuple[str], List[str]] = ('##any',),
                 process_contents='strict',  # lax|skip|strict
                 ):

        self._id = id if config['any element']['id'] else None
        self._minOccurs = minOccurs if config['any element']['minOccurs'] else None
        self._maxOccurs = maxOccurs if config['any element']['maxOccurs'] else None
        self._namespace = namespace if config['any element']['namespace'] else None
        self._process_contents = process_contents if config[
            'any element']['process_contents'] else None
        self._index_in_sequence = None
        self._parent_type = None

    def __str__(self):
        attr_list = [
            f" id=\"{self._id}\"" if self._id != None else "",
            f" minOccurs=\"{self._minOccurs}\"" if self._minOccurs != None else "",
            f" maxOccurs=\"{self._maxOccurs}\"" if self._maxOccurs != None else "",
            f" namespace=\"{self._namespace}\"" if self._namespace != None else "",
            f" process_contents=\"{self._process_contents}\"" if self._process_contents != None else "",
            f" index_in_sequence=\"{self._index_in_sequence}\"" if self._index_in_sequence != None else "",
            f" parent_type=\"{self._parent_type}\"" if self._parent_type != None else "",
        ]

        return "<any" + "".join(attr_list) + ">"

    def get_name_without_any_ns(self) -> str:
        return "any"

    def compare(self, node_element) -> list:
        if type(node_element) != GraphNodeAnyElement:
            return None
        return get_differences(self, node_element)


class GraphNodeAttribute:
    _component_name = 'attribute'

    def __init__(self,
                 config: dict,
                 default='',
                 fixed='',
                 form='',  # qualified|unqualified
                 id='',
                 name='',
                 type='',
                 use='optional',  # optional|prohibited|required
                 # ref='', #A LAISSER POUR LES ELEMENTS RECURSIFS?
                 ):

        self._default = default if config['attribute']['default'] else None
        self._fixed = fixed if config['attribute']['fixed'] else None
        self._form = form if config['attribute']['form'] else None
        self._id = id if config['attribute']['id'] else None
        self._name = name if config['attribute']['name'] else None
        self._type = type if config['attribute']['type'] else None
        self._use = use if config['attribute']['use'] else None

    def __str__(self):
        attr_list = [
            f" default=\"{self._default}\"" if self._default != None else "",
            f" fixed=\"{self._fixed}\"" if self._fixed != None else "",
            f" form=\"{self._form}\"" if self._form != None else "",
            f" id=\"{self._id}\"" if self._id != None else "",
            f" name=\"{self._name}\"" if self._name != None else "",
            f" type=\"{self._type}\"" if self._type != None else "",
            f" use=\"{self._use}\"" if self._use != None else "",
        ]

        return "<attribute" + "".join(attr_list) + ">"

    def compare(self, node_element) -> list:
        if type(node_element) != GraphNodeAttribute:
            return None
        if self._name != node_element._name:
            return None
        return get_differences(self, node_element)


class GraphNodeAnyAttribute:
    _component_name = 'anyAttribute'

    def __init__(self, config: dict, id, namespace, process_contents):

        self._id = id if config['any attribute']['id'] else None
        self._namespace = namespace if config['any attribute']['namespace'] else None
        # lax|skip|strict
        self._process_contents = process_contents if config[
            'any attribute']['process_contents'] else None

    def __str__(self):
        attr_list = [
            f" id=\"{self._id}\"" if self._id != None else "",
            f" namespace=\"{self._namespace}\"" if self._namespace != None else "",
            f" processContents=\"{self._process_contents}\"" if self._process_contents != None else "",
        ]

        return "<anyAttribute" + "".join(attr_list) + ">"

    def compare(self, node_element) -> list:
        if type(node_element) != GraphNodeAnyAttribute:
            return None
        differences = [{attribute[1:]: self.__dict__[attribute] for attribute in self.__dict__ if self.__dict__[
            attribute] != node_element.__dict__[attribute]},
            {attribute[1:]: node_element.__dict__[attribute] for attribute in self.__dict__ if self.__dict__[
                attribute] != node_element.__dict__[attribute]}]
        return differences


def createNodeSchema(schema: xmlschema.XMLSchema10, config: dict) -> GraphNodeSchema:
    id = schema.id
    attributeFormDefault = schema.attribute_form_default
    elementFormDefault = schema.element_form_default
    blockDefault = schema.block_default
    finalDefault = schema.final_default
    targetNamespace = schema.target_namespace
    version = schema.version
    xmlns = schema.namespaces
    return GraphNodeSchema(config, xmlns, id, attributeFormDefault,
                           elementFormDefault,
                           blockDefault,
                           finalDefault,
                           targetNamespace,
                           version,)


def createNodeElement(element: xmlschema.XsdElement, target_namespace: str, config: dict) -> GraphNodeElement:
    abstract = element.abstract if hasattr(element, 'abstract') else False
    block = element._block
    default = element.default
    final = element._final
    fixed = element.fixed
    if element.form != None:
        form = element.form
    else:
        form = element.qualified
    id = element.id
    if not element.occurs:
        minOccurs = 1
        maxOccurs = 1
    else:
        minOccurs = element.occurs[0]
        maxOccurs = element.occurs[1] if element.occurs[1] != None else "unbounded"

    # name = removeSpecificNamespace(element.name, target_namespace)
    name = element.name
    nillable = element.nillable
    typ = get_type_of_xsd_element(element)

    return GraphNodeElement(
        config,
        abstract,
        block,
        default,
        final,
        fixed,
        form,
        id,
        minOccurs,
        maxOccurs,
        name,
        nillable,
        typ)


def createNodeAnyElement(any_element: xmlschema.validators.wildcards.XsdAnyElement, config: dict):
    id = any_element.id
    if not any_element.occurs:
        minOccurs = 1
        maxOccurs = 1
    else:
        minOccurs = any_element.occurs[0]
        maxOccurs = any_element.occurs[1] if any_element.occurs[1] != None else "unbounded"
    namespace = any_element.namespace if any_element.namespace != None else (
        '##any',) if config['any']['namespace'] else ''
    process_contents = any_element.process_contents if any_element.process_contents != None else 'strict'

    return GraphNodeAnyElement(config, id, minOccurs, maxOccurs, namespace, process_contents)


def createNodeAttribute(attribute: xmlschema.XsdAttribute, target_namespace: str, config: dict):
    default = attribute.default
    fixed = attribute.fixed
    if attribute.form != None:
        form = attribute.form
    else:
        form = attribute.qualified
    id = attribute.id
    name = attribute.name
    # name = removeSpecificNamespace(attribute.name, target_namespace) if attribute.name != None else ''
    typ = get_type_of_xsd_element(
        attribute) if attribute.type != None and attribute.type.name != None else None
    use = attribute.use
    return GraphNodeAttribute(config, default, fixed, form, id, name, typ, use)


def createNodeAnyAttribute(any_attribute: xmlschema.validators.wildcards.XsdAnyAttribute, config: dict):
    id = any_attribute.id
    namespace = any_attribute.namespace
    process_contents = any_attribute.process_contents
    return GraphNodeAnyAttribute(config, id, namespace, process_contents)


def removeAnyNamespace(name_with_namespace: str):
    return re.sub("[\{].*?[\}]", "", name_with_namespace)


def removeSpecificNamespace(name_with_namespace: str, namespace: str):
    return re.sub("\{" + namespace + "\}", "", name_with_namespace)


def hash_dict(dic: dict) -> int:
    print(dic)
    res_set = frozenset().union(
        [frozenset(dic.keys()), frozenset(dic.values())])
    return hash(res_set.__str__())


def get_type_of_xsd_element(element):
    if element.type.is_simple() or element.type.has_simple_content():
        simple_type_tree = get_simple_type_tree(element.type)
        return f"simpleType {str(simple_type_tree)}"
    elif element.type.is_complex():
        return f"complexType{' mixed' if element.type.has_mixed_content() else ''}"
    else:
        print(
            f"Found unsupported type {element.type}: {type(element.type.__dict__)}")
        return None
    return res


def build_xsd_graph(schema: xmlschema.XMLSchema10, config: dict):
    labeldict = {}
    graph = nx.DiGraph()

    first_node = createNodeSchema(schema, config)
    target_namespace = schema.target_namespace
    graph.add_node(first_node)
    labeldict[first_node] = 'schema'

    queue = [(schema, first_node)]
    visited = set()
    while queue != []:
        element, element_node = queue.pop()
        visited.add(element)
        for position_sequence, child in enumerate(element):
            if child not in visited:
                if type(child) == xmlschema.XsdElement:
                    child_node = createNodeElement(
                        child, target_namespace, config)
                    if child.parent != None and child.parent.model == 'sequence':
                        child_node._index_in_sequence = position_sequence
                    if child.parent != None:
                        child_node._parent_type = child.parent.model
                elif type(child) == xmlschema.validators.wildcards.XsdAnyElement:
                    child_node = createNodeAnyElement(child, config)
                    if child.parent != None and child.parent.model == 'sequence':
                        child_node._index_in_sequence = position_sequence
                    if child.parent != None:
                        child_node._parent_type = child.parent.model
                else:
                    raise Exception(
                        'ERROR: child is not type element or anyElement : ' + str(type(child)))
                graph.add_node(child_node)
                graph.add_edge(element_node, child_node)
                labeldict[child_node] = child.name if child.name != '' else child.type
                queue.append((child, child_node))
            else:
                continue
        # Si element a des attributs, on ajoute leurs noeuds
        if type(element.attributes) == xmlschema.validators.attributes.XsdAttributeGroup:
            for attribute in element.attributes.iter_components(xmlschema.XsdAttribute):
                child_node = createNodeAttribute(
                    attribute, target_namespace, config)
                if child_node not in labeldict:
                    graph.add_node(child_node)
                    graph.add_edge(element_node, child_node)
                    labeldict[child_node] = attribute.name if attribute.name else attribute.type
            for attribute in element.attributes.iter_components(xmlschema.validators.wildcards.XsdAnyAttribute):
                child_node = createNodeAnyAttribute(attribute, config)
                if child_node not in labeldict:
                    graph.add_node(child_node)
                    graph.add_edge(child_node, element_node)
                    labeldict[child_node] = attribute.name if attribute.name else attribute.type
    return graph, first_node, labeldict


if __name__ == '__main__':
    from config_builder import get_default_config

    path_original_xsd = sys.argv[1]
    schema = xmlschema.XMLSchema(path_original_xsd)
    graph, fst, labeldict = build_xsd_graph(schema, get_default_config())

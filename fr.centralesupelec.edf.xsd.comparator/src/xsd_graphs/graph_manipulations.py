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

import cutie
import networkx as nx


def get_list_of_successors(graph: nx.DiGraph, node) -> list:
    """
    Returns the list of nodes of graph that are (in)direct successors of `node`,
    including `node`.
    """
    res = nx.descendants(graph, node)
    res.add(node)
    return list(res)


def get_root_elements_graph_to_ignore(graph1, root1, graph2, root2, root_element_to_keep=None):
    """
    Supprimer les éléments de schéma1 et schema2 sélectionnés par l'utilisateur.
    """
    root_elts1 = [e1 for e1 in graph1.neighbors(root1)]
    root_elts2 = [e2 for e2 in graph2.neighbors(root2)]

    if len(root_elts1) == len(root_elts2) <= 1:
        # There si no ambiguity on the root element
        return [], []

    elif root_element_to_keep:
        to_del1 = [elt for elt in root_elts1 if elt.get_name_without_any_ns()
                   != root_element_to_keep]
        to_del2 = [elt for elt in root_elts2 if elt.get_name_without_any_ns()
                   != root_element_to_keep]

        if len(to_del1) == len(root_elts1):
            print(
                f"Warning: Element '{root_element_to_keep}' not found in XSD 1.")
        if len(to_del2) == len(root_elts2):
            print(
                f"Warning: Element '{root_element_to_keep}' not found in XSD 2.")

        return to_del1, to_del2

    all_root_elts = root_elts1 + root_elts2

    print("XSD1 and XSD2 have the several elements at their roots. Which elements to you want to take in account or to ignore ?")

    menu_entry_indices = cutie.select_multiple(
        options=[f"XSD1: {e1._name}" for e1 in root_elts1] +
        [f"XSD2: {e2._name}" for e2 in root_elts2],
        deselected_unticked_prefix="     ",
        deselected_ticked_prefix=" x   ",
        selected_unticked_prefix="[ ]  ",
        selected_ticked_prefix="[x]  ",
        # by default, tick all elements
        ticked_indices=list(range(len(all_root_elts))),
    )

    to_del = [i for i in range(len(all_root_elts))
              if i not in menu_entry_indices]

    # noeuds à supprimer dans graph1
    to_del1 = [all_root_elts[v] for v in to_del if v < len(root_elts1)]
    # noeuds à suprrimer dans graph2
    to_del2 = [all_root_elts[v] for v in to_del if v >= len(root_elts1)]

    return to_del1, to_del2


def remove_descendants(graph: nx.DiGraph, roots_list):
    """
    Given a digraph and a list of nodes, remove all the (in)direct successors of
    nodes from the list.
    """
    nodes_to_remove = []
    for node in roots_list:
        nodes_to_remove += get_list_of_successors(graph, node)
    graph.remove_nodes_from(nodes_to_remove)


def ask_and_delete_root_elements(graph1, root1, graph2, root2, root_element_to_keep):
    """
    Asks the user to select root elements he wants to compare, and
    deletes them from graph1 and graph2 if any.
    """
    to_del1, to_del2 = get_root_elements_graph_to_ignore(
        graph1, root1,
        graph2, root2,
        root_element_to_keep=root_element_to_keep
    )

    remove_descendants(graph1, to_del1)
    remove_descendants(graph2, to_del2)

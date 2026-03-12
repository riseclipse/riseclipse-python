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

from operator import xor

import networkx as nx

from normalizer.xsd2tree import (GraphNodeAnyAttribute, GraphNodeAnyElement,
                                 GraphNodeAttribute, GraphNodeElement)

SHOW_RECURSIVE_DIFFS = False


def root_trees(t1, root1, t2, root2):
    """Create a single digraph dT of free trees t1 and t2
    #   with roots root1 and root2 respectively
    # rename the nodes with consecutive integers
    # so that all nodes get a unique name between both trees

    # our new "fake" root node is 0
    # t1 is numbers from 1 ... n
    # t2 is numbered from n+1 to 2n
    """

    dT = nx.DiGraph()

    newroot1 = 1  # left root will be 1
    newroot2 = nx.number_of_nodes(t1) + 1  # right will be n+1

    # may be overlap in node names here so need separate maps
    # given the old name, what is the new
    namemap1 = {root1: newroot1}
    namemap2 = {root2: newroot2}

    # add an edge from our new root to root1 and root2
    dT.add_edge(0, namemap1[root1])
    dT.add_edge(0, namemap2[root2])

    for i, (v1, v2) in enumerate(nx.bfs_edges(t1, root1)):
        namemap1[v2] = i + namemap1[root1] + 1
        dT.add_edge(namemap1[v1], namemap1[v2])

    for i, (v1, v2) in enumerate(nx.bfs_edges(t2, root2)):
        namemap2[v2] = i + namemap2[root2] + 1
        dT.add_edge(namemap2[v1], namemap2[v2])

    # now we really want the inverse of namemap1 and namemap2
    # giving the old name given the new
    # since the values of namemap1 and namemap2 are unique
    # there won't be collisions
    namemap = {}
    for old, new in namemap1.items():
        namemap[new] = old
    for old, new in namemap2.items():
        namemap[new] = old

    return (dT, namemap, newroot1, newroot2)


# figure out the level of each node, with 0 at root
def assign_levels(G, root):
    level = {}
    level[root] = 0
    for v1, v2 in nx.bfs_edges(G, root):
        level[v2] = level[v1] + 1

    return level

# now group the nodes at each level


def group_by_levels(levels):
    L = {}
    for n, lev in levels.items():
        if lev not in L:
            L[lev] = []
        L[lev].append(n)

    return L

# now lets get the isomorphism by walking the ordered_children


def generate_isomorphism(v, w, M, ordered_children):
    # make sure tree1 comes first
    assert v < w
    M.append((v, w))
    for i, (x, y) in enumerate(zip(ordered_children[v], ordered_children[w])):
        generate_isomorphism(x, y, M, ordered_children)


def get_subtree_of_key(root2: int, i: int) -> int:
    assert 0 < i
    return 1 if i < root2 else 2


def unique_values(d):
    """
    Returns the list of keys k on `d` such that k is the unique key of `d`
    with value `d[k]`.
    """
    seen = {}  # dict (value, key)
    result = set()  # keys with unique values
    for k in d:
        v = d[k]
        if v in seen:
            result.discard(seen[v])
        else:
            seen[v] = k
            result.add(k)
    return list(result)


def print_differences_1(tree, labels, namemap, newroot2):
    """
    Arguments :
     - `labels` label of different nodes in the isomorphism algorithm
     - `namemap` a dictionnary mapping nodes index to name
     - `newroot2` index of the root of subtree 2.

    Prints the names of nodes that are different according to labels dict.
    Depending on `SHOW_RECURSIVE_DIFFS`, elements that have same name but different
    labels (inherited from differences in their subtree) are shown or not.
    Verbose level: 1
    """

    labels_to_print = labels if SHOW_RECURSIVE_DIFFS else {
        k: str(namemap[k]) for k in labels}

    keys = sorted(unique_values(labels_to_print),
                  key=lambda x: labels_to_print[x])

    if keys != []:
        print(f"Unable to match following elements:")
        while keys != []:
            current_key = keys.pop()
            current_node = namemap[current_key]
            # For attributes, print their parent element too
            if type(current_node) == GraphNodeAttribute or type(current_node) == GraphNodeAnyAttribute:
                attributes_prefix = f"in element {namemap[next(tree.predecessors(current_key))].get_name_without_any_ns()}"
            else:
                attributes_prefix = ""

            correct_matches = []
            for other_key in keys:
                differences = current_node.compare(
                    namemap[other_key])
                if get_subtree_of_key(newroot2, current_key) != get_subtree_of_key(newroot2, other_key) and differences:
                    correct_matches.append((other_key, differences))

            if len(correct_matches) == 1:
                similar_element_key, differences_to_print = correct_matches[0]

                string1 = f"XSD{get_subtree_of_key(newroot2, current_key)}: {differences_to_print[0]}"
                string2 = f"XSD{get_subtree_of_key(newroot2, similar_element_key)}: {differences_to_print[1]}"
                if get_subtree_of_key(newroot2, current_key) == 2:
                    string1, string2 = string2, string1

                if type(current_node) == GraphNodeElement:
                    display_name = f"\'{current_node.get_name_without_any_ns()}\'"
                elif type(current_node) == GraphNodeAttribute:
                    display_name = f"\'{current_node._name}\'"
                else:
                    display_name = ""
                print(
                    f"""    {current_node._component_name} {display_name} {attributes_prefix} has different attributes:
        {string1}
        {string2}"""
                )
                keys.remove(similar_element_key)
            else:
                print(
                    f"    XSD{get_subtree_of_key(newroot2, current_key)}: {attributes_prefix} {current_node}")


def print_differences_2(tree, labels, namemap, newroot2):
    """
    Arguments :
     - `labels` label of different nodes in the isomorphism algorithm
     - `namemap` a dictionnary mapping nodes index to name
     - `newroot2` index of the root of subtree 2.

    Prints the names of nodes that are different according to labels dict.
    Depending on `SHOW_RECURSIVE_DIFFS`, elements that have same name but different
    labels (inherited from differences in their subtree) are shown or not.
    Verbose level: 2
    """

    labels_to_print = labels if SHOW_RECURSIVE_DIFFS else {
        k: str(namemap[k]) for k in labels}

    keys = sorted(unique_values(labels_to_print),
                  key=lambda x: labels_to_print[x])

    if keys != []:
        print(f"Unable to match following elements:")
        for k in keys:
            # For attributes, print their parent element too
            if type(namemap[k]) == GraphNodeAttribute or type(namemap[k]) == GraphNodeAnyAttribute:
                attributes_prefix = f"in element {namemap[next(tree.predecessors(k))].get_name_without_any_ns()} "
            else:
                attributes_prefix = ""
            print(
                f"    XSD{get_subtree_of_key(newroot2, k)}: {attributes_prefix}{namemap[k]}")


def xsd_rooted_tree_isomorphism(t1, root1, t2, root2, verbose_level):
    """
    Given two rooted trees `t1` and `t2`,
    with roots `root1` and `root2` respectively
    this routine will determine if they are isomorphic.

    These trees may be either directed or undirected,
    but if they are directed, all edges should flow from the root.

    It returns the isomorphism, a mapping of the nodes of `t1` onto the nodes
    of `t2`, such that two trees are then identical.

    Note that two trees may have more than one isomorphism, and this
    routine just returns one valid mapping.

    Parameters
    ----------
    `t1` :  NetworkX graph
        One of the trees being compared

    `root1` : a node of `t1` which is the root of the tree

    `t2` : undirected NetworkX graph
        The other tree being compared

    `root2` : a node of `t2` which is the root of the tree

    This is a subroutine used to implement `tree_isomorphism`, but will
    be somewhat faster if you already have rooted trees.

    Returns
    -------
    isomorphism : list
        A list of pairs in which the left element is a node in `t1`
        and the right element is a node in `t2`.  The pairs are in
        arbitrary order.  If the nodes in one tree is mapped to the names in
        the other, then trees will be identical. Note that an isomorphism
        will not necessarily be unique.

        If `t1` and `t2` are not isomorphic, then it returns the empty list.
    """

    assert nx.is_tree(t1)
    assert nx.is_tree(t2)

    # get the rooted tree formed by combining them
    # with unique names
    (dT, namemap, newroot1, newroot2) = root_trees(t1, root1, t2, root2)

    # compute the distance from the root, with 0 for our
    levels = assign_levels(dT, 0)

    # height
    h = max(levels.values())

    # collect nodes into a dict by level
    L = group_by_levels(levels)

    # each node has a label, initially set to 0
    label = {v: 0 for v in dT}
    # and also ordered_labels and ordered_children
    # which will store ordered tuples
    ordered_labels = {v: () for v in dT}
    ordered_children = {v: () for v in dT}

    # nothing to do on last level so start on h-1
    # NON! : On commence à h car on veut aussi comparer les feuilles
    # car leurs noms peuvent être différents
    # also nothing to do for our fake level 0, so skip that
    for i in range(h, 0, -1):
        # update the ordered_labels and ordered_children
        # for any children
        for v in L[i]:
            # nothing to do if no children
            if dT.out_degree(v) > 0:
                # get all the pairs of labels and nodes of children
                # and sort by labels
                s = sorted((label[u], u) for u in dT.successors(v))

                # invert to give a list of two tuples
                # the sorted labels, and the corresponding children
                ordered_labels[v], ordered_children[v] = list(zip(*s))

        # now collect and sort the sorted ordered_labels
        # for all nodes in L[i], carrying along the node

        # On rajoute les namemap dedans car on veut vérifier s'ils sont différents
        forlabel = sorted(
            ((ordered_labels[v], str(namemap[v])), v) for v in L[i])

        # now assign labels to these nodes, according to the sorted order
        # starting from 0, where identical ordered_labels get the same label
        current = 0
        added_labels = {}
        for i, (ol, v) in enumerate(forlabel):
            # advance to next label if not 0, and different from previous
            if (i != 0) and (ol != forlabel[i - 1][0]):
                current += 1
            label[v] = current
            added_labels[v] = current

        # Elements that do not match are those added in this loop turn with
        # unique labels.

        if verbose_level == 1:
            print_differences_1(dT, added_labels, namemap, newroot2)
        elif verbose_level == 2:
            print_differences_2(dT, added_labels, namemap, newroot2)
        elif verbose_level == 0:
            pass

    # they are isomorphic if the labels of newroot1 and newroot2 are 0
    isomorphism = []
    if label[newroot1] == 0 and label[newroot2] == 0:
        generate_isomorphism(newroot1, newroot2, isomorphism, ordered_children)

        # get the mapping back in terms of the old names
        # return in sorted order for neatness
        isomorphism = [(namemap[u], namemap[v]) for (u, v) in isomorphism]

    return isomorphism

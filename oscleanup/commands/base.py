# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from six import string_types, text_type, add_metaclass
from prettytable import PrettyTable
from neutronclient.v2_0 import client
from termcolor import cprint
from utils import format_tree, printo
import abc
import sys
import json


@add_metaclass(abc.ABCMeta)
class Tree(object):
    """
    Tree class - supporting tree related functions.
    """

    def format_node(self, t, **args):
        """
        Format the String for Node Heading

        params:
            t -- string - Node Resource Type (example: Networks)
            **args -- dictornary contains key,val

        output : [t key1=val1, key2=val2, key.n=val.n,]
        """

        text = "{} [".format(t)
        for key, val in args.items():
            text = "{} {}={},".format(text, key, val)
        text = "{} ]".format(text)
        return text

    def populate_node(self, data):
        return {'node': data}

    def add_child_node(self, tree, node):
        if 'childs' not in tree:
            tree['childs'] = []
        tree['childs'].append(node)
        return tree

    def print_info_tree(self, data):
        """Printing Green Colored Text."""
        printo(format_tree(data))

    def print_warn_tree(self, data):
        """Printing Red Colored Text."""
        printo(format_tree(data))


@add_metaclass(abc.ABCMeta)
class Print(object):
    """
    Print Class, Supports Print table fn
    """
    def filter_data(self, data, FIELDS):
        """
        filter the data
        """
        if not data:
            return
        printdata = []
        # prepare the print data with the FIELDS key
        for val in data:
            printdata.append({i: val.get(i) for i in FIELDS if i in val})
        return printdata

    def print_table(self, data, FIELDS):
        """
        Prints in the tabular format. Filter out the fields to be printed
        by the FIELDS parameter.
        Ex:
        data =  [{"name": "test1", "age": 40, "address": "ABC"},
                 {"name": "test2", "age": 30, "address": "CBA"}
                ]
        FIELDS =["name", "age"]

        output :  prints only name, age fields in tabular format.

        #TODO:  word wrap
        """

        printdata = self.filter_data(data, FIELDS)
        if not printdata:
            return
        # prepare the prettytable with header as FIELDS
        t = PrettyTable([k for k in FIELDS if k in printdata[0]])
        t.align = 'l'
        # add the printdata as rows
        for val in printdata:
            t.add_row([val.get(k) for k in FIELDS if k in val])
        # printing in the screen
        print t

    def write_json_file(self, data):
        """
        """
        # write result
        with open('neutron_stale_resources.json', 'w') as outfile:
            json.dump(data, outfile)


@add_metaclass(abc.ABCMeta)
class BaseCommand(Tree, Print):
    """
    Abstract Base Class for Commands
    """
    # command name
    name = "base"

    def run(self, **f):
        pass

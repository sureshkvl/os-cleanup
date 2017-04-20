# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from six import string_types, text_type
from termcolor import colored, cprint
import os
import sys


def fff():
    return 10


def get_credentials():
    """Returns the Openstack env variables as a dict."""
    d = {}
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


# The below code is copied from
#  https://github.com/eonpatapon/contrail-api-cli, utils.py
def format_table(rows, sep='  '):
    """Format table

    :param sep: separator between columns
    :type sep: unicode on python2 | str on python3

    Given the table::

        table = [
            ['foo', 'bar', 'foo'],
            [1, 2, 3],
            ['54a5a05d-c83b-4bb5-bd95-d90d6ea4a878'],
            ['foo', 45, 'bar', 2345]
        ]

    `format_table` will return::

        foo                                   bar  foo
        1                                     2    3
        54a5a05d-c83b-4bb5-bd95-d90d6ea4a878
        foo                                   45   bar  2345
    """
    max_col_length = [0] * 100
    # calculate max length for each col
    for row in rows:
        for index, (col, length) in enumerate(zip(row, max_col_length)):
            if len(text_type(col)) > length:
                max_col_length[index] = len(text_type(col))
    formated_rows = []
    for row in rows:
        format_str = sep.join([
            '{:<%s}' % l if i < (len(row) - 1) else '{}'
            for i, (c, l) in enumerate(zip(row, max_col_length))
        ])
        formated_rows.append(format_str.format(*row))
    return '\n'.join(formated_rows)


def format_tree(tree):
    """Format a python tree structure

    Given the python tree::

        tree = {
            'node': ['ROOT', 'This is the root of the tree'],
            'childs': [{
                'node': 'A1',
                'childs': [{
                    'node': 'B1',
                    'childs': [{
                        'node': 'C1'
                    }]
                },
                {
                    'node': 'B2'
                }]
            },
            {
                'node': 'A2',
                'childs': [{
                    'node': 'B3',
                    'childs': [{
                        'node': ['C2', 'This is a leaf']
                    },
                    {
                        'node': 'C3'
                    }]
                }]
            },
            {
                'node': ['A3', 'This is a node'],
                'childs': [{
                    'node': 'B2'
                }]
            }]
        }

    `format_tree` will return::

        ROOT            This is the root of the tree
        ├── A1
        │   ├── B1
        │   │   └── C1
        │   └── B2
        ├── A2
        │   └── B3
        │       ├── C2  This is a leaf
        │       └── C3
        └── A3          This is a node
            └── B2

    """

    def _traverse_tree(tree, parents=None):
        tree['parents'] = parents
        childs = tree.get('childs', [])
        nb_childs = len(childs)
        for index, child in enumerate(childs):
            child_parents = list(parents) + [index == nb_childs - 1]
            tree['childs'][index] = _traverse_tree(
                tree['childs'][index],
                parents=child_parents)
        return tree

    tree = _traverse_tree(tree, parents=[])

    def _get_rows_data(tree, rows):
        prefix = ''
        for p in tree['parents'][:-1]:
            if p is False:
                prefix += '│   '
            else:
                prefix += '    '
        if not tree['parents']:
            pass
        elif tree['parents'][-1] is True:
            prefix += '└── '
        else:
            prefix += '├── '
        if isinstance(tree['node'], string_types):
            tree['node'] = [tree['node']]
        rows.append([prefix + tree['node'][0]] + tree['node'][1:])
        for child in tree.get('childs', []):
            rows = _get_rows_data(child, rows)
        return rows

    rows = _get_rows_data(tree, [])
    return format_table(rows)


def printo(msg, encoding=None, errors='replace', std_type='stdout'):
    """Write msg on stdout. If no encoding is specified
    the detected encoding of stdout is used. If the encoding
    can't encode some chars they are replaced by '?'

    :param msg: message
    :type msg: unicode on python2 | str on python3
    """
    std = getattr(sys, std_type, sys.stdout)
    if encoding is None:
        try:
            encoding = std.encoding
        except:
            encoding = None
    # Fallback to ascii if no encoding is found
    if encoding is None:
        encoding = 'ascii'
    # https://docs.python.org/3/library/sys.html#sys.stdout
    # write in the binary buffer directly in python3
    if hasattr(std, 'buffer'):
        std = std.buffer
    std.write(msg.encode(encoding, errors=errors))
    std.write(b'\n')
    std.flush()

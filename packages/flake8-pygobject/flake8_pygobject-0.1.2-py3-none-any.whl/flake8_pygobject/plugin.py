# -*- coding: utf-8 -*-
# flake8-pygobject
# Copyright (C) Gnomify. All rights reserved.
#
# This software is proprietary. You may not copy, modify, distribute, or
# use it without explicit permission from Gnomify.
# Contact: ghostkoders@gmail.com

import ast

class PyGObjectVisitor(ast.NodeVisitor):
    """
    AST Visitor to detect common PyGObject mistakes:
    1. connect() に関数呼び出しを渡していないか
    2. GLib.idle_add / timeout_add に関数呼び出しを渡していないか
    3. self に GObject.Property を上書きしていないか
    4. builder.get_object() の結果を保持しているか
    """

    def __init__(self):
        self.errors = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute) and node.func.attr == "connect":
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Call):
                self.errors.append((
                    node.lineno, node.col_offset,
                    "PYG001 connect() に関数呼び出しを渡しています"
                ))

        if isinstance(node.func, ast.Attribute) and node.func.attr in ("idle_add", "timeout_add"):
            if len(node.args) >= 1 and isinstance(node.args[0], ast.Call):
                self.errors.append((
                    node.lineno, node.col_offset,
                    f"PYG002 GLib.{node.func.attr} に関数呼び出しを渡しています"
                ))

        if isinstance(node.func, ast.Attribute) and node.func.attr == "get_object":
            parent = getattr(node, "parent", None)
            if not parent or not isinstance(parent, ast.Assign):
                self.errors.append((
                    node.lineno, node.col_offset,
                    "PYG003 builder.get_object() の結果を変数に保持してください"
                ))

        self.generic_visit(node)

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Attribute):
            target = node.targets[0]
            if isinstance(target.value, ast.Name) and target.value.id == "self":
                self.errors.append((
                    node.lineno, node.col_offset,
                    "PYG004 self に GObject.Property を上書きしています"
                ))
        self.generic_visit(node)


class Flake8PyGObjectPlugin:
    name = "flake8-pygobject"
    version = "0.1.0"

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        visitor = PyGObjectVisitor()
        visitor.visit(self.tree)

        for lineno, col_offset, msg in visitor.errors:
            yield lineno, col_offset, msg, type(self)

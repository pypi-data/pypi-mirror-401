#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Base analyser"""

import ast
import sys
import typing as t
from abc import ABC

__all__: t.Tuple[str, ...] = ("BaseAnalyser",)


class BaseAnalyser(ast.NodeVisitor, ABC):
    """Base class for AST analysers"""

    def __init__(self, file_path: str, content: str, in_review: bool = False):
        self.file_path = file_path
        self.content = content
        self.lines = content.splitlines()
        self.tree = None
        self.in_review = in_review
        try:
            self.tree = ast.parse(content, filename=file_path)
        except SyntaxError as e:
            err_msg: str = (
                f"SyntaxError in file '{e.filename}', line {e.lineno}, offset {e.offset}:\n"
                f"    {e.text.strip() if e.text else ''}\n"
                f"    {' ' * ((e.offset or 1) - 1)}^\n"
                f"{e.msg}"
            )
            print(err_msg, file=sys.stderr)
            sys.exit(1)

    def _yn(self, prompt: str) -> bool:
        """Ask yes/no question to reviewer, yes by default"""
        if not self.in_review:
            return True
        user_input = input(f"{prompt}? (Y/n) ").lower().strip()
        return user_input == "" or user_input.startswith("y")

    def _ny(self, prompt: str) -> bool:
        """Ask yes/no question to reviewer, no by default"""
        if not self.in_review:
            return False
        user_input = input(f"{prompt}? (y/N) ").lower().strip()
        return user_input != "" and user_input.startswith("y")

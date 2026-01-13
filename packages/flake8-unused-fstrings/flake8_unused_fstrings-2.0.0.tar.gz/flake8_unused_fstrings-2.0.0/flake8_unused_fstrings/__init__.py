#!/usr/bin/env python3
#
#  __init__.py
"""
Flake8 plugin to catch f-strings with no fields.
"""
#
#  Copyright © 2019-2020 adam hitchcock <adam+python@northisup.com>
#  License: ISC License (ISCL)
#  See the LICENSE file for details.
#

# stdlib
import ast

# 3rd party
import flake8_helper

__author__: str = "adam hitchcock"
__copyright__: str = "2019-2020 adam hitchcock"
__license__: str = "ISC License (ISCL)"
__version__: str = "2.0.0"
__email__: str = "adam+python@northisup.com"

__all__ = ["Plugin", "Visitor"]

NUF001 = "NUF001 f-string without interpolation."


class Visitor(flake8_helper.Visitor):
	"""
	AST node visitor for identifying f-strings with no fields.
	"""

	def visit_JoinedStr(self, node: ast.JoinedStr) -> None:  # noqa: D102
		is_good = any(isinstance(value, ast.FormattedValue) for value in ast.walk(node))

		if not is_good:
			self.errors.append((
					node.lineno,
					node.col_offset,
					NUF001,
					))


class Plugin(flake8_helper.Plugin[Visitor]):
	"""
	A Flake8 plugin which checks for f-strings with no fields.

	:param tree: The abstract syntax tree (AST) to check.
	"""

	name: str = __name__

	#: The plugin version
	version: str = __version__

	visitor_class = Visitor

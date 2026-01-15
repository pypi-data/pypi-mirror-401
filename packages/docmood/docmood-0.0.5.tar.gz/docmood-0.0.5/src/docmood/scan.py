from __future__ import annotations

import ast
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, Sequence


@dataclass(frozen=True)
class DocItem:
    """A single discovered function/method docstring."""

    path: Path
    doc_lineno: int
    doc: str


class _FuncDocVisitor(ast.NodeVisitor):
    """AST visitor that collects function/method docstrings."""

    def __init__(self, *, file_path: Path) -> None:
        """Create a visitor bound to a specific file path."""
        self._file_path = file_path
        self.items: list[DocItem] = []

    # Method names must match ast.NodeVisitor API
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # pylint: disable=invalid-name
        """Visit a function definition node and extract its docstring."""
        self._maybe_add(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # pylint: disable=invalid-name
        """Visit an async function definition node and extract its docstring."""
        self._maybe_add(node)
        self.generic_visit(node)

    def _maybe_add(self, node: ast.AST) -> None:
        """Record the docstring for a function/method node, if present."""
        # Only function/method docstrings (not module/class docstrings).
        if not hasattr(node, "body"):
            return

        body = getattr(node, "body")
        if not isinstance(body, list) or not body:
            return

        first_stmt = body[0]
        if not isinstance(first_stmt, ast.Expr):
            return

        value = first_stmt.value
        if not isinstance(value, ast.Constant) or not isinstance(value.value, str):
            return

        docstring = value.value
        line_number = getattr(first_stmt, "lineno", None)
        if not isinstance(line_number, int):
            return

        self.items.append(
            DocItem(path=self._file_path, doc_lineno=line_number, doc=docstring)
        )


def iter_python_files(root: Path, *, skip_dirs: Sequence[str]) -> Iterator[Path]:
    """Yield Python files under root, skipping specified directories."""
    root = root.resolve()
    skip = set(skip_dirs)

    for dirpath, dirnames, filenames in os.walk(root):
        # Avoid scanning large/irrelevant directories by default.
        dirnames[:] = [d for d in dirnames if d not in skip and not d.startswith(".")]

        for filename in filenames:
            if filename.endswith(".py"):
                yield Path(dirpath) / filename


def iter_function_doc_items(py_file: Path) -> Iterator[DocItem]:
    """Yield discovered function/method docstring items from a single file."""
    try:
        text = py_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return

    try:
        tree = ast.parse(text, filename=str(py_file))
    except SyntaxError:
        return

    visitor = _FuncDocVisitor(file_path=py_file)
    visitor.visit(tree)
    yield from visitor.items


def scan_project(root: Path, *, skip_dirs: Sequence[str]) -> list[DocItem]:
    """Scan a project directory and return all discovered docstring items."""
    files = sorted(iter_python_files(root, skip_dirs=skip_dirs), key=str)
    items: list[DocItem] = []
    for py_file in files:
        items.extend(iter_function_doc_items(py_file))
    return items

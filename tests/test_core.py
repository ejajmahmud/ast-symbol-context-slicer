"""Tests for AST Symbol Context Slicer."""
import unittest
from ast_symbol_context_slicer.core import ASTSymbolSlicer


SAMPLE = """def leaf(v):
    return v * 2

def mid(v):
    return leaf(v) + 1

def unrelated():
    return "noise"
"""


class TestASTSymbolSlicer(unittest.TestCase):
    def test_extracts_closure_and_excludes_unrelated(self):
        slicer = ASTSymbolSlicer(SAMPLE)
        sliced = slicer.slice_symbol("mid", max_hops=2)
        self.assertIn("def leaf", sliced)
        self.assertIn("def mid", sliced)
        self.assertNotIn("unrelated", sliced)

    def test_zero_hops_returns_only_target(self):
        slicer = ASTSymbolSlicer(SAMPLE)
        sliced = slicer.slice_symbol("mid", max_hops=0)
        self.assertIn("def mid", sliced)
        self.assertNotIn("def leaf", sliced)

    def test_missing_symbol_raises(self):
        slicer = ASTSymbolSlicer(SAMPLE)
        with self.assertRaises(KeyError):
            slicer.slice_symbol("does_not_exist")

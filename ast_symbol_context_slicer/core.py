"""Core dependency-closed Python AST symbol slicer for context engineering."""
import ast
from collections import deque
from typing import Dict, List, Set


class ASTSymbolSlicer:
    """Parses Python source and extracts a minimal dependency-closed slice around target symbols."""

    def __init__(self, source: str):
        self.source = source
        self.lines = source.splitlines()
        self.tree = ast.parse(source)
        self.symbols: Dict[str, ast.AST] = {}
        self.deps: Dict[str, Set[str]] = {}
        self._index()

    def _index(self):
        for node in self.tree.body:
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                self.symbols[node.name] = node
        for name, node in self.symbols.items():
            called = set()
            for child in ast.walk(node):
                if isinstance(child, ast.Name) and child.id in self.symbols and child.id != name:
                    called.add(child.id)
            self.deps[name] = called

    def dependency_closure(self, target: str, max_hops: int = 2) -> List[str]:
        if target not in self.symbols:
            raise KeyError(f"Symbol '{target}' not found")
        seen = {target}
        order = [target]
        q = deque([(target, 0)])
        while q:
            cur, depth = q.popleft()
            if depth >= max_hops:
                continue
            for dep in sorted(self.deps.get(cur, set())):
                if dep not in seen:
                    seen.add(dep)
                    order.append(dep)
                    q.append((dep, depth + 1))
        return sorted(order, key=lambda n: self.symbols[n].lineno)

    def slice_symbol(self, target: str, max_hops: int = 2) -> str:
        needed = self.dependency_closure(target, max_hops=max_hops)
        chunks: List[str] = []
        for sym in needed:
            node = self.symbols[sym]
            seg = "\n".join(self.lines[node.lineno - 1:node.end_lineno])
            chunks.append(seg)
        return "\n\n".join(chunks)

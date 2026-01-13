"""Resolve model generation order based on relationships."""

from __future__ import annotations

from collections import deque
from typing import Dict, List


def build_dependency_graph(models: dict) -> Dict[str, List[str]]:
    """Build a dependency graph for model generation order."""
    graph: Dict[str, List[str]] = {name: [] for name in models}

    for model_name, model_info in models.items():
        dependencies = set()
        for rel in model_info.get("relationships", {}).values():
            related_model = rel.get("model")
            rel_type = rel.get("type")
            if not related_model or related_model not in graph:
                continue
            if related_model == model_name:
                continue
            if rel_type in {
                "ForeignKey",
                "OneToOne",
                "OneToOneField",
                "OneToMany",
                "ManyToMany",
                "ManyToManyField",
            }:
                dependencies.add(related_model)

        graph[model_name] = sorted(dependencies)

    return graph


def get_generation_order(dependency_graph: Dict[str, List[str]]) -> List[str]:
    """Return topological order for model generation."""
    detect_circular_dependencies(dependency_graph)

    in_degree: Dict[str, int] = {node: len(deps) for node, deps in dependency_graph.items()}
    reverse_graph: Dict[str, List[str]] = {node: [] for node in dependency_graph}
    for node, deps in dependency_graph.items():
        for dep in deps:
            reverse_graph[dep].append(node)

    queue = deque([node for node, deg in in_degree.items() if deg == 0])
    order: List[str] = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for dependent in reverse_graph.get(node, []):
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    if len(order) != len(dependency_graph):
        raise ValueError("Could not resolve generation order.")

    return order


def detect_circular_dependencies(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Detect circular dependencies in the graph."""
    visited: Dict[str, int] = {node: 0 for node in graph}
    stack: List[str] = []
    cycles: List[List[str]] = []

    def visit(node: str) -> None:
        if visited[node] == 1:
            if node in stack:
                cycle = stack[stack.index(node) :]
                cycles.append(cycle + [node])
            return
        if visited[node] == 2:
            return

        visited[node] = 1
        stack.append(node)
        for dep in graph.get(node, []):
            visit(dep)
        stack.pop()
        visited[node] = 2

    for node in graph:
        if visited[node] == 0:
            visit(node)

    if cycles:
        raise ValueError(f"Circular dependency detected: {cycles}")

    return cycles

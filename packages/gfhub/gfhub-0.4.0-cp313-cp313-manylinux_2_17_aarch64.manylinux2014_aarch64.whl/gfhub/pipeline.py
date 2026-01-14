"""Friendly pipeline module."""

from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy
from typing import Self, cast


class Pipeline:
    """A friendly pipeline representation."""

    def __init__(self) -> None:
        """Create an empty pipeline."""
        super().__setattr__("_nodes", {})
        super().__setattr__("_edges", [])

    def __repr__(self) -> str:
        return f"Pipeline(\n  nodes={self._nodes!r},\n  edges={self._edges!r}\n)"

    def __setattr__(self, name: str, node: Node | dict) -> None:
        if not isinstance(node, Node | dict):
            msg = (
                "A pipeline node should be of type `Node` "
                "(or a dict with keys 'type' and 'config')"
            )
            raise TypeError(msg)
        if isinstance(node, Node):
            node = node.to_dict()
        node = dict(node)
        nodes = cast(dict[str, Node], self._nodes)
        nodes[name] = Node(name, node["type"], node.get("config", {}))

    def __iadd__(self, item: Edge | Node | dict | Iterable) -> Self:
        if not isinstance(item, Edge | Node | dict):
            if isinstance(item, Iterable):
                for _node in item:
                    self += _node
                return self
            msg = (
                "A pipeline node or edge should be of type `Node` or `Edge` "
                "(or an equivalent dict.)"
            )
            raise AttributeError(msg)
        if isinstance(item, Edge | Node):
            item = item.to_dict()
        item = dict(item)
        if "source" in item and "target" in item and len(item) == 2:
            edges = cast(list[Edge], self._edges)
            edges.append(Edge(item["source"], item["target"]))
        else:
            nodes = cast(dict[str, Node], self._nodes)
            nodes[item["name"]] = Node(
                item["name"], item["type"], item.get("config", {})
            )
        return self

    def __getattr__(self, name: str) -> Node:
        nodes = cast(dict[str, Node], self._nodes)
        if name not in nodes:
            msg = f"This pipeline does not contain a node with name {name}."
            raise AttributeError(msg)
        return nodes[name]

    def to_dict(self) -> dict:
        """Convert pipeline to dict representation."""
        return {
            "nodes": [n.to_dict() for n in cast(dict, self._nodes).values()],
            "edges": [e.to_dict() for e in cast(list, self._edges)],
        }


class Node:
    """A node."""

    def __init__(self, name: str, type: str, config: dict) -> None:  # noqa: A002
        """A node."""
        self.name = str(name)
        self.type = str(type)
        self.config = dict(config)

    def __repr__(self) -> str:
        return f"Node(name={self.name!r}, type={self.type!r}, config={self.config!r})"

    def __getitem__(self, idx: int) -> Port:
        return Port(self.name, int(idx))

    def __rshift__(self, other: Node | Port) -> Edge:
        return self[0] >> other

    def to_dict(self) -> dict:
        """Convert a Node to a dict."""
        return {"name": self.name, "type": self.type, "config": self.config}


class Port:
    """A node port."""

    def __init__(self, node: str, index: int) -> None:
        """A node port."""
        self.node = str(node)
        self.index = int(index)

    def __repr__(self) -> str:
        return f"Port(node={self.node!r}, index={self.index!r})"

    def __rshift__(self, other: Port | Node) -> Edge:
        if isinstance(other, Node):
            return self >> other[0]
        return Edge(self, other)

    def to_dict(self) -> dict:
        """Convert a Port to a dict."""
        return {"node": self.node, "index": self.index}


class Edge:
    """A pipeline edge."""

    def __init__(self, source: Port | dict, target: Port | dict) -> None:
        """A pipeline edge."""
        if isinstance(source, Port):
            source = source.to_dict()
        if isinstance(target, Port):
            target = target.to_dict()
        self.source = {
            "node": source["node"],
            "output": source.get("output", source.get("index", 0)),
        }
        self.target = {
            "node": target["node"],
            "input": target.get("input", target.get("index", 0)),
        }

    def __repr__(self) -> str:
        return f"Edge(\n  source={self.source!r},\n  target={self.target!r}\n)"

    def to_dict(self) -> dict:
        """Convert an Edge to a dict."""
        return {"source": deepcopy(self.source), "target": deepcopy(self.target)}

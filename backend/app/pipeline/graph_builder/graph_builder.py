import logging
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class DependencyGraph:
    nodes: list[str] = field(default_factory=list)
    edges: list[tuple[str, str]] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "nodes": self.nodes,
            "edges": self.edges,
        }


class GraphBuilder:
    def build_graph(self, parsed_dependencies: dict) -> dict:
        if not parsed_dependencies:
            logger.warning("build_graph called with empty dependency map.")
            return DependencyGraph().to_dict()

        seen_nodes: set[str] = set()
        seen_edges: set[tuple[str, str]] = set()

        nodes: list[str] = []
        edges: list[tuple[str, str]] = []

        for source_file, imports in parsed_dependencies.items():
            self._add_node(source_file, seen_nodes, nodes)

            for imported_module in imports:
                if not imported_module:
                    continue

                self._add_node(imported_module, seen_nodes, nodes)

                edge = (source_file, imported_module)
                if edge not in seen_edges:
                    edges.append(edge)
                    seen_edges.add(edge)

        graph = DependencyGraph(nodes=nodes, edges=edges)

        logger.info(
            "Dependency graph built: %d nodes, %d edges.",
            len(graph.nodes),
            len(graph.edges),
        )

        return graph.to_dict()

    @staticmethod
    def _add_node(name: str, seen: set[str], nodes: list[str]) -> None:
        if name not in seen:
            nodes.append(name)
            seen.add(name)
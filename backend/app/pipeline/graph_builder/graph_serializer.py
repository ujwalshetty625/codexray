import logging

logger = logging.getLogger(__name__)


class GraphSerializer:
    def serialize_graph(self, nodes: list[str] | set, edges: list[tuple]) -> dict:
        if not nodes and not edges:
            logger.warning("serialize_graph called with empty graph.")
            return {"nodes": [], "edges": []}

        serialized_nodes = sorted(nodes)

        serialized_edges = []
        seen: set[tuple[str, str]] = set()

        for edge in edges:
            if not self._is_valid_edge(edge):
                logger.warning("Skipping malformed edge: %s", edge)
                continue

            source, target = edge[0], edge[1]
            key = (source, target)

            if key in seen:
                continue

            serialized_edges.append({"source": source, "target": target})
            seen.add(key)

        logger.info(
            "Serialized graph: %d nodes, %d edges.",
            len(serialized_nodes),
            len(serialized_edges),
        )

        return {
            "nodes": serialized_nodes,
            "edges": serialized_edges,
        }

    @staticmethod
    def _is_valid_edge(edge) -> bool:
        return (
            isinstance(edge, (tuple, list))
            and len(edge) >= 2
            and isinstance(edge[0], str)
            and isinstance(edge[1], str)
            and edge[0]
            and edge[1]
        )
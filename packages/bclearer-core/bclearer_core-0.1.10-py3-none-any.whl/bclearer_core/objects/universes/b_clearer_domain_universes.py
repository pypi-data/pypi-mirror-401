"""Domain universe container providing access to specialised registries."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from bclearer_interop_services.graph_services.b_simple_graph_service.objects.b_simple_graphs_universe_registries import (
    BSimpleGraphsUniverseRegistries,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


class BClearerDomainUniverses:
    """Aggregate for the various registry types used within a universe."""

    def __init__(self) -> None:
        self._graph_registries = BSimpleGraphsUniverseRegistries(
            owning_b_simple_graphs_universe=self,
        )

    # ------------------------------------------------------------------
    # Graph data object helpers
    # ------------------------------------------------------------------
    def add_graph_data_object(
        self,
        registry_name: str,
        register_name: str,
        graph_name: str,
        graph_object: Any,
    ) -> None:
        """Persist a graph object for the specified registry/register pair."""

        self._graph_registries.add_graph(
            registry_name=registry_name,
            register_name=register_name,
            graph_name=graph_name,
            graph_object=graph_object,
        )

    def remove_graph_data_object(
        self,
        registry_name: str,
        register_name: str,
        graph_name: str,
    ) -> None:
        """Remove a previously stored graph object."""

        self._graph_registries.remove_graph(
            registry_name=registry_name,
            register_name=register_name,
            graph_name=graph_name,
        )

    def list_graph_data_objects(
        self,
        registry_name: str,
        register_name: str,
    ) -> Mapping[str, Any]:
        """Return the graph objects stored for a register."""

        return self._graph_registries.list_graphs(
            registry_name=registry_name,
            register_name=register_name,
        )

    def export_graph_data_objects_to_graph_ml(
        self,
        output_folder: Folders,
    ) -> None:
        """Export all stored graphs to GraphML format."""

        self._graph_registries.export_all_b_simple_graphs_to_graph_ml(
            output_folder=output_folder,
        )


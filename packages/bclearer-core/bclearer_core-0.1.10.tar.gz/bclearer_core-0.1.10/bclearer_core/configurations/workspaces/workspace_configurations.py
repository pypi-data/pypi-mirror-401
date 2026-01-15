from dataclasses import dataclass

from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


@dataclass(frozen=True)
class WorkspaceConfigurations:
    this_run_workspace: Folders

    this_run_human_readable_short_name: (
        str
    )

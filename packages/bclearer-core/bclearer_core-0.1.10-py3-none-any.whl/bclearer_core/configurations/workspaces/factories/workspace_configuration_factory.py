from pathlib import Path

from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common_base.b_source.services.datetime_service.time_helpers.time_getter import (
    now_time_as_string_for_files,
)


def create_workspace_configuration(
    parent_workspace: Folders,
    workspace_type_prefix: (
        str | None
    ) = None,
    workspace_type_suffix: (
        str | None
    ) = None,
) -> WorkspaceConfigurations:
    this_run_human_readable_short_name = (
        now_time_as_string_for_files()
    )

    this_run_workspace = __get_this_run_workspace(
        parent_workspace=parent_workspace,
        this_run_human_readable_short_name=this_run_human_readable_short_name,
        workspace_type_prefix=workspace_type_prefix,
        workspace_type_suffix=workspace_type_suffix,
    )

    workspace_configuration = WorkspaceConfigurations(
        this_run_workspace=this_run_workspace,
        this_run_human_readable_short_name=this_run_human_readable_short_name,
    )

    return workspace_configuration


def __get_this_run_workspace(
    parent_workspace: Folders,
    this_run_human_readable_short_name: str,
    workspace_type_prefix: (
        str | None
    ) = None,
    workspace_type_suffix: (
        str | None
    ) = None,
) -> Folders:
    this_run_workspace_name = __get_this_run_workspace_name(
        this_run_human_readable_short_name=this_run_human_readable_short_name,
        workspace_type_prefix=workspace_type_prefix,
        workspace_type_suffix=workspace_type_suffix,
    )

    this_run_workspace = parent_workspace.get_descendant_file_system_folder(
        relative_path=Path(
            this_run_workspace_name
        )
    )

    this_run_workspace.make_me_on_disk()

    return this_run_workspace


def __get_this_run_workspace_name(
    this_run_human_readable_short_name: str,
    workspace_type_prefix: (
        str | None
    ) = None,
    workspace_type_suffix: (
        str | None
    ) = None,
) -> str:
    workspace_name_components = [
        component
        for component in (
            workspace_type_prefix,
            this_run_human_readable_short_name,
            workspace_type_suffix,
        )
        if component
    ]

    this_run_workspace_name = "_".join(
        workspace_name_components
    )

    return this_run_workspace_name

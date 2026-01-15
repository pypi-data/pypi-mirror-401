from bclearer_core.configurations.workspaces.factories.workspace_configuration_factory import (
    create_workspace_configuration,
)
from bclearer_core.configurations.workspaces.workspace_configurations import (
    WorkspaceConfigurations,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)


def create_service_workspace_configuration(
    this_service_workspace: Folders,
    this_service_workspace_type_prefix: (
        str | None
    ) = None,
    this_service_workspace_type_suffix: (
        str | None
    ) = None,
) -> WorkspaceConfigurations:
    service_workspace_configuration = create_workspace_configuration(
        parent_workspace=this_service_workspace,
        workspace_type_prefix=this_service_workspace_type_prefix,
        workspace_type_suffix=this_service_workspace_type_suffix,
    )

    return (
        service_workspace_configuration
    )

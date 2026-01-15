from bclearer_core.configurations.workspaces.factories.workspace_configuration_factory import (
    create_workspace_configuration,
)
from bclearer_interop_services.file_system_service.objects.folders import (
    Folders,
)
from nf_common_base.b_source.services.b_app_service.configurations.b_app_configurations import (
    BAppConfigurations,
)


def create_and_set_this_b_app_run_workspace_configuration(
    this_b_app_run_nf_workspace: Folders,
    this_b_app_run_workspace_type_prefix: (
        str | None
    ) = None,
    this_b_app_run_workspace_type_suffix: (
        str | None
    ) = None,
) -> None:
    this_b_app_run_workspace_configuration = create_workspace_configuration(
        parent_workspace=this_b_app_run_nf_workspace,
        workspace_type_prefix=this_b_app_run_workspace_type_prefix,
        workspace_type_suffix=this_b_app_run_workspace_type_suffix,
    )

    BAppConfigurations.THIS_B_APP_RUN_WORKSPACE_CONFIGURATION = this_b_app_run_workspace_configuration

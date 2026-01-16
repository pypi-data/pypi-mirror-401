from __future__ import annotations

from typing import Self

from clearskies.columns import (
    HasMany,
)

from clearskies_gitlab.rest.models import (
    gitlab_rest_group_access_token_reference,
    gitlab_rest_group_base,
    gitlab_rest_group_member_reference,
    gitlab_rest_group_project_reference,
    gitlab_rest_group_subgroup_reference,
    gitlab_rest_group_variable_reference,
)


class GitlabRestGroup(
    gitlab_rest_group_base.GitlabRestGroupBase,
):
    """Model for groups."""

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups"

    projects = HasMany(
        gitlab_rest_group_project_reference.GitlabRestGroupProjectReference,
        foreign_column_name="group_id",
    )
    access_tokens = HasMany(
        gitlab_rest_group_access_token_reference.GitlabRestGroupAccessTokenReference,
        foreign_column_name="group_id",
    )
    variables = HasMany(
        gitlab_rest_group_variable_reference.GitlabRestGroupVariableReference,
        foreign_column_name="group_id",
    )
    subgroups = HasMany(
        gitlab_rest_group_subgroup_reference.GitlabRestGroupSubgroupReference,
        foreign_column_name="group_id",
    )
    members = HasMany(
        gitlab_rest_group_member_reference.GitlabRestGroupMemberReference,
        foreign_column_name="group_id",
    )

from __future__ import annotations

from typing import Self

from clearskies.columns import HasMany, HasManySelf, String

from clearskies_gitlab.rest.models import (
    gitlab_rest_group_access_token_reference,
    gitlab_rest_group_base,
    gitlab_rest_group_member_reference,
    gitlab_rest_group_project_reference,
    gitlab_rest_group_variable_reference,
)


class GitlabRestGroupSubgroup(
    gitlab_rest_group_base.GitlabRestGroupBase,
):
    """Model for Subgroups."""

    # id_column_name = "group_id"

    @classmethod
    def destination_name(cls: type[Self]) -> str:
        """Return the slug of the api endpoint for this model."""
        return "groups/:group_id/subgroups"

    group_id = String()

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
    subgroups = HasManySelf(
        foreign_column_name="group_id",
    )
    members = HasMany(
        gitlab_rest_group_member_reference.GitlabRestGroupMemberReference,
        foreign_column_name="group_id",
    )
    # parent_id = BelongsToSelf()
    # parent = BelongsToModel("parent_id")
    # ### Search params
    # skip_groups = Json()
    # all_available = Boolean()
    # search = String()
    # order_by = String()
    # sort = String()
    # visibility = Select(allowed_values=["public", "internal", "private"])
    # with_custom_attributes = Boolean()
    # owned = Boolean()
    # min_access_level = Integer()
    # top_level_only = Boolean()
    # repository_storage = String()
    # marked_for_deletion_on = Datetime(date_format="%Y-%m-%d")

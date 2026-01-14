# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecFlowerClientBuild(TaskSpecFunction):
    """
    TaskSpecFlowerClientBuild specifications.
    """

    def __init__(
        self,
        function: str,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        instructions: list[str] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            function,
            volumes,
            resources,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.instructions = instructions


class TaskValidatorFlowerClientBuild(TaskValidatorFunction):
    """
    TaskValidatorFlowerClientBuild validator.
    """

    instructions: list[str] | None = None

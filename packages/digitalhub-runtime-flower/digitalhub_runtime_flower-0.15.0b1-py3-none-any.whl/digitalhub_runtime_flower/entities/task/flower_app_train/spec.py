# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.spec import TaskSpecFunction, TaskValidatorFunction


class TaskSpecFlowerAppTrain(TaskSpecFunction):
    """
    TaskSpecFlowerAppTrain specifications.
    """

    def __init__(
        self,
        function: str,
        schedule: str | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
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
        self.schedule = schedule


class TaskValidatorFlowerAppTrain(TaskValidatorFunction):
    """
    TaskValidatorFlowerAppTrain validator.
    """

    schedule: str | None = None

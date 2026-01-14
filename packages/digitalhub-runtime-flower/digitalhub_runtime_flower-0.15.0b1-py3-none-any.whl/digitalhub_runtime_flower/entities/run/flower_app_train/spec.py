# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_flower.entities.run._base.spec import RunSpecFlowerRun, RunValidatorFlowerRun


class RunSpecFlowerAppTrain(RunSpecFlowerRun):
    """
    RunSpecFlowerAppTrain specifications.
    """

    def __init__(
        self,
        task: str,
        local_execution: bool = False,
        function: str | None = None,
        workflow: str | None = None,
        volumes: list[dict] | None = None,
        resources: dict | None = None,
        envs: list[dict] | None = None,
        secrets: list[str] | None = None,
        profile: str | None = None,
        schedule: str | None = None,
        fab_source: dict | None = None,
        image: str | None = None,
        base_image: str | None = None,
        requirements: list[str] | None = None,
        parameters: dict | None = None,
        federation: str | None = None,
        superlink: str | None = None,
        root_certificates: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(
            task,
            local_execution,
            function,
            workflow,
            volumes,
            resources,
            envs,
            secrets,
            profile,
            **kwargs,
        )
        self.schedule = schedule
        self.fab_source = fab_source
        self.image = image
        self.base_image = base_image
        self.requirements = requirements
        self.parameters = parameters
        self.federation = federation
        self.superlink = superlink
        self.root_certificates = root_certificates


class RunValidatorFlowerAppTrain(RunValidatorFlowerRun):
    """
    RunValidatorFlowerAppTrain validator.
    """

    # Task parameters
    schedule: str | None = None

    # Function parameters
    fab_source: dict | None = None
    image: str | None = None
    base_image: str | None = None
    requirements: list[str] | None = None

    # Run parameters
    parameters: dict | None = None
    """Run parameters."""

    federation: str | None = None
    """Flower federation."""

    superlink: str | None = None
    """Flower superlink."""

    root_certificates: str | None = None
    """Root certificates."""

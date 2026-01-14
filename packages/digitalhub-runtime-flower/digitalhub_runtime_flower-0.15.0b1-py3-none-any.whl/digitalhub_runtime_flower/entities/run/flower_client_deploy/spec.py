# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_flower.entities.run._base.spec import RunSpecFlowerRun, RunValidatorFlowerRun


class RunSpecFlowerClientDeploy(RunSpecFlowerRun):
    """
    RunSpecFlowerClientDeploy specifications.
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
        image: str | None = None,
        base_image: str | None = None,
        requirements: list[str] | None = None,
        superlink: str | None = None,
        node_config: dict | None = None,
        root_certificates: str | None = None,
        private_key_secret: str | None = None,
        public_key_secret: str | None = None,
        isolation: str | None = None,
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
        self.image = image
        self.base_image = base_image
        self.requirements = requirements
        self.superlink = superlink
        self.node_config = node_config
        self.root_certificates = root_certificates
        self.private_key_secret = private_key_secret
        self.public_key_secret = public_key_secret
        self.isolation = isolation


class RunValidatorFlowerClientDeploy(RunValidatorFlowerRun):
    """
    RunValidatorFlowerClientDeploy validator.
    """

    # Function parameters
    image: str | None = None
    base_image: str | None = None
    requirements: list[str] | None = None

    # Run parameters
    superlink: str | None = None
    """Flower superlink."""

    node_config: dict | None = None
    """Node configuration."""

    root_certificates: str | None = None
    """Root certificates."""

    private_key_secret: str | None = None
    """Private key secret name."""

    public_key_secret: str | None = None
    """Public key string formatted as public key PEM."""

    isolation: str | None = None
    """Whether to use process or subprocess isolation."""

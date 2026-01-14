# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from pydantic import BaseModel


class FABSource(BaseModel):
    """
    FABModel for Flower Application Bundle.
    """

    source: str | None = None
    """Git source."""

    clientapp: str | None = None
    """ClientApp source."""

    serverapp: str | None = None
    """ServerApp source."""

    clientbase64: str | None = None
    """ClientBase64 source."""

    serverbase64: str | None = None
    """ServerBase64 source."""

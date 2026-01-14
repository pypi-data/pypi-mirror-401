# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub_runtime_modelserve.entities.function.modelserve.spec import (
    FunctionSpecModelserve,
    FunctionValidatorModelserve,
)
from digitalhub_runtime_modelserve.entities.function.vllmserve.models import VLLMAdapter


class FunctionSpecVllmserve(FunctionSpecModelserve):
    """
    FunctionSpecVllmserve specifications.
    """

    def __init__(
        self,
        url: str | None = None,
        model_name: str | None = None,
        image: str | None = None,
        adapters: list[dict] | None = None,
    ) -> None:
        super().__init__()
        self.url = url
        self.model_name = model_name
        self.image = image
        self.adapters = adapters


class FunctionValidatorVllmserve(FunctionValidatorModelserve):
    """
    FunctionValidatorVllmserve validator.
    """

    url: str | None = None
    """URL of the VLLMServe service."""

    model_name: str | None = None
    """Name of the model to be used."""

    image: str | None = None
    """Docker image to use for the VLLMServe function."""

    adapters: list[VLLMAdapter] | None = None
    """List of adapters configurations."""

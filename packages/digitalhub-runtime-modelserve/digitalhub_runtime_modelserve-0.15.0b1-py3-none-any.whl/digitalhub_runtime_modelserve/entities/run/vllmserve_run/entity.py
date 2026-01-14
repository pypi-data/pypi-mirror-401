# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing

import requests
from digitalhub.utils.exceptions import EntityError

from digitalhub_runtime_modelserve.entities.run.modelserve_run.entity import RunModelserveRun

if typing.TYPE_CHECKING:
    from digitalhub.entities._base.entity.metadata import Metadata

    from digitalhub_runtime_modelserve.entities.run.vllmserve_run.spec import RunSpecVllmserveRun
    from digitalhub_runtime_modelserve.entities.run.vllmserve_run.status import RunStatusVllmserveRun


class RunVllmserveRun(RunModelserveRun):
    """
    RunVllmserveRun class.
    """

    def __init__(
        self,
        project: str,
        uuid: str,
        kind: str,
        metadata: Metadata,
        spec: RunSpecVllmserveRun,
        status: RunStatusVllmserveRun,
        user: str | None = None,
    ) -> None:
        super().__init__(project, uuid, kind, metadata, spec, status, user)

        self.spec: RunSpecVllmserveRun
        self.status: RunStatusVllmserveRun

    def invoke(
        self,
        method: str = "POST",
        url: str | None = None,
        **kwargs,
    ) -> requests.Response:
        """
        Invoke served model.
        """
        raise EntityError("Invoke method not implemented yet for VllmserveRun.")

# SPDX-FileCopyrightText: © 2025 DSLab - Fondazione Bruno Kessler
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from digitalhub.entities.task._base.builder import TaskBuilder

from digitalhub_runtime_modelserve.entities._base.runtime_entity.builder import RuntimeEntityBuilderVllmserve
from digitalhub_runtime_modelserve.entities._commons.enums import EntityKinds
from digitalhub_runtime_modelserve.entities.task.vllmserve_serve.entity import TaskVllmserveServe
from digitalhub_runtime_modelserve.entities.task.vllmserve_serve.spec import (
    TaskSpecVllmserveServe,
    TaskValidatorVllmserveServe,
)
from digitalhub_runtime_modelserve.entities.task.vllmserve_serve.status import TaskStatusVllmserveServe


class TaskVllmserveServeBuilder(TaskBuilder, RuntimeEntityBuilderVllmserve):
    """
    TaskVllmserveServe builder.
    """

    ENTITY_CLASS = TaskVllmserveServe
    ENTITY_SPEC_CLASS = TaskSpecVllmserveServe
    ENTITY_SPEC_VALIDATOR = TaskValidatorVllmserveServe
    ENTITY_STATUS_CLASS = TaskStatusVllmserveServe
    ENTITY_KIND = EntityKinds.TASK_VLLMSERVE_SERVE.value

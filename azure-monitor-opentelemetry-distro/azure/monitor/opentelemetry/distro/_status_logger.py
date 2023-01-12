# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License in the project root for
# license information.
# --------------------------------------------------------------------------

import socket
from json import dumps
from os import getpid, makedirs
from os.path import exists, join

from azure.monitor.opentelemetry.distro._constants import (
    _CUSTOMER_IKEY,
    _EXTENSION_VERSION,
    _IS_DIAGNOSTICS_ENABLED,
    _get_log_path
)
from azure.monitor.opentelemetry.distro._version import VERSION

_MACHINE_NAME = socket.gethostname()
_STATUS_LOG_PATH = _get_log_path(status_log_path=True)


def _get_status_json(agent_initialized_successfully, pid, reason=None):
    status_json = {
        "AgentInitializedSuccessfully": agent_initialized_successfully,
        "AppType": "python",
        "MachineName": _MACHINE_NAME,
        "PID": pid,
        "SdkVersion": VERSION,
        "Ikey": _CUSTOMER_IKEY,
        "ExtensionVersion": _EXTENSION_VERSION,
    }
    if reason:
        status_json["Reason"] = reason
    return status_json


def log_status(agent_initialized_successfully, reason=None):
    if _IS_DIAGNOSTICS_ENABLED and _STATUS_LOG_PATH :
        pid = getpid()
        status_json = _get_status_json(
            agent_initialized_successfully, pid, reason
        )
        if not exists(_STATUS_LOG_PATH):
            makedirs(_STATUS_LOG_PATH)
        # Change to be hostname and pid
        status_logger_file_name = f"status_{_MACHINE_NAME}_{pid}.json"
        with open(join(_STATUS_LOG_PATH, status_logger_file_name), "w") as f:
            f.seek(0)
            f.write(dumps(status_json))
            f.truncate()

"""Experiment checking module."""

from __future__ import annotations

import logging
from enum import StrEnum
from typing import TYPE_CHECKING, assert_never

from slurmbench.tool import connector as tool_connector
from slurmbench.tool import description as tool_desc

from . import file_system as exp_fs
from . import managers as exp_managers

if TYPE_CHECKING:
    from pathlib import Path


_LOGGER = logging.getLogger(__name__)


class RunOK[M: exp_managers.AnyManager]:
    """OK status."""

    def __init__(self, exp_manager: M) -> None:
        self._exp_manager: M = exp_manager

    def exp_manager(self) -> M:
        """Get experiment manager."""
        return self._exp_manager


class RunErrors(StrEnum):
    """Experiment checks error status before run."""

    NO_PERMISSION = "no_permission"
    READ_CONFIG_FAILED = "read_config_failed"
    MISSING_TOOL_ENV_WRAPPER_SCRIPT = "missing_tool_env_wrapper_script"


def check_before_start[C: tool_connector.AnyWithOptions](
    exp_name: str,
    data_dir: Path,
    work_dir: Path,
    tool_description: tool_desc.Description,
    tool_connector_type: type[C],
) -> RunOK[exp_managers.Manager[C]] | RunErrors:
    """Check experiment."""
    match _check_read_write_access(data_dir, work_dir):
        case PermissionErrors():
            return RunErrors.NO_PERMISSION

    exp_fs_managers = exp_fs.Managers.new(
        data_dir,
        work_dir,
        tool_description,
        exp_name,
    )

    match connector_or_err := instantiate_connector(
        tool_connector_type,
        exp_fs_managers.data().config_yaml(),
    ):
        case RunErrors():
            return connector_or_err
        case tool_connector.WithOptions():
            exp_manager = exp_managers.Manager(
                exp_fs_managers,
                connector_or_err,
            )
        case _:
            assert_never(connector_or_err)

    _LOGGER.debug(
        "Experiment config:\n%s",
        exp_manager.tool_connector().to_yaml_dump(),
    )

    if _missing_env_wrapper_script(exp_manager.fs_managers().data()):
        return RunErrors.MISSING_TOOL_ENV_WRAPPER_SCRIPT

    return RunOK(exp_manager)


class PermissionOK(StrEnum):
    """Permission OK status."""

    READ_WRITE = "read_write"


class PermissionErrors(StrEnum):
    """Permission status."""

    NO_READ_ACCESS = "no_read_access"
    NO_WRITE_ACCESS = "no_write_access"


type PermissionStatus = PermissionOK | PermissionErrors


def _check_read_write_access(data_dir: Path, work_dir: Path) -> PermissionStatus:
    """Check read and write access."""
    match status := _check_read_write_access_data(data_dir):
        case PermissionErrors():
            return status

    match status := _check_read_write_access_work(work_dir):
        case PermissionErrors():
            return status

    return PermissionOK.READ_WRITE


def _check_read_write_access_data(data_dir: Path) -> PermissionStatus:
    """Check read and write access."""
    if not data_dir.exists():
        _LOGGER.critical("Data directory %s does not exist", data_dir)
        return PermissionErrors.NO_READ_ACCESS

    file_test = data_dir / "test_read_write.txt"
    try:
        file_test.write_text("test")
    except OSError as err:
        _LOGGER.critical("No write access to %s with exception: %s", data_dir, err)
        return PermissionErrors.NO_WRITE_ACCESS

    try:
        file_test.read_text()
    except OSError as err:
        _LOGGER.critical("No read access to %s with exception: %s", data_dir, err)
        file_test.unlink()
        return PermissionErrors.NO_READ_ACCESS

    file_test.unlink()

    return PermissionOK.READ_WRITE


def _check_read_write_access_work(work_dir: Path) -> PermissionStatus:
    """Check read and write access."""
    try:
        work_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        _LOGGER.exception("No write access to %s", work_dir)
        return PermissionErrors.NO_WRITE_ACCESS
    file_test = work_dir / "test_read_write.txt"

    try:
        file_test.write_text("test")
    except OSError:
        _LOGGER.exception("No write access to %s", work_dir)
        file_test.unlink(missing_ok=True)
        if not any(work_dir.iterdir()):
            work_dir.rmdir()
        return PermissionErrors.NO_WRITE_ACCESS

    try:
        file_test.read_text()
    except OSError:
        _LOGGER.exception("No read access to %s", work_dir)
        file_test.unlink()
        if not any(work_dir.iterdir()):
            work_dir.rmdir()
        return PermissionErrors.NO_READ_ACCESS

    file_test.unlink()
    if not any(work_dir.iterdir()):
        work_dir.rmdir()

    return PermissionOK.READ_WRITE


# REFACTOR common function so use common ERROR
def instantiate_connector[C: tool_connector.AnyWithOptions](
    connector_type: type[C],
    config_yaml: Path,
) -> C | RunErrors:
    """Instantiate connector."""

    def _leaf_msg(node_ref_path: list[tool_connector.NodeRef]) -> str:
        """Get leaf message."""

        def _ref_str(ref: tool_connector.NodeRef) -> str:
            match ref:
                case tool_connector.Key():
                    return f"at key {ref}"
                case tool_connector.Index():
                    return f"at index {ref}"

        return "Argument leaf has no bash lines builder, " + ", ".join(
            _ref_str(ref) for ref in node_ref_path
        )

    match connector_or_error := connector_type.from_yaml(config_yaml):
        case tool_connector.Error():
            match err := connector_or_error.error():
                case tool_connector.NodeMappingParsingError():
                    path_to_error: list[tool_connector.NodeRef] = [err.node_ref()]
                    child = err.child()

                    while not isinstance(child, tool_connector.ArgParsingError):
                        path_to_error.append(child.node_ref())
                        path_to_error.append(child.node_ref())
                        child = child.child()

                    _LOGGER.critical(child.msg())
                    return RunErrors.READ_CONFIG_FAILED
                case tool_connector.MissingArgumentNameError():
                    _LOGGER.critical(err.msg())
                    return RunErrors.READ_CONFIG_FAILED
                case tool_connector.ExtraArgumentNameError():
                    _LOGGER.critical(err.msg())
                    return RunErrors.READ_CONFIG_FAILED
    return connector_or_error


def _missing_env_wrapper_script(data_exp_fs_manager: exp_fs.DataManager) -> bool:
    """Check missing env wrapper script."""
    if not data_exp_fs_manager.tool_env_script_sh().exists():
        _LOGGER.critical("Missing tool environment wrapper script")
        _LOGGER.info("You can use `draft-env` command to generate a draft script")
        return True
    return False


class SameExperimentConfigs(StrEnum):
    """Same experiment configs OK status."""

    SAME = "same"


class DifferentExperimentConfigs(StrEnum):
    """Different experiment configs error."""

    DIFFERENT_SYNTAX = "different_syntax"
    NOT_SAME = "not_same"


type ExperimentConfigComparison = SameExperimentConfigs | DifferentExperimentConfigs


def compare_config_vs_config_in_data[
    C: tool_connector.AnyWithOptions,
](
    connector: C,
    config_in_data_yaml: Path,
) -> ExperimentConfigComparison:
    """Compare two experimentation configs."""
    match connector_in_data := connector.from_yaml(config_in_data_yaml):
        case tool_connector.Error():
            return DifferentExperimentConfigs.DIFFERENT_SYNTAX

    is_same = connector.is_same(connector_in_data)

    if not is_same:
        _LOGGER.critical(
            "Existing and given experiment configurations are not the same",
        )
        return DifferentExperimentConfigs.NOT_SAME

    return SameExperimentConfigs.SAME

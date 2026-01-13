"""Sample missing inputs."""

from __future__ import annotations

from enum import StrEnum
from typing import TYPE_CHECKING, final

from slurmbench import tab_files

from . import file_system as smp_fs
from . import items as smp
from . import status as smp_status

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator

    from slurmbench.experiment import managers as exp_managers
    from slurmbench.tool import connector as tool_connector
    from slurmbench.tool import description as tool_desc


class MissingInput:
    """Missing input item."""

    @classmethod
    def from_exp_arg_path_to_result(
        cls,
        exp_arg_path_to_result: tool_connector.ExpArgPathWithDataFSManager,
        reason: smp_status.Error,
    ) -> MissingInput:
        """Create missing input from tool input."""

        def _get_help_str(tool_description: tool_desc.Description) -> str:
            """Get help string."""
            return (
                "slurmbench"
                f" {tool_description.topic().cmd()}"
                f" {tool_description.cmd()}"
                f" run"
                " --help"
            )

        tool_description = exp_arg_path_to_result.exp_arg().tool().to_description()
        return cls(
            ",".join(map(str, exp_arg_path_to_result.exp_arg_path())),
            tool_description.topic().name(),
            tool_description.name(),
            exp_arg_path_to_result.exp_arg().experiment_name(),
            reason,
            _get_help_str(tool_description),
        )

    def __init__(  # noqa: PLR0913
        self,
        arg_name: str,
        topic_name: str,
        tool_name: str,
        experiment_name: str,
        reason: smp_status.Error,
        help_string: str,
    ) -> None:
        """Initialize."""
        self.__arg_name = arg_name
        self.__topic_name = topic_name
        self.__tool_name = tool_name
        self.__exp_name = experiment_name
        self.__reason = reason
        self.__help_string = help_string

    def arg_path(self) -> str:
        """Get argument path in the configuration."""
        return self.__arg_name

    def topic_name(self) -> str:
        """Get topic name."""
        return self.__topic_name

    def tool_name(self) -> str:
        """Get tool name."""
        return self.__tool_name

    def experiment_name(self) -> str:
        """Get experiment name."""
        return self.__exp_name

    def reason(self) -> smp_status.Error:
        """Get reason."""
        return self.__reason

    def help(self) -> str:
        """Get help string."""
        return self.__help_string


class MissingInputsTSVHeader(StrEnum):
    """Missing inputs TSV header."""

    ARG_PATH = "arg_path"
    TOPIC = "input_topic"
    TOOL = "input_tool"
    EXPERIMENT = "input_experiment"
    REASON = "reason"
    HELP = "help"


@final
class MissingInputsTSVReader(tab_files.TSVReader[MissingInputsTSVHeader, MissingInput]):
    """Missing inputs TSV reader."""

    @classmethod
    def header_type(cls) -> type[MissingInputsTSVHeader]:
        """Get header type."""
        return MissingInputsTSVHeader

    def __iter__(self) -> Iterator[MissingInput]:
        """Iterate over missing inputs items."""
        for row in self._csv_reader:
            yield MissingInput(
                self._get_cell(row, MissingInputsTSVHeader.ARG_PATH),
                self._get_cell(row, MissingInputsTSVHeader.TOPIC),
                self._get_cell(row, MissingInputsTSVHeader.TOOL),
                self._get_cell(row, MissingInputsTSVHeader.TOOL),
                smp_status.Error(
                    self._get_cell(row, MissingInputsTSVHeader.REASON),
                ),
                self._get_cell(row, MissingInputsTSVHeader.HELP),
            )


@final
class MissingInputsTSVWriter(tab_files.TSVWriter[MissingInputsTSVHeader, MissingInput]):
    """Missing inputs TSV writer."""

    @classmethod
    def header_type(cls) -> type[MissingInputsTSVHeader]:
        """Get header type."""
        return MissingInputsTSVHeader

    @classmethod
    def reader_type(cls) -> type[MissingInputsTSVReader]:
        """Get reader type."""
        return MissingInputsTSVReader

    def _to_cell(self, item: MissingInput, column_id: MissingInputsTSVHeader) -> object:
        """Get cell from item."""
        match column_id:
            case MissingInputsTSVHeader.ARG_PATH:
                return item.arg_path()
            case MissingInputsTSVHeader.TOPIC:
                return item.topic_name()
            case MissingInputsTSVHeader.TOOL:
                return item.tool_name()
            case MissingInputsTSVHeader.EXPERIMENT:
                return item.experiment_name()
            case MissingInputsTSVHeader.REASON:
                return item.reason()
            case MissingInputsTSVHeader.HELP:
                return item.help()


def write_sample_missing_inputs(
    exp_manager: exp_managers.Manager[tool_connector.AnyWithArguments],
    row_numbered_sample: smp.RowNumbered,
    sample_missing_inputs: Iterable[MissingInput],
) -> None:
    """Write sample missing inputs."""
    data_sample_fs_manager = (
        exp_manager.fs_managers()
        .data()
        .sample_fs_manager(
            row_numbered_sample,
        )
    )
    smp_fs.reset_sample_dir(data_sample_fs_manager)
    with MissingInputsTSVWriter.open(
        data_sample_fs_manager.missing_inputs_tsv(),
        "w",
    ) as out_miss_inputs:
        out_miss_inputs.write_bunch(sample_missing_inputs)  # ty:ignore[unresolved-attribute]


def for_sample(
    exp_arg_paths_with_data_fs_managers: list[
        tool_connector.ExpArgPathWithDataFSManager
    ],
    sample: smp.RowNumbered,
) -> list[MissingInput]:
    """Get a list of missing inputs."""
    list_missing_inputs: list[MissingInput] = []
    for exp_arg_path_with_data_fs_manager in exp_arg_paths_with_data_fs_managers:
        sample_fs_manager = (
            exp_arg_path_with_data_fs_manager.data_fs_manager().sample_fs_manager(
                sample,
            )
        )

        match input_status := smp_status.get_status(sample_fs_manager):
            case smp_status.Error():
                list_missing_inputs.append(
                    MissingInput.from_exp_arg_path_to_result(
                        exp_arg_path_with_data_fs_manager,
                        input_status,
                    ),
                )

    return list_missing_inputs

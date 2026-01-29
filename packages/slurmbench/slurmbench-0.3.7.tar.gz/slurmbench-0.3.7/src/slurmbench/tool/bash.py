"""Tools script logics."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, final

from slurmbench.bash import items as bash_items
from slurmbench.samples import bash as smp_sh
from slurmbench.samples import file_system as smp_fs

from . import results

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator
    from pathlib import Path

    from slurmbench.experiment import file_system as exp_fs


class Node(ABC):
    """Tool argument base class."""

    @abstractmethod
    def init_lines(self) -> Iterator[str]:
        """Get shell input init lines."""
        raise NotImplementedError

    def close_lines(self) -> Iterator[str]:
        """Get shell input close lines."""
        # DOCU can be modified
        yield from ()


# FEATURE How to deal with argument tree (mirror the structure here)
class ExpArgLike[R: results.Result](Node):
    """Experiment argument like bash lines builder."""

    _input_result: R
    _input_data_smp_sh_fs_manager: smp_fs.Manager
    _work_exp_fs_manager: exp_fs.WorkManager
    _work_smp_sh_fs_manager: smp_fs.Manager

    def input_result(self) -> R:
        """Get input result."""
        return self._input_result

    def input_data_smp_sh_fs_manager(self) -> smp_fs.Manager:
        """Get input data sample shell file system manager."""
        return self._input_data_smp_sh_fs_manager

    def work_exp_fs_manager(self) -> exp_fs.WorkManager:
        """Get working experiment file system manager."""
        return self._work_exp_fs_manager

    def work_smp_sh_fs_manager(self) -> smp_fs.Manager:
        """Get working sample shell file system manager."""
        return self._work_smp_sh_fs_manager


type AnyExpArgLike = ExpArgLike[results.Result]


# FEATURE How to deal with argument tree (mirror the structure here)
class ExpArg[R: results.Result](ExpArgLike[R]):
    """Experiment argument bash lines builder."""

    def __init__(
        self,
        input_result: R,
        work_exp_fs_manager: exp_fs.WorkManager,
    ) -> None:
        """Initialize."""
        self._input_result = input_result
        self._input_data_smp_sh_fs_manager = (
            input_result.exp_fs_manager().sample_sh_var_fs_manager()
        )
        self._work_exp_fs_manager = work_exp_fs_manager
        self._work_smp_sh_fs_manager = (
            self._work_exp_fs_manager.sample_sh_var_fs_manager()
        )


type AnyExpArg = ExpArg[results.Result]


class Options:
    """Bash lines builder for user tool options."""

    USER_TOOL_OPTIONS_VAR = bash_items.Variable("USER_TOOL_OPTIONS")

    def __init__(self, tool_options: Iterable[str]) -> None:
        """Initialize."""
        self.__tool_options = tool_options

    def tool_options(self) -> Iterable[str]:
        """Get tool options."""
        return self.__tool_options

    def set_options(self) -> Iterator[str]:
        """Set user tool options sh array variable."""
        yield self.USER_TOOL_OPTIONS_VAR.set(
            "(" + " ".join(self.__tool_options) + ")",
        )


class WithOptions(ABC):
    """Commands with options."""

    WORK_EXP_SAMPLE_DIR_VAR = bash_items.Variable("WORK_EXP_SAMPLE_DIR")

    CORE_COMMAND_SH_FILENAME = "core_command.sh"

    @classmethod
    @final
    def core_command_sh_path(cls, tool_bash_script_dir: Path) -> Path:
        """Get core command shell path."""
        return tool_bash_script_dir / cls.CORE_COMMAND_SH_FILENAME

    def __init__(
        self,
        opts_sh_lines_builder: Options,
        exp_fs_managers: exp_fs.Managers,
        tool_bash_script_dir: Path,
    ) -> None:
        """Initialize."""
        self._opts_sh_lines_builder = opts_sh_lines_builder
        self._exp_fs_managers = exp_fs_managers
        self._tool_bash_script_dir = tool_bash_script_dir

    @abstractmethod
    def init_lines(self) -> Iterator[str]:
        """Iterate over core command shell input init lines."""
        raise NotImplementedError

    @abstractmethod
    def close_lines(self) -> Iterator[str]:
        """Iterate over core command shell input close lines."""
        raise NotImplementedError

    # DOCU can be modified for custom only options tool
    def init_output_lines(self) -> Iterator[str]:
        """Iterate over core command shell output init lines."""
        yield from ()

    # DOCU can be modified for custom only options tool
    def close_output_lines(self) -> Iterator[str]:
        """Iterate over core command shell output close lines."""
        yield from ()

    @final
    def commands(self) -> Iterator[str]:
        """Iterate over the tool commands."""
        # DOCU say WORK_EXP_SAMPLE_DIR variable is set
        # DOCU say SAMPLES_TSV variable is set
        yield from smp_sh.SampleUIDLinesBuilder(
            self._exp_fs_managers.data().samples_tsv(),
        ).lines()
        yield ""
        yield from self.set_work_sample_exp_dir()
        yield from self.mkdir_work_sample_exp_dir()
        yield ""
        yield from self._opts_sh_lines_builder.set_options()
        yield ""
        yield from self.init_lines()
        yield ""
        yield from self.core_commands()
        yield ""
        yield from self.close_lines()

    def opts_sh_lines_builder(self) -> Options:
        """Get options bash lines builder."""
        return self._opts_sh_lines_builder

    def exp_fs_managers(self) -> exp_fs.Managers:
        """Get experiment file system managers."""
        return self._exp_fs_managers

    def set_work_sample_exp_dir(self) -> Iterator[str]:
        """Set working experiment sample directory."""
        work_exp_sample_sh_var_dir = self._exp_fs_managers.work().sample_sh_var_dir()
        yield self.WORK_EXP_SAMPLE_DIR_VAR.set(
            bash_items.path_to_str(work_exp_sample_sh_var_dir),
        )

    @final
    def mkdir_work_sample_exp_dir(self) -> Iterator[str]:
        """Mkdir working experiment sample directory."""
        yield f"mkdir -p {self.WORK_EXP_SAMPLE_DIR_VAR.eval()} 2>/dev/null"

    @final
    def core_commands(self) -> Iterator[str]:
        """Iterate over the tool command lines."""
        core_command_shell_path = self.core_command_sh_path(self._tool_bash_script_dir)

        with core_command_shell_path.open("r") as in_core_cmd:
            for line in in_core_cmd:
                yield line.rstrip()


class OnlyOptions(WithOptions):
    """Tool commands when the tool has no arguments."""

    @final
    def init_lines(self) -> Iterator[str]:
        """Iterate over core command shell input init lines."""
        yield from self.init_output_lines()

    @final
    def close_lines(self) -> Iterator[str]:
        """Iterate over core command shell input close lines."""
        yield from self.close_output_lines()


class WithArguments(WithOptions):
    """Tool commands with options and arguments."""

    @final
    def __init__(
        self,
        arg_sh_lines_builders: Iterable[Node],
        opts_sh_lines_builder: Options,
        exp_fs_managers: exp_fs.Managers,
        _tool_bash_script_dir: Path,
    ) -> None:
        """Initialize."""
        self._arg_sh_lines_builders = list(arg_sh_lines_builders)
        super().__init__(opts_sh_lines_builder, exp_fs_managers, _tool_bash_script_dir)

    @final
    def arg_sh_lines_builders(self) -> Iterator[Node]:
        """Get argument bash lines builders."""
        yield from self._arg_sh_lines_builders

    @final
    def init_lines(self) -> Iterator[str]:
        """Iterate over core command shell input init lines."""
        for result_lines_builder in self._arg_sh_lines_builders:
            yield from result_lines_builder.init_lines()
        yield from self.init_output_lines()

    @final
    def close_lines(self) -> Iterator[str]:
        """Iterate over core command shell input close lines."""
        for result_lines_builder in self._arg_sh_lines_builders:
            yield from result_lines_builder.close_lines()
        yield from self.close_output_lines()

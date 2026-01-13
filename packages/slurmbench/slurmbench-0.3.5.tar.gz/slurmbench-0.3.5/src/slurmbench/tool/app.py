"""Tool abstract application module."""

# Due to typer usage:
# ruff: noqa: TC003, FBT002, FBT001

from __future__ import annotations

import datetime
import logging
import shutil
from collections.abc import Callable
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer

import slurmbench.experiment.checks as exp_checks
import slurmbench.experiment.file_system as exp_fs
import slurmbench.experiment.managers as exp_managers
import slurmbench.experiment.report as exp_report
import slurmbench.experiment.resume as exp_resume
import slurmbench.experiment.run as exp_run
import slurmbench.samples.status as smp_status
import slurmbench.slurm.config as slurm_cfg
from slurmbench import root_logging

from . import bash
from . import connector as tool_connector
from . import description as tool_desc
from . import environments as tool_env

_LOGGER = logging.getLogger(__name__)


def log_filename() -> Path:
    """Get log filename."""
    return Path(
        "slurmbench_"
        + datetime.datetime.now(tz=None).strftime("%Y-%m-%dT%H_%M_%S")  # noqa: DTZ005
        + ".log",
    )


class RichHelp(StrEnum):
    """Rich help categories."""

    MAIN_CMD = "Main commands"
    UTILS_CMD = "Utilities"


def new[C: tool_connector.AnyWithOptions](
    description: tool_desc.Description,
    connector_type: type[C],
) -> typer.Typer:
    """Build tool application."""
    app = typer.Typer(
        name=description.cmd(),
        help=f"Subcommand for tool `{description.name()}`",
        rich_markup_mode="rich",
    )
    #
    # Run app
    #
    run_app = Run(description, connector_type)
    app.command(
        name=run_app.NAME,
        help=run_app.help(),
        rich_help_panel=RichHelp.MAIN_CMD,
    )(run_app.main)
    #
    # Resume app
    #
    resume_app = Resume(description, connector_type)
    app.command(
        name=resume_app.NAME,
        help=resume_app.help(),
        rich_help_panel=RichHelp.MAIN_CMD,
    )(resume_app.main)
    #
    # Config app
    #
    config_app = Config(description, connector_type)
    app.command(
        name=config_app.NAME,
        help=config_app.help(),
        rich_help_panel=RichHelp.UTILS_CMD,
    )(config_app.main)
    #
    # Draft tool environment script app
    #
    draft_env_sh_app = ToolEnvWrapper(description, connector_type)
    app.command(
        name=draft_env_sh_app.NAME,
        help=draft_env_sh_app.help(),
        rich_help_panel=RichHelp.UTILS_CMD,
    )(draft_env_sh_app.main)
    #
    # Report app
    #
    report_app = Report(description)
    app.command(
        name=report_app.NAME,
        help=report_app.help(),
        rich_help_panel=RichHelp.UTILS_CMD,
    )(report_app.main)
    return app


class Arguments:
    """Tool application arguments."""

    EXP_NAME = typer.Argument(
        help="Name of the experiment",
    )

    DATA_DIR = typer.Argument(
        help="Path to the data directory (preferably absolute)",
    )


class RunArgs:
    """Run command arguments."""

    WORK_DIR = typer.Argument(
        help="Path to the working directory (preferably absolute)",
    )


class RunOptions:
    """Run command options."""

    __RUN_CATEGORY = "Samples to run"
    __SLURM_OPTS = "SLURM configurations"

    # FEATURE Implement run options
    RUN_SUCCESS = typer.Option(
        "--success/--skip-success",
        help="Run the experiment for samples that succeeded",
        rich_help_panel=__RUN_CATEGORY,
    )
    RUN_NOT_RUN = typer.Option(
        "--not-run/--skip-not-run",
        help="Run the experiment for samples that were not run (default)",
        rich_help_panel=__RUN_CATEGORY,
    )
    RUN_MISSING_INPUTS = typer.Option(
        "--missing-inputs/--skip-missing-inputs",
        help="Run the experiment for samples that have missing inputs",
        rich_help_panel=__RUN_CATEGORY,
    )
    RUN_ERROR = typer.Option(
        "--error/--skip-error",
        help="Run the experiment for failed samples",
        rich_help_panel=__RUN_CATEGORY,
    )
    RUN_ALL = typer.Option(
        "--all",
        help="Run the experiment for all samples",
        rich_help_panel=__RUN_CATEGORY,
    )
    SLURM_OPTIONS = typer.Option(
        "--slurm-opts",
        help="SLURM options",
        rich_help_panel=__SLURM_OPTS,
    )


class Run[C: tool_connector.AnyWithOptions]:
    """Run application."""

    NAME = "run"

    def __init__(
        self,
        description: tool_desc.Description,
        connector_type: type[C],
    ) -> None:
        """Initialize."""
        self._description: tool_desc.Description = description
        self._connector_type: type[C] = connector_type

    def description(self) -> tool_desc.Description:
        """Get tool description."""
        return self._description

    def connector_type(self) -> type[C]:
        """Get connector."""
        return self._connector_type

    def help(self) -> str:
        """Get help string."""
        return (
            f"Run {self._description.name()} ({self._description.topic().name()}) tool."
        )

    def main(  # noqa: PLR0913
        self,
        exp_name: Annotated[str, Arguments.EXP_NAME],
        data_dir: Annotated[Path, Arguments.DATA_DIR],
        work_dir: Annotated[Path, RunArgs.WORK_DIR],
        run_success: Annotated[bool, RunOptions.RUN_SUCCESS] = False,
        run_not_run: Annotated[bool, RunOptions.RUN_NOT_RUN] = True,
        run_missing_inputs: Annotated[bool, RunOptions.RUN_MISSING_INPUTS] = False,
        run_error: Annotated[bool, RunOptions.RUN_ERROR] = False,
        run_all: Annotated[bool, RunOptions.RUN_ALL] = False,
        slurm_opts: Annotated[str | None, RunOptions.SLURM_OPTIONS] = None,
        debug: Annotated[bool, root_logging.OPT_DEBUG] = False,
    ) -> None:
        """Run tool."""
        root_logging.init_logger(
            _LOGGER,
            (
                f"Run experiment `{exp_name}`"
                f" for tool {self._description.name()}"
                f" for topic {self._description.topic().name()}"
            ),
            debug,
            log_file=log_filename(),
        )

        exp_manager = self._successfull_check_before_start_or_errror(
            exp_name,
            data_dir,
            work_dir,
        )
        self._error_if_experiment_is_running(exp_manager)

        if slurm_opts is None:
            slurm_opts = slurm_cfg.default_slurm_options(None)

        exp_run.start_new_experiment(
            exp_manager,
            self._target_samples_to_run(
                run_success,
                run_not_run,
                run_missing_inputs,
                run_error,
                run_all,
            ),
            slurm_opts,
        )
        raise typer.Exit(0)

    def _error_if_experiment_is_running(
        self,
        exp_manager: exp_managers.Manager[C],
    ) -> None:
        """Exit with error if the experiment is already running."""
        match running_exp := exp_report.running_experiment(
            exp_manager.fs_managers().data(),
        ):
            case exp_report.RunningExperiment():
                _LOGGER.critical(
                    "The experiment is already in progress\n"
                    "* Experiment launched the: %s\n"
                    "* Working directory root path: %s\n"
                    "* SLURM job ID: %s\n"
                    "* SACCT state: %s\n",
                    running_exp.in_progress_data().date(),
                    running_exp.in_progress_data().working_directory(),
                    running_exp.in_progress_data().job_id(),
                    running_exp.sacct_state(),
                )
                _LOGGER.info("You must use the `resume` command")
                raise typer.Exit(1)

    def _successfull_check_before_start_or_errror(
        self,
        exp_name: str,
        data_dir: Path,
        work_dir: Path,
    ) -> exp_managers.Manager[C]:
        #
        # Resolve absolute paths
        #
        data_dir = data_dir.resolve()
        work_dir = work_dir.resolve()

        match check_result := exp_checks.check_before_start(
            exp_name,
            data_dir,
            work_dir,
            self._description,
            self._connector_type,
        ):
            case exp_checks.RunOK():
                return check_result.exp_manager()
            case exp_checks.RunErrors():
                _LOGGER.critical("The experiment checkers found errors")
                raise typer.Exit(1)

    def _target_samples_to_run(
        self,
        run_success: bool,
        run_not_run: bool,
        run_missing_inputs: bool,
        run_error: bool,
        run_all: bool,
    ) -> Callable[[smp_status.Status], bool]:
        targets_to_run_filter: dict[smp_status.Status, bool] = dict.fromkeys(
            (
                smp_status.Success.OK,
                smp_status.Error.NOT_RUN,
                smp_status.Error.MISSING_INPUTS,
                smp_status.Error.ERROR,
            ),
            run_all,
        )
        if not run_all:
            targets_to_run_filter[smp_status.Success.OK] = run_success
            targets_to_run_filter[smp_status.Error.NOT_RUN] = run_not_run
            targets_to_run_filter[smp_status.Error.MISSING_INPUTS] = run_missing_inputs
            targets_to_run_filter[smp_status.Error.ERROR] = run_error
        return lambda status: targets_to_run_filter[status]


class Resume[C: tool_connector.AnyWithOptions]:
    """Resume application class."""

    NAME = "resume"

    def __init__(
        self,
        description: tool_desc.Description,
        connector_type: type[C],
    ) -> None:
        """Initialize."""
        self._description = description
        self._connector_type: type[C] = connector_type

    def description(self) -> tool_desc.Description:
        """Get tool description."""
        return self._description

    def connector_type(
        self,
    ) -> type[C]:
        """Get connector."""
        return self._connector_type

    def main(
        self,
        exp_name: Annotated[str, Arguments.EXP_NAME],
        data_dir: Annotated[Path, Arguments.DATA_DIR],
        debug: Annotated[bool, root_logging.OPT_DEBUG] = False,
    ) -> None:
        """Resume the tool jobs."""
        root_logging.init_logger(
            _LOGGER,
            (
                f"Resume experiment `{exp_name}`"
                f" for tool {self._description.name()}"
                f" for topic {self._description.topic().name()}"
            ),
            debug,
            log_file=log_filename(),
        )

        exp_manager, array_job_id = self._retrieve_exp_manager_array_job_id(
            exp_name,
            data_dir,
        )

        exp_resume.resume(exp_manager, array_job_id)

        raise typer.Exit(0)

    def _retrieve_exp_manager_array_job_id(
        self,
        exp_name: str,
        data_dir: Path,
    ) -> tuple[exp_managers.Manager[C], str]:
        #
        # Resolve absolute paths
        #
        data_fs_manager = exp_fs.DataManager(
            data_dir.resolve(),
            self._description,
            exp_name,
        )
        running_experiment = exp_report.running_experiment(data_fs_manager)
        if running_experiment is None:
            _LOGGER.critical(
                "The experiment `%s` is not in progress for tool `%s` and topic `%s`",
                exp_name,
                self._description.name(),
                self._description.topic().name(),
            )
            raise typer.Exit(1)

        work_fs_manager = exp_fs.WorkManager(
            running_experiment.in_progress_data().working_directory(),
            self._description,
            exp_name,
        )
        connector = exp_checks.instantiate_connector(
            self.connector_type(),
            data_fs_manager.config_yaml(),
        )

        if isinstance(connector, exp_checks.RunErrors):
            _LOGGER.critical("Cannot instantiate connector")
            raise typer.Exit(1)

        return exp_managers.Manager(
            exp_fs.Managers(data_fs_manager, work_fs_manager),
            connector,
        ), running_experiment.in_progress_data().job_id()

    def help(self) -> str:
        """Get help string."""
        return (
            "Complete slurmbench jobs for"
            f" {self._description.name()}"
            f" ({self._description.topic().name()}) tool."
        )


class ConfigOpts:
    """Config options."""

    EXP_CONFIG_YAML = typer.Option(
        "-c",
        "--exp-config-yaml",
        help="Path to the experiment configuration clone YAML file",
    )


class Config[C: tool_connector.AnyWithOptions]:
    """Config application class."""

    NAME = "config"

    def __init__(
        self,
        description: tool_desc.Description,
        connector_type: type[C],
    ) -> None:
        """Initialize."""
        self._description = description
        self._connector_type: type[C] = connector_type

    def description(self) -> tool_desc.Description:
        """Get tool description."""
        return self._description

    def connector_type(self) -> type[C]:
        """Get connector."""
        return self._connector_type

    def help(self) -> str:
        """Get help string."""
        return (
            "Get a configuration YAML file draft"
            f" for tool {self._description.topic().name()}"
        )

    def main(
        self,
        exp_name: Annotated[str, Arguments.EXP_NAME],
        data_dir: Annotated[Path, Arguments.DATA_DIR],
        config_exp_yaml: Annotated[Path | None, ConfigOpts.EXP_CONFIG_YAML] = None,
        debug: Annotated[bool, root_logging.OPT_DEBUG] = False,
    ) -> None:
        """Get draft config."""
        root_logging.init_logger(
            _LOGGER,
            "Generating a configuration file draft"
            f" for topic: {self._description.topic().name()}"
            f" tool: {self._description.name()}",
            debug,
        )

        data_exp_fs_manager = exp_fs.DataManager(
            data_dir.resolve(),
            self._description,
            exp_name,
        )

        data_exp_fs_manager.exp_dir().mkdir(parents=True, exist_ok=True)
        self._connector_type.to_example_yaml(data_exp_fs_manager.config_yaml())
        _LOGGER.info(
            "Tool configuration written into the data experiment directory: %s",
            data_exp_fs_manager.config_yaml(),
        )
        if config_exp_yaml is not None:
            shutil.copy(data_exp_fs_manager.config_yaml(), config_exp_yaml)
            _LOGGER.info(
                "Copy the tool configuration file to: %s",
                config_exp_yaml,
            )
        raise typer.Exit(0)


class ToolEnvWrapperOpts:
    """Tool environnment wrapper options."""

    ERASE = typer.Option(
        "--erase/--do-not-erase",
        help="Erase existing tool environnment wrapper script",
    )


class ToolEnvWrapper[C: tool_connector.AnyWithOptions]:
    """Draft tool environnment wrapper script."""

    NAME = "draft-env"

    def __init__(
        self,
        description: tool_desc.Description,
        connector_type: type[C],
    ) -> None:
        self._description = description
        self._connector_type: type[C] = connector_type

    def main(
        self,
        data_dir: Annotated[Path, Arguments.DATA_DIR],
        erase: Annotated[bool, ToolEnvWrapperOpts.ERASE] = False,
        debug: Annotated[bool, root_logging.OPT_DEBUG] = False,
    ) -> None:
        """Generate environnment wrapper script."""
        root_logging.init_logger(
            _LOGGER,
            (
                f"Generating an environnment wrapper script"
                f" for tool {self._description.name()}"
                f" for topic {self._description.topic().name()}"
            ),
            debug,
        )
        data_exp_manager = exp_fs.DataManager(
            data_dir.resolve(),
            self._description,
            "fake_exp",
        )
        core_command_sh_path = bash.WithOptions.core_command_sh_path(
            self._connector_type.parent_dir_where_defined(),
        )
        env_wrapper_sh_path = data_exp_manager.tool_env_script_sh()
        if env_wrapper_sh_path.exists() and not erase:
            _LOGGER.critical(
                "The environnment wrapper script %s already exists",
                env_wrapper_sh_path,
            )
            raise typer.Exit(1)

        if not data_exp_manager.tool_dir().exists():
            _LOGGER.info(
                "Create non-existing tool directory %s",
                data_exp_manager.tool_dir(),
            )
            data_exp_manager.tool_dir().mkdir(parents=True)

        to_do_lines: list[str] = []
        with core_command_sh_path.open() as f_in:
            in_block_comment = True
            iter_lines = iter(f_in)
            while in_block_comment:
                line = next(iter_lines, None)
                if line is None or not line.startswith("#"):
                    in_block_comment = False
                else:
                    to_do_lines.append(line.rstrip())

        with env_wrapper_sh_path.open("w") as f_out:
            f_out.write("# Tips from the tool core commands:\n")
            f_out.write("\n".join(to_do_lines))
            if to_do_lines:
                f_out.write("\n")
            f_out.write("\n")
            f_out.write(tool_env.ScriptWrapper.BEGIN_ENV_MAGIC_COMMENT + " ===\n")
            f_out.write("\n")
            f_out.write("# Commands to initialize the environment\n")
            f_out.write("\n")
            f_out.write(tool_env.ScriptWrapper.MID_ENV_MAGIC_COMMENT + " ---\n")
            f_out.write("\n")
            f_out.write("# Commands to close the environment\n")
            f_out.write("\n")
            f_out.write(tool_env.ScriptWrapper.END_ENV_MAGIC_COMMENT + " ===\n")

        _LOGGER.info(
            "Tool environnment wrapper draft script written to %s",
            env_wrapper_sh_path,
        )
        raise typer.Exit(0)

    def help(self) -> str:
        """Get help string."""
        return (
            "Generate a draft environnment wrapper script"
            f" for tool {self._description.name()}"
            f" for topic {self._description.topic().name()}"
        )


class ReportOpts:
    """Report command options."""

    YAML_FILE = typer.Option(
        "--yaml",
        "-o",
        help="YAML output file",
    )


class Report:
    """Report command."""

    NAME = "report"

    def __init__(self, description: tool_desc.Description) -> None:
        self._description = description

    def main(
        self,
        exp_name: Annotated[str, Arguments.EXP_NAME],
        data_dir: Annotated[Path, Arguments.DATA_DIR],
        yaml_file: Annotated[Path | None, ReportOpts.YAML_FILE] = None,
        debug: Annotated[bool, root_logging.OPT_DEBUG] = False,
    ) -> None:
        """Generate report."""
        root_logging.init_logger(
            _LOGGER,
            (
                f"Generating a report"
                f" for tool {self._description.name()}"
                f" for topic {self._description.topic().name()}"
            ),
            debug,
        )
        data_exp_manager = exp_fs.DataManager(
            data_dir.resolve(),
            self._description,
            exp_name,
        )
        if not data_exp_manager.exp_dir().exists():
            _LOGGER.critical(
                "There is no experiment nammed `%s` for tool `%s` and topic `%s`",
                data_exp_manager.experiment_name(),
                self._description.name(),
                self._description.topic().name(),
            )
            raise typer.Exit(1)

        report = exp_report.Report.from_data_exp_fs_manager(data_exp_manager)

        _LOGGER.info("Report:\n%s", exp_report.report_to_string(report))
        if yaml_file is not None:
            _LOGGER.info("Writing report to `%s`", yaml_file)
            report.to_yaml(yaml_file)
        raise typer.Exit(0)

    def help(self) -> str:
        """Get help string."""
        return (
            "Generate a report"
            f" for tool {self._description.name()}"
            f" for topic {self._description.topic().name()}"
        )

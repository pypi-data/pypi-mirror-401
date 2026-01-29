"""Abstract tools results items module."""

from typing import final

import slurmbench.experiment.file_system as exp_fs


class Result:
    """A direct result of a tool or a formatted result."""

    @final
    def __init__(self, exp_fs_manager: exp_fs.ManagerBase) -> None:
        """Initialize."""
        self._exp_fs_manager = exp_fs_manager

    @final
    def exp_fs_manager(self) -> exp_fs.ManagerBase:
        """Get file system manager."""
        return self._exp_fs_manager

    # DOCU suggest to implement pair of methods for sample and sh var
    # e.g. For a FASTA GZ result
    # * fasta_gz(sample: smp.RowNumbered)
    # * fasta_gz_sh_var() for SAMPLE_UID sh variable
    #   * use self.exp_fs_manager().sample_sh_var_dir()

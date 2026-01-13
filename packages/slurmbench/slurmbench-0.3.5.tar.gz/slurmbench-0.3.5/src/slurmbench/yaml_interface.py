"""YAML interface module."""

from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

import yaml

try:
    Dumper: type[yaml.Dumper | yaml.CDumper]
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper


if TYPE_CHECKING:
    from pathlib import Path


@runtime_checkable
class YAMLInterface[T, Err](Protocol):
    """YAML interface."""

    @classmethod
    def from_yaml(cls, yaml_filepath: Path) -> Self | Err:
        """Get object from YAML file."""
        with yaml_filepath.open("r") as file:
            obj_dict = yaml.safe_load(file)
        return cls.from_yaml_load(obj_dict)

    @classmethod
    @abstractmethod
    def from_yaml_load(cls, pyyaml_obj: T) -> Self | Err:
        """Convert pyyaml object to self."""
        raise NotImplementedError

    @abstractmethod
    def to_yaml_dump(self) -> T:
        """Convert to dict."""
        raise NotImplementedError

    def to_yaml(self, yaml_filepath: Path) -> Path:
        """Write to yaml."""
        with yaml_filepath.open("w") as file:
            yaml.dump(self.to_yaml_dump(), file, Dumper=Dumper, sort_keys=False)
        return yaml_filepath

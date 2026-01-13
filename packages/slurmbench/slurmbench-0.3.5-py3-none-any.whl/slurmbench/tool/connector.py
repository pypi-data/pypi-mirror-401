"""Tool connector module."""

from __future__ import annotations

import inspect
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Protocol,
    Self,
    assert_never,
    final,
    runtime_checkable,
)

import yaml

import slurmbench.experiment.file_system as exp_fs
import slurmbench.topic.results as topic_res
import slurmbench.topic.visitor as topic_visitor
from slurmbench.yaml_interface import YAMLInterface

from . import bash, results

try:
    Dumper: type[yaml.Dumper | yaml.CDumper]
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator


_LOGGER = logging.getLogger(__name__)


Index = int
Key = str

NodeRef = Index | Key
type AnyNodeRef = Any


class _NodeParsingError(Exception):
    """Parsing error for node."""


class Error[E: _NodeParsingError]:
    """Error."""

    def __init__(self, error: E) -> None:
        self._error = error

    def error(self) -> E:
        """Get error."""
        return self._error


class _Node[Y, Err: _NodeParsingError](YAMLInterface[Y, Error[Err]], ABC):
    """Argument node."""

    @classmethod
    @abstractmethod
    def to_example_yaml_dump(cls) -> Y:
        """Convert to yaml default."""
        raise NotImplementedError


type AnyNode = AnyArg | AnyNodeContainer


class ArgParsingError(_NodeParsingError):
    """Parsing error for leaf argument."""

    @abstractmethod
    def msg(self) -> str:
        """Return error message."""
        raise NotImplementedError


class Arg[Y, Err: ArgParsingError](_Node[Y, Err]):
    """Argument leaf."""


type AnyArg = Arg[Any, ArgParsingError]


@final
class InvalidToolNameError(ArgParsingError):
    """Invalid tool name error."""

    def __init__(
        self,
        invalid_tool_name: str,
        expected_tool_names: Iterable[str],
    ) -> None:
        self._invalid_tool_name = invalid_tool_name
        self._expected_tool_names: tuple[str, ...] = tuple(expected_tool_names)

    def invalid_tool_name(self) -> str:
        """Get invalid tool name."""
        return self._invalid_tool_name

    def expected_tool_names(self) -> tuple[str, ...]:
        """Get expected tool names."""
        return self._expected_tool_names

    def msg(self) -> str:
        """Return error message."""
        return (
            f"Invalid tool name: {self._invalid_tool_name}."
            " Expected one of: " + ", ".join(map(str, self._expected_tool_names)) + "."
        )


class ExpArgLike[
    Y,
    Err: ArgParsingError,
    T: topic_visitor.Tools,
    R: results.Result,
](
    Arg[Y, Err | InvalidToolNameError],
):
    """Experiment argument like."""

    @classmethod
    def tool_example_yaml(cls) -> str:
        """Get the list of valid tools string."""
        # DOCU show how to use for custom class
        tool_choice_str = " | ".join(map(str, cls.valid_tools()))
        return tool_choice_str or "ERROR: no tool implements this argument"

    @classmethod
    def exp_example_yaml(cls) -> str:
        """Get an experiment name example string."""
        # DOCU show how to use for custom class
        return "MY_EXPERIMENT_NAME"

    @classmethod
    @abstractmethod
    def tools_type(cls) -> type[T]:
        """Get tools type."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def result_visitor(cls) -> type[topic_res.Visitor[T, R]]:
        """Get result visitor function."""
        raise NotImplementedError

    @classmethod
    @final
    def valid_tools(cls) -> Iterable[T]:
        """Get valid tools."""
        return (
            tool
            for tool in cls.tools_type()
            if cls.result_visitor().tool_gives_the_result(tool)
        )

    @classmethod
    @final
    def tool_from_str(cls, tool_str: str) -> T | InvalidToolNameError:
        """Return the tool from the config."""
        # DOCU show how to use for custom class
        try:
            tool = cls.tools_type()(tool_str)
        except ValueError:
            return InvalidToolNameError(
                tool_str,
                (str(tool) for tool in cls.valid_tools()),
            )
        match cls.result_visitor().result_builder_from_tool(tool):
            case topic_res.Error():
                return InvalidToolNameError(
                    tool_str,
                    (str(tool) for tool in cls.valid_tools()),
                )
        return tool

    def __init__(self, tool: T, exp_name: str) -> None:
        """Initialize."""
        self._tool = tool
        self._exp_name = exp_name

    @final
    def tool(self) -> T:
        """Get tool."""
        return self._tool

    @final
    def experiment_name(self) -> str:
        """Get experiment name."""
        return self._exp_name

    @final
    def input_data_result(self, data_dir: Path) -> R:
        """Get input data result builder."""
        return self.result_visitor().result_builder()(self.data_fs_manager(data_dir))

    @final
    def output_work_result(self, work_dir: Path) -> R:
        """Get output work result builder."""
        return self.result_visitor().result_builder()(self.work_fs_manager(work_dir))

    @final
    def data_fs_manager(self, data_dir: Path) -> exp_fs.DataManager:
        """Get data file system manager."""
        return exp_fs.DataManager(data_dir, self._tool.to_description(), self._exp_name)

    @final
    def work_fs_manager(self, work_dir: Path) -> exp_fs.WorkManager:
        """Get work file system manager."""
        return exp_fs.WorkManager(work_dir, self._tool.to_description(), self._exp_name)


type AnyExpArgLike = ExpArgLike[
    Any,
    ArgParsingError,
    topic_visitor.Tools,
    results.Result,
]


class ExpArg[T: topic_visitor.Tools, R: results.Result](
    ExpArgLike[list[str], InvalidToolNameError, T, R],
):
    """Experiment argument."""

    # DOCU for Subclassing, use only subclass (because super can be abstract)

    @classmethod
    @final
    def to_example_yaml_dump(cls) -> list[str]:
        """Give a default YAML object."""
        return [cls.tool_example_yaml(), cls.exp_example_yaml()]

    @classmethod
    @final
    def from_yaml_load(
        cls,
        pyyaml_obj: list[str],
    ) -> Self | Error[InvalidToolNameError]:
        """Convert dict to object."""
        # DOCU User must change this if ExpArg subclassing
        match tool_or_err := cls.tool_from_str(pyyaml_obj[0]):
            case InvalidToolNameError():
                return Error(tool_or_err)
        return cls(tool_or_err, pyyaml_obj[1])

    @final
    def to_yaml_dump(self) -> list[str]:
        """Convert to yaml dump."""
        return [str(self._tool), self._exp_name]


type AnyExpArg = ExpArg[topic_visitor.Tools, results.Result]


@runtime_checkable
class ShLinesBuilder[Sh: bash.Node](Protocol):
    """Shell lines builder."""

    @classmethod
    def sh_lines_builder_type(cls) -> type[Sh]:
        """Get shell lines builder type."""

    def sh_lines_builder(self, exp_fs_managers: exp_fs.Managers) -> Sh:
        """Get shell lines builder."""


class ShExpArgLike[
    Y,
    Err: ArgParsingError,
    T: topic_visitor.Tools,
    R: results.Result,
    Sh: bash.AnyExpArgLike,
](
    ExpArgLike[Y, Err, T, R],
    ShLinesBuilder[Sh],
):
    """Experiment argument like with a bash lines builder."""


class ShExpArg[
    T: topic_visitor.Tools,
    R: results.Result,
    Sh: bash.AnyExpArg,
](
    ExpArg[T, R],
    ShLinesBuilder[Sh],
):
    """Experiment argument with a bash lines builder."""

    def sh_lines_builder(self, exp_fs_managers: exp_fs.Managers) -> Sh:
        """Convert input to shell lines builder."""
        return self.sh_lines_builder_type()(
            self.input_data_result(exp_fs_managers.data().root_dir()),
            exp_fs_managers.work(),
        )


class _NodeContainerParsingError[
    Ref: (Index, Key),
    ItemErr: _NodeParsingError,  # HACK cannot subtype tuple contrained generic types
    # ( noqa: ERA001
    #     ArgParsingError,
    #     "_AnyNodeContainerParsingError",
    # ),
](_NodeParsingError):
    """Node container parsing error."""

    def __init__(self, node_ref: Ref, child_error: ItemErr) -> None:
        self._node_ref: Ref = node_ref
        self._child_error: ItemErr = child_error

    def node_ref(self) -> Ref:
        """Get node ref."""
        return self._node_ref

    def child(self) -> ItemErr:
        """Get child error."""
        return self._child_error


type _AnyNodeContainerParsingError = _NodeContainerParsingError[
    AnyNodeRef,
    ArgParsingError | _AnyNodeContainerParsingError,
]

type _AnyArgContainerParsingError = _NodeContainerParsingError[
    AnyNodeRef,
    ArgParsingError,
]

type _AnyReContainerParsingError = _NodeContainerParsingError[
    AnyNodeRef,
    _AnyNodeContainerParsingError,
]


type AnyNodeParsingError = ArgParsingError | _AnyNodeContainerParsingError


class _NodeContainer[
    Ref: (Index, Key),
    ItemNode: AnyNode,
    Y: (dict[Key, Any], list[Any]),
    E: _NodeParsingError,
](_Node[Y, E]):
    """Node container."""

    @abstractmethod
    def children(self) -> Iterable[tuple[Ref, ItemNode]]:
        """Get children nodes."""
        raise NotImplementedError


type AnyNodeContainer = _NodeContainer[
    AnyNodeRef,
    AnyArg | AnyNodeContainer,
    Any,
    ArgParsingError | _AnyNodeContainerParsingError,
]


class _FixNodeTypeContainer[
    Ref: (Index, Key),
    ItemNode: AnyNode,  # HACK use of large generic
    Y: (dict[Key, Any], list[Any]),
    E: _AnyNodeContainerParsingError,
](
    _NodeContainer[Ref, ItemNode, Y, E],
):
    """Node container."""

    @classmethod
    @abstractmethod
    def item_type(cls) -> type[ItemNode]:
        """Get item type."""
        raise NotImplementedError


class FixArgTypeContainer[
    Ref: (Index, Key),
    ItemNode: AnyArg,
    Y: (dict[Key, Any], list[Any]),
    E: _AnyArgContainerParsingError,
](
    _FixNodeTypeContainer[Ref, ItemNode, Y, E],
):
    """Fix argument container."""


class FixRecTypeContainer[
    Ref: (Index, Key),
    ItemNode: AnyNodeContainer,
    Y: (dict[Key, Any], list[Any]),
    E: _AnyReContainerParsingError,
](
    _FixNodeTypeContainer[Ref, ItemNode, Y, E],
):
    """Fix recursive container."""


class NodeListParsingError[
    ItemErr: _NodeParsingError,
](
    _NodeContainerParsingError[Index, ItemErr],
):
    """Node list parsing error."""


type AnyNodeListParsingError = NodeListParsingError[_NodeParsingError]


class _NodeList[
    ItemNode: AnyNode,
    ItemErr: AnyNodeParsingError,
](
    _FixNodeTypeContainer[Index, ItemNode, list[Any], NodeListParsingError[ItemErr]],
):
    """Node list."""

    @classmethod
    @final
    def from_yaml_load(
        cls,
        pyyaml_obj: list[Any],
    ) -> Self | Error[NodeListParsingError[ItemErr]]:
        """Create node list from YAML list."""
        items: list[ItemNode] = []
        for i, yaml_item in enumerate(pyyaml_obj):
            item_or_err = cls.item_type().from_yaml_load(yaml_item)
            match item_or_err:
                case Error():
                    # HACK https://github.com/python/mypy/issues/14813
                    return Error(NodeListParsingError(i, item_or_err.error()))  # type: ignore[arg-type]
            items.append(item_or_err)  # type: ignore[arg-type]
        return cls(items)

    @classmethod
    def to_example_yaml_dump(cls) -> list[Any]:
        """Give a default YAML object."""
        example_item = cls.item_type().to_example_yaml_dump()
        return [example_item, example_item]

    def __init__(self, items: Iterable[ItemNode]) -> None:
        self._items: list[ItemNode] = list(items)

    @final
    def children(self) -> Iterable[tuple[Index, ItemNode]]:
        """Get children nodes."""
        yield from enumerate(self._items)

    @final
    def to_yaml_dump(self) -> list[Any]:
        """Convert to yaml dump."""
        return [item.to_yaml_dump() for item in self._items]


class ArgList[
    ArgItem: AnyArg,
    ArgErr: ArgParsingError,
](
    _NodeList[ArgItem, ArgErr],
):
    """Argument list."""


type AnyArgList = ArgList[AnyArg, ArgParsingError]


class ReList[
    RecItem: AnyNodeContainer,
    RecErr: _AnyNodeContainerParsingError,
](
    _NodeList[RecItem, RecErr],
):
    """Recursive list."""


type AnyReList = ReList[AnyNodeContainer, _AnyNodeContainerParsingError]


class NodeMappingParsingError[
    ItemErr: _NodeParsingError,
](
    _NodeContainerParsingError[Key, ItemErr],
):
    """Node mapping parsing error."""


type AnyNodeMappingParsingError = NodeMappingParsingError[
    ArgParsingError | _AnyNodeContainerParsingError
]


class _NodeMapping[
    ItemNode: AnyNode,
    ItemErr: AnyNodeParsingError,
](
    _FixNodeTypeContainer[
        Key,
        ItemNode,
        dict[str, Any],
        NodeMappingParsingError[ItemErr],
    ],
):
    """Node list."""

    @classmethod
    @abstractmethod
    def item_type(cls) -> type[ItemNode]:
        """Get item type."""
        raise NotImplementedError

    @classmethod
    @final
    def from_yaml_load(
        cls,
        pyyaml_obj: dict[str, Any],
    ) -> Self | Error[NodeMappingParsingError[ItemErr]]:
        """Create node list from YAML list."""
        key_items: list[tuple[str, ItemNode]] = []
        for key, yaml_item in pyyaml_obj.items():
            item_or_err = cls.item_type().from_yaml_load(yaml_item)
            match item_or_err:
                case Error():
                    # HACK https://github.com/python/mypy/issues/14813
                    return Error(NodeMappingParsingError(key, item_or_err.error()))  # type: ignore[arg-type]
            key_items.append((key, item_or_err))  # type: ignore[arg-type]
        return cls(key_items)

    @classmethod
    def to_example_yaml_dump(cls) -> dict[str, Any]:
        """Give a default YAML object."""
        example_item = cls.item_type().to_example_yaml_dump()
        return {"key": example_item, "key2": example_item}

    def __init__(self, key_items: Iterable[tuple[Key, ItemNode]]) -> None:
        self._key_items: dict[Key, ItemNode] = dict(key_items)

    @final
    def children(self) -> Iterable[tuple[Key, ItemNode]]:
        """Get children nodes."""
        yield from self._key_items.items()

    @final
    def to_yaml_dump(self) -> dict[str, Any]:
        """Convert to yaml dump."""
        return {key: item.to_yaml_dump() for key, item in self._key_items.items()}


class ArgMapping[
    ArgItem: AnyArg,
    ArgErr: ArgParsingError,
](
    _NodeMapping[ArgItem, ArgErr],
):
    """Argument mapping."""


type AnyArgMapping = ArgMapping[AnyArg, ArgParsingError]


class ReMapping[
    RecItem: AnyNodeContainer,
    RecErr: _AnyNodeContainerParsingError,
](
    _NodeMapping[RecItem, RecErr],
):
    """Recursive mapping."""


type AnyReMapping = ReMapping[AnyNodeContainer, _AnyNodeContainerParsingError]


@final
class MissingArgumentNameError(ArgParsingError):
    """Missing argument name error."""

    def __init__(self, missing_arg_name: str, required_names: Iterable[str]) -> None:
        self._missing_arg_name = missing_arg_name
        self._required_names: tuple[str, ...] = tuple(required_names)

    def missing_arg_name(self) -> str:
        """Get missing argument name."""
        return self._missing_arg_name

    def required_names(self) -> tuple[str, ...]:
        """Get list or required names."""
        return self._required_names

    def msg(self) -> str:
        """Return error message."""
        return (
            f"Missing argument name: {self._missing_arg_name}."
            " Required names: " + ", ".join(map(str, self._required_names)) + "."
        )


@final
class ExtraArgumentNameError(ArgParsingError):
    """Extra argument name error."""

    def __init__(
        self,
        extra_arg_names: Iterable[str],
        expected_names: Iterable[str],
    ) -> None:
        self._extra_arg_names: tuple[str, ...] = tuple(extra_arg_names)
        self._expected_names: tuple[str, ...] = tuple(expected_names)

    def extra_arg_names(self) -> tuple[str, ...]:
        """Get extra argument name."""
        return self._extra_arg_names

    def expected_names(self) -> tuple[str, ...]:
        """Get names type."""
        return self._expected_names

    def msg(self) -> str:
        """Return error message."""
        return (
            "Extra argument names: "
            + ", ".join(map(str, self._extra_arg_names))
            + ". Expected names: "
            + ", ".join(map(str, self._expected_names))
            + "."
        )


type NodeFixMappingParsingError = (
    AnyNodeMappingParsingError | MissingArgumentNameError | ExtraArgumentNameError
)


class NodeFixMapping(
    _NodeContainer[
        Key,
        AnyArg | AnyNodeContainer,
        dict[Key, Any],
        NodeFixMappingParsingError,
    ],
):
    """Node with fixed keys."""

    @classmethod
    @abstractmethod
    def node_name_types(cls) -> dict[str, type[AnyArg | AnyNodeContainer]]:
        """Get node types associated with their name."""
        raise NotImplementedError

    @classmethod
    def from_yaml_load(
        cls,
        pyyaml_obj: dict[str, Any],
    ) -> Self | Error[NodeFixMappingParsingError]:
        """Convert dict to object."""
        name_to_arg: dict[str, AnyArg | AnyNodeContainer] = {}
        for name, node_type in cls.node_name_types().items():
            if name not in pyyaml_obj:
                return Error(
                    MissingArgumentNameError(
                        name,
                        cls.node_name_types().keys(),
                    ),
                )
            yaml_node = pyyaml_obj[name]

            match arg_or_err := node_type.from_yaml_load(yaml_node):
                case Error():
                    match e := arg_or_err.error():
                        case ArgParsingError():
                            return Error(NodeMappingParsingError(name, e))
                        case _NodeContainerParsingError():
                            return Error(NodeMappingParsingError(name, e))
                case arg:
                    name_to_arg[name] = arg

        if extra_arg := set(pyyaml_obj) - set(name_to_arg):
            return Error(ExtraArgumentNameError(extra_arg, set(name_to_arg)))

        return cls(name_to_arg)

    @classmethod
    @final
    def to_example_yaml_dump(cls) -> dict[str, Any]:
        """Give a default YAML object."""
        return {
            name: node_type.to_example_yaml_dump()
            for name, node_type in cls.node_name_types().items()
        }

    def __init__(self, arguments: dict[str, AnyArg | AnyNodeContainer]) -> None:
        self.__arguments = arguments

    def children(self) -> Iterable[tuple[Key, AnyArg | AnyNodeContainer]]:
        """Get children nodes."""
        yield from self.__arguments.items()

    def to_yaml_dump(self) -> dict[str, Any]:
        """Convert to yaml dump."""
        return {name: arg.to_yaml_dump() for name, arg in self.__arguments.items()}


class PathToExpArg:
    """ExpArg with path in arguments."""

    # FIXME logic will change with argument composition

    def __init__(self, exp_arg: AnyExpArgLike, path: tuple[NodeRef, ...]) -> None:
        self._exp_arg = exp_arg
        self._path = path

    def exp_arg(self) -> AnyExpArgLike:
        """Get exp arg."""
        return self._exp_arg

    def path(self) -> tuple[NodeRef, ...]:
        """Get path of node references."""
        return self._path


class ExpArgPathWithDataFSManager:
    """Exp arg path with data file system manager."""

    def __init__(
        self,
        path_to_exp_arg: PathToExpArg,
        data_dir: Path,
    ) -> None:
        self._path_to_exp_arg = path_to_exp_arg
        self._data_fs_manager = self._path_to_exp_arg.exp_arg().data_fs_manager(
            data_dir,
        )

    def exp_arg(self) -> AnyExpArgLike:
        """Get exp arg."""
        return self._path_to_exp_arg.exp_arg()

    def exp_arg_path(self) -> tuple[NodeRef, ...]:
        """Get exp arg path."""
        return self._path_to_exp_arg.path()

    def data_fs_manager(self) -> exp_fs.DataManager:
        """Get data file system manager."""
        return self._data_fs_manager


class Arguments(NodeFixMapping):
    """Tool arguments configuration."""

    @final
    def sh_lines_builders(
        self,
        exp_fs_managers: exp_fs.Managers,
    ) -> Iterator[bash.Node]:
        """Convert to commands."""

        def _leaf_msg(node_ref_path: list[NodeRef]) -> str:
            """Get leaf message."""

            def _ref_str(ref: NodeRef) -> str:
                match ref:
                    case Key():
                        return f"at key {ref}"
                    case Index():
                        return f"at index {ref}"

            return "Argument leaf has no bash lines builder, " + ", ".join(
                _ref_str(ref) for ref in node_ref_path
            )

        node_lifo: list[tuple[int, tuple[NodeRef, AnyArg | AnyNodeContainer]]] = [
            (0, x) for x in self.children()
        ]
        node_ref_path: list[NodeRef] = []
        while node_lifo:
            ref_depth, (node_ref, node) = node_lifo.pop()
            if ref_depth < len(node_ref_path):
                node_ref_path[ref_depth] = node_ref
            else:
                node_ref_path.append(node_ref)

            if isinstance(node, ShLinesBuilder):
                yield node.sh_lines_builder(exp_fs_managers)  # ty:ignore[invalid-argument-type]
                node_ref_path.pop()
            else:
                match node:
                    case Arg():
                        _LOGGER.warning("%s", _leaf_msg(node_ref_path[: ref_depth + 1]))
                        node_ref_path.pop()
                    case _NodeContainer():
                        node_lifo.extend((ref_depth + 1, x) for x in node.children())
                    case _:
                        assert_never(node)

    @final
    def exp_arg_likes(self) -> Iterator[PathToExpArg]:
        """Get experiment argument like nodes."""
        node_lifo: list[tuple[int, tuple[NodeRef, AnyArg | AnyNodeContainer]]] = [
            (0, x) for x in self.children()
        ]
        node_ref_path: list[NodeRef] = []
        while node_lifo:
            ref_depth, (node_ref, node) = node_lifo.pop()
            if ref_depth < len(node_ref_path):
                node_ref_path[ref_depth] = node_ref
            else:
                node_ref_path.append(node_ref)
            if isinstance(node, ExpArgLike):
                yield PathToExpArg(node, tuple(node_ref_path[: ref_depth + 1]))  # ty:ignore[invalid-argument-type]
                node_ref_path.pop()
            else:
                match node:
                    case Arg():
                        node_ref_path.pop()
                    case _NodeContainer():
                        node_lifo.extend((ref_depth + 1, x) for x in node.children())
                    case _:
                        assert_never(node)


type AnyArguments = Arguments


@final
class StringOpts(YAMLInterface[list[str], "StringOpts"]):
    """String options.

    When the options are regular short/long options.
    """

    @classmethod
    def from_yaml_load(cls, pyyaml_obj: list[str]) -> Self:
        """Convert dict to object."""
        return cls(pyyaml_obj)

    @classmethod
    def to_example_yaml_dump(cls) -> list[str]:
        """Give a default YAML object."""
        return ["--long-option=value1", "--flag"]

    def __init__(self, options: Iterable[str]) -> None:
        self.__options = list(options)

    def __bool__(self) -> bool:
        """Check if options are not empty."""
        return len(self.__options) > 0

    def __len__(self) -> int:
        """Get options length."""
        return len(self.__options)

    def __iter__(self) -> Iterator[str]:
        """Iterate options."""
        return iter(self.__options)

    def sh_lines_builder(self) -> bash.Options:
        """Get shell lines builder type."""
        return bash.Options(self)

    def to_yaml_dump(self) -> list[str]:
        """Convert to dict."""
        return self.__options


class WithOptions[E](YAMLInterface[dict[str, Any], E], ABC):
    """Tool config with options."""

    KEY_OPTIONS = "options"

    @classmethod
    @final
    def _get_options_from_yaml_load(
        cls,
        yaml_obj: dict[str, Any],
    ) -> StringOpts:
        return StringOpts.from_yaml_load(yaml_obj.get(cls.KEY_OPTIONS, []))

    @classmethod
    def to_example_yaml(cls, yaml_filepath: Path) -> Path:
        """Write example YAML configuration file."""
        with yaml_filepath.open("w") as file:
            yaml.dump(cls.to_example_yaml_dump(), file, Dumper=Dumper, sort_keys=False)
        return yaml_filepath

    @classmethod
    @abstractmethod
    def to_example_yaml_dump(cls) -> dict[str, Any]:
        """Give a default YAML object."""
        raise NotImplementedError

    def __init__(self, options: StringOpts) -> None:
        """Initialize."""
        self._options = options

    def options(self) -> StringOpts:
        """Get options."""
        return self._options

    @abstractmethod
    def sh_commands(
        self,
        exp_fs_managers: exp_fs.Managers,
    ) -> bash.WithOptions | None:
        """Get sh commands."""
        raise NotImplementedError

    def is_same(self, other: AnyWithOptions) -> bool:
        """Check if configs are the same."""
        return self.to_yaml_dump() == other.to_yaml_dump()

    @classmethod
    def parent_dir_where_defined(cls) -> Path:
        """Get the parent directory of the module defining the connector.

        Usefull to retrieve the tool template bash script.
        """
        cls_mod = inspect.getmodule(cls)
        match cls_mod:
            case None:
                _LOGGER.critical("No module for %s", cls)
                raise ValueError
        if cls_mod.__file__ is None:
            _LOGGER.critical("No file for %s", cls)
            raise ValueError
        return Path(cls_mod.__file__).parent

    def _options_to_yaml_dump(self) -> dict[str, list[str]]:
        if not self._options:
            return {}
        return {self.KEY_OPTIONS: self._options.to_yaml_dump()}


class OnlyOptions(WithOptions["OnlyOptions"]):
    """Tool config without arguments."""

    @classmethod
    @final
    def from_yaml_load(cls, pyyaml_obj: dict[str, Any]) -> Self:
        """Convert dict to object."""
        return cls(cls._get_options_from_yaml_load(pyyaml_obj))

    @classmethod
    def bash_lines_builder_type(cls) -> type[bash.OnlyOptions]:
        """Get bash lines builder type."""
        # DOCU user can change bash.OnlyOptions
        return bash.OnlyOptions

    @classmethod
    @final
    def to_example_yaml_dump(cls) -> dict[str, Any]:
        """Give a default YAML object."""
        return {cls.KEY_OPTIONS: StringOpts.to_example_yaml_dump()}

    @final
    def sh_commands(
        self,
        exp_fs_managers: exp_fs.Managers,
    ) -> bash.OnlyOptions:
        """Get sh commands."""
        return self.bash_lines_builder_type()(
            bash.Options(self._options),
            exp_fs_managers,
            self.parent_dir_where_defined(),
        )

    @final
    def to_yaml_dump(self) -> dict[str, Any]:
        """Convert to dict."""
        return self._options_to_yaml_dump()


class WithArguments[Args: Arguments](
    WithOptions[Error[NodeFixMappingParsingError]],
):
    """Tool config with arguments."""

    KEY_ARGUMENTS = "arguments"

    @classmethod
    @abstractmethod
    def arguments_type(cls) -> type[Args]:
        """Get arguments type."""
        raise NotImplementedError

    @classmethod
    def from_yaml_load(
        cls,
        pyyaml_obj: dict[str, Any],
    ) -> Self | Error[NodeFixMappingParsingError]:
        """Convert dict to object."""
        args_or_err = cls.arguments_type().from_yaml_load(
            pyyaml_obj[cls.KEY_ARGUMENTS],
        )
        match args_or_err := cls.arguments_type().from_yaml_load(
            pyyaml_obj[cls.KEY_ARGUMENTS],
        ):
            case Error():
                return args_or_err  # ty:ignore[invalid-return-type]
            case _:
                return cls(args_or_err, cls._get_options_from_yaml_load(pyyaml_obj))

    @classmethod
    @final
    def to_example_yaml_dump(cls) -> dict[str, Any]:
        """Give a default YAML object."""
        return {
            cls.KEY_ARGUMENTS: cls.arguments_type().to_example_yaml_dump(),
            cls.KEY_OPTIONS: StringOpts.to_example_yaml_dump(),
        }

    def __init__(self, arguments: Args, options: StringOpts) -> None:
        """Initialize."""
        super().__init__(options)
        self._arguments = arguments

    def arguments(self) -> Args:
        """Get arguments."""
        return self._arguments

    def sh_commands(
        self,
        exp_fs_managers: exp_fs.Managers,
    ) -> bash.WithArguments | None:
        """Get sh commands or None if there is no argument sh line builder."""
        args_sh_lines_builders = list(
            self._arguments.sh_lines_builders(exp_fs_managers),
        )
        if not args_sh_lines_builders:
            return None
        return bash.WithArguments(
            args_sh_lines_builders,
            self.options().sh_lines_builder(),
            exp_fs_managers,
            self.parent_dir_where_defined(),
        )

    def to_yaml_dump(self) -> dict[str, Any]:
        """Convert to dict."""
        return {
            self.KEY_ARGUMENTS: self._arguments.to_yaml_dump(),
            **self._options_to_yaml_dump(),
        }


type AnyWithArguments = WithArguments[AnyArguments]

type AnyWithOptions = OnlyOptions | AnyWithArguments


def from_exp_fs_data_manager[C: AnyWithOptions](
    connector_type: type[C],
    exp_fs_manager: exp_fs.DataManager,
) -> C:
    """Get connector from data file system manager."""
    match connector_or_err := connector_type.from_yaml(exp_fs_manager.config_yaml()):
        case Error():
            _err_msg = "Cannot instantiate connector from data file system manager"
            raise ValueError(_err_msg)
        case _:
            return connector_or_err  # mypy: ignore[return-value]

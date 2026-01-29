from __future__ import annotations

import logging
import math
import os
import re
from collections.abc import Mapping
from enum import Enum, auto
from typing import Any, Optional, Union

import h5py
import numpy as np
import scipy.io as scio

try:
    from esrf_pathlib import ESRFPath as Path
except ImportError:
    from pathlib import Path
from silx.io import open as silx_open

logger = logging.getLogger(__name__)


class FileType(Enum):
    """Enumeration of supported file types."""

    HDF5 = auto()
    MAT = auto()
    CIF = auto()
    REFLECTION = auto()
    DISTORTION = auto()
    UNKNOWN = auto()


class genericFile:
    """Base class for generic file loading and processing."""

    def __init__(self, data=None):
        r"""Initialize a generic file wrapper.

        Parameters
        ----------
        data
            Underlying data container.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        Raw data is stored on `self.data` and optional raw text on `self.sRaw`.
        """
        self.data = data or {}
        self.sRaw = None

    def get_value(self, key, default=None, indices: Any = None):
        r"""Retrieve a value from the stored data.

        Parameters
        ----------
        key
            Slash-delimited key path or token.
        default
            Value to return when lookup fails.
        indices
            Optional indices or slices applied to array-like targets.

        Returns
        -------
        Any
            Resolved value or `default` on failure.

        Notes
        -----
        Keys can traverse mappings, sequences, numpy arrays, and attributes.
        """
        if key in (None, ""):
            return self.data

        sentinel = object()
        try:
            value: Any = self.data
            for attr in self._split_key(key):
                if isinstance(value, genericFile):
                    value = value.get_value(attr, sentinel)
                    if value is sentinel:
                        raise KeyError(attr)
                    continue

                if isinstance(value, Mapping):
                    value = value[attr]
                    continue

                if isinstance(value, (list, tuple)):
                    index = self._parse_sequence_index(attr)
                    if index is None or index >= len(value):
                        raise KeyError(attr)
                    value = value[index]
                    continue

                if isinstance(value, np.ndarray):
                    index = self._parse_sequence_index(attr)
                    if index is None:
                        raise KeyError(attr)
                    value = value[index]
                    continue

                if hasattr(value, attr):
                    value = getattr(value, attr)
                    continue

                value = value[attr]

            value = self._apply_indices(value, indices)
            return self._coerce_value(value)
        except Exception:
            # logging.warning(f"Failed to get value for key: {key}")
            return default

    @staticmethod
    def _split_key(key: str) -> list[str]:
        r"""Split a key path into tokens.

        Parameters
        ----------
        key
            Slash-delimited key string.

        Returns
        -------
        list[str]
            List of non-empty key tokens.

        Notes
        -----
        Empty tokens are ignored.
        """
        return [token for token in str(key).split("/") if token]

    def _coerce_value(self, value: Any) -> Any:
        r"""Normalize return values into convenient Python types.

        Parameters
        ----------
        value
            Raw value to normalize.

        Returns
        -------
        Any
            Normalized value with arrays coerced and mappings wrapped.

        Notes
        -----
        HDF5 datasets are read into numpy arrays when encountered.
        """
        if isinstance(value, dict):
            return self._wrap_mapping(value)

        if isinstance(value, list) and value and all(isinstance(i, dict) for i in value):
            return [self._wrap_mapping(item) for item in value]

        if isinstance(value, np.ndarray):
            return self._finalize_array(value)

        if isinstance(value, h5py.Dataset):
            return self._finalize_array(value[()])

        if isinstance(value, bytes):
            return value.decode("utf-8")

        if isinstance(value, np.generic):
            return value.item()

        return value

    def _wrap_mapping(self, mapping: Mapping) -> "genericFile":
        r"""Wrap a mapping in the appropriate helper type.

        Parameters
        ----------
        mapping
            Mapping to wrap.

        Returns
        -------
        genericFile
            Wrapper instance, using `FilterMATDataset` when applicable.

        Notes
        -----
        The current instance type determines the wrapper class.
        """
        if isinstance(self, FilterMATDataset):
            return FilterMATDataset(mapping)
        return genericFile(mapping)

    def _apply_indices(self, value: Any, indices: Any) -> Any:
        r"""Apply indices to array-like or dataset values.

        Parameters
        ----------
        value
            Candidate value to index.
        indices
            Index or slice to apply.

        Returns
        -------
        Any
            Indexed value.

        Notes
        -----
        Raises `TypeError` when indices target non-sequence values.
        """
        if indices is None:
            return value

        value = self._dereference_node(value)

        if isinstance(value, h5py.Dataset):
            return value[indices]

        if isinstance(value, np.ndarray):
            return value[indices]

        if isinstance(value, (list, tuple)):
            try:
                return value[indices]
            except TypeError:
                return np.asarray(value)[indices]

        raise TypeError("Indices can only be applied to datasets or sequences.")

    def _decode_if_bytes(self, array: np.ndarray) -> np.ndarray:
        r"""Decode byte strings in a numpy array.

        Parameters
        ----------
        array
            Numpy array that may contain byte strings.

        Returns
        -------
        np.ndarray
            Array with byte strings decoded as UTF-8.

        Notes
        -----
        Elements that are not bytes are returned unchanged.
        """
        return np.vectorize(lambda x: x.decode("utf-8") if isinstance(x, bytes) else x)(
            array
        )

    def _finalize_array(self, array: np.ndarray) -> Any:
        r"""Finalize array-like values into scalars or normalized arrays.

        Parameters
        ----------
        array
            Array or dataset to normalize.

        Returns
        -------
        Any
            Scalar value or normalized numpy array.

        Notes
        -----
        Column/row vectors are flattened and singletons are unwrapped.
        """
        value = array
        if isinstance(value, h5py.Dataset):
            value = value[()]
        if isinstance(value, np.ndarray):
            arr = value
        else:
            arr = np.asarray(value)

        if arr.dtype == np.object_ or getattr(arr.dtype, "kind", "") in {"S", "a"}:
            arr = self._decode_if_bytes(arr)

        if arr.ndim == 2 and arr.shape[1] == 1:
            arr = arr.reshape(arr.shape[0])
        elif arr.ndim == 2 and arr.shape[0] == 1:
            arr = arr.reshape(arr.shape[1])

        if arr.size == 1:
            return np.squeeze(arr).item()

        return arr

    def get_keys(self, key=None) -> list[str]:
        r"""Return available keys for a mapping or group.

        Parameters
        ----------
        key
            Optional key path to resolve before listing keys.

        Returns
        -------
        list[str]
            List of available keys (empty if none are found).

        Notes
        -----
        Non-mapping targets return an empty list.
        """
        target = self if key in (None, "") else self.get_value(key)
        target = self._dereference_node(target)

        if isinstance(target, Mapping):
            return list(target.keys())

        if hasattr(target, "keys"):
            try:
                return list(target.keys())
            except Exception:  # pragma: no cover - defensive guard
                return []

        return []

    def display_struct(self, max_level=None) -> str:
        r"""Return a raw string representation of the data structure.

        Parameters
        ----------
        max_level
            Maximum nesting depth to display (unused here).

        Returns
        -------
        str
            Raw structure string or an empty string.

        Notes
        -----
        This base implementation returns cached raw content when available.
        """
        return self.sRaw if self.sRaw else ""

    def to_dict(self) -> dict[str, Any]:
        r"""Convert the object data to a dictionary.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        dict[str, Any]
            Dictionary of resolved key-value pairs.

        Notes
        -----
        Values are resolved through `get_value`.
        """
        return {key: self.get_value(key) for key in self.get_keys()}

    def _dereference_node(self, node: Any) -> Any:
        r"""Unwrap helper classes to expose underlying data containers.

        Parameters
        ----------
        node
            Candidate node to unwrap.

        Returns
        -------
        Any
            Underlying data container.

        Notes
        -----
        Nested `genericFile` wrappers are unwrapped iteratively.
        """
        while isinstance(node, genericFile):
            node = node.data
        return node

    @staticmethod
    def _parse_sequence_index(token: Union[str, int]) -> Optional[int]:
        r"""Parse a token representing a sequence index.

        Parameters
        ----------
        token
            Index token such as `0` or `[0]`.

        Returns
        -------
        Optional[int]
            Parsed integer index or None when invalid.

        Notes
        -----
        Only non-negative integer tokens are accepted.
        """
        if isinstance(token, int):
            return token
        if not isinstance(token, str):
            return None
        if token.isdigit():
            return int(token)
        if token.startswith("[") and token.endswith("]"):
            inner = token[1:-1]
            if inner.isdigit():
                return int(inner)
        return None

    def _resolve_metadata_target(self, key: str) -> Any:
        r"""Resolve a metadata target without materializing datasets.

        Parameters
        ----------
        key
            Slash-delimited key path.

        Returns
        -------
        Any
            Resolved node or None when not found.

        Notes
        -----
        This traversal prefers lightweight metadata access.
        """
        if key in (None, ""):
            return self._dereference_node(self.data)

        parts = [part for part in key.split("/") if part]
        current: Any = self._dereference_node(self.data)

        for part in parts:
            current = self._dereference_node(current)
            if current is None:
                return None

            if isinstance(current, (h5py.Group, h5py.File)):
                if part in current:
                    current = current[part]
                    continue
                attrs = getattr(current, "attrs", None)
                if attrs is not None and part in attrs:
                    current = attrs[part]
                    continue
                return None

            if isinstance(current, Mapping):
                current = current.get(part)
                continue

            if isinstance(current, (list, tuple)):
                index = self._parse_sequence_index(part)
                if index is None or index >= len(current):
                    return None
                current = current[index]
                continue

            if hasattr(current, "keys"):
                keys = current.keys()
                if part in keys:
                    getter = getattr(current, "get", None)
                    if callable(getter):
                        current = getter(part)
                    else:
                        try:
                            current = current[part]
                        except Exception:
                            return None
                    continue

            if hasattr(current, part):
                current = getattr(current, part)
                continue

            return None

        return self._dereference_node(current)

    def get_size(self, key: str) -> Union[Optional[tuple[int, ...]], Optional[int]]:
        r"""Return size information for a dataset or group.

        Parameters
        ----------
        key
            Key or identifier for the target node.

        Returns
        -------
        Optional[tuple[int, ...] | int]
            Shape tuple, length, member count, or None when unavailable.

        Notes
        -----
        HDF5 groups report children plus attribute count.
        """

        if self.data is None:
            return None

        try:
            target = self._resolve_metadata_target(key)
            target = self._dereference_node(target)

            if target is None:
                return None

            if isinstance(target, h5py.Dataset):
                shape = tuple(target.shape)
                if len(shape) == 1:
                    return shape[0]
                return shape

            if isinstance(target, (h5py.Group, h5py.File)):
                children = len(target.keys()) if hasattr(target, "keys") else 0
                attrs = getattr(target, "attrs", None)
                attr_count = len(attrs) if attrs is not None else 0
                return children + attr_count

            shape_attr = getattr(target, "shape", None)
            if shape_attr is not None and not isinstance(
                target, (h5py.Group, h5py.File)
            ):
                try:
                    shape_iter = tuple(shape_attr)
                except TypeError:
                    shape_iter = (shape_attr,)
                shape = tuple(
                    int(dim) if isinstance(dim, np.integer) else dim
                    for dim in shape_iter
                )
                if len(shape) == 1:
                    return shape[0]
                return shape

            if isinstance(target, Mapping):
                return len(target)

            if isinstance(target, (list, tuple)):
                if not target:
                    return 0
                if all(hasattr(item, "__len__") for item in target):
                    try:
                        first_len = len(target[0])
                        if all(len(item) == first_len for item in target):
                            return (len(target), first_len)
                    except Exception as exc:  # pragma: no cover - defensive guard
                        logger.debug(
                            "Unable to infer consistent lengths for %s sequence: %s",
                            type(target).__name__,
                            exc,
                        )
                return len(target)

            # Handle single values
            if hasattr(target, "__len__") and not isinstance(target, (str, bytes)):
                return len(target)

            return None

        except Exception as e:
            logging.warning(f"Error getting size for key '{key}': {str(e)}")

        return None


class FilterH5Dataset(genericFile):
    """A helper class to manage data within HDF5 structures."""

    def __init__(self, data: Union[h5py.Group, h5py.Dataset], from_mat: bool = None):
        r"""Initialize an HDF5 dataset wrapper.

        Parameters
        ----------
        data
            HDF5 group or dataset to wrap.
        from_mat
            Flag indicating MATLAB v7.3 orientation handling.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        MATLAB v7.3 detection is performed when `from_mat` is not provided.
        """
        self.data = data
        if from_mat is None:
            self._is_matlab_v73 = self._check_matlab_v73()
        else:
            self._is_matlab_v73 = from_mat
        super().__init__(data)

    def _check_matlab_v73(self) -> bool:
        r"""Check whether the dataset belongs to a MATLAB v7.3 file.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        bool
            True when a MATLAB v7.3 signature is detected.

        Notes
        -----
        The check walks up the HDF5 hierarchy to the root group.
        """
        if not hasattr(self.data, "parent"):
            return False

        try:
            # Start with current object
            current = self.data
            visited = set()

            # Traverse up to root group with loop protection
            while hasattr(current, "parent") and current.parent not in visited:
                visited.add(current)
                if isinstance(current, h5py.File):
                    return "MATLAB_version" in current.attrs
                current = current.parent

            return False
        except Exception:
            return False

    def get_value(
        self, key: str, default: Optional[Any] = None, indices: Any = None
    ) -> Any:
        r"""Retrieve a value from an HDF5 structure.

        Parameters
        ----------
        key
            Key path to retrieve.
        default
            Value to return when lookup fails.
        indices
            Optional indices or slices to apply.

        Returns
        -------
        Any
            Resolved value or `default` on failure.

        Notes
        -----
        Group nodes are wrapped as `FilterH5Dataset`.
        """
        if key in (None, ""):
            return self

        try:
            target = self._resolve_metadata_target(key)
            if target is None:
                return default
            target = self._apply_indices(target, indices)
            return self._coerce_hdf5_value(target)
        except Exception:
            # logging.warning(f"Failed to get value for key: {key}")
            return default

    def _coerce_hdf5_value(self, value: Any) -> Any:
        r"""Convert HDF5 nodes into Python objects.

        Parameters
        ----------
        value
            HDF5 node, dataset, or attribute value.

        Returns
        -------
        Any
            Converted Python object.

        Notes
        -----
        Arrays are normalized and MATLAB v7.3 orientation is adjusted.
        """
        if isinstance(value, (h5py.Group, h5py.File)):
            return FilterH5Dataset(value, from_mat=self._is_matlab_v73)

        if isinstance(value, h5py.Dataset):
            data = value[()]
            if self._is_matlab_v73:
                data = self._fix_matlab_orientation(data)
            return self._finalize_numpy_like(data)

        if isinstance(value, np.ndarray):
            data = self._fix_matlab_orientation(value) if self._is_matlab_v73 else value
            return self._finalize_numpy_like(data)

        if isinstance(value, bytes):
            return value.decode("utf-8")

        if isinstance(value, np.generic):
            return value.item()

        return value

    def _finalize_numpy_like(self, data: Any) -> Any:
        r"""Standardize numpy arrays or scalars returned by HDF5.

        Parameters
        ----------
        data
            Numpy array-like data or scalar.

        Returns
        -------
        Any
            Scalar or normalized numpy array.

        Notes
        -----
        Byte arrays are decoded and singleton shapes are squeezed.
        """
        if np.isscalar(data):
            if isinstance(data, (bytes, np.bytes_)):
                return data.decode("utf-8")
            return data.item()

        array = np.asarray(data)

        if array.dtype == np.object_ or getattr(array.dtype, "kind", "") in {"S", "a"}:
            array = self._decode_if_bytes(array)

        if array.ndim == 2 and array.shape[1] == 1:
            array = array.reshape(array.shape[0])
        elif array.ndim == 2 and array.shape[0] == 1:
            array = array.reshape(array.shape[1])

        if array.size == 1:
            return np.squeeze(array).item()

        return array

    def _fix_matlab_orientation(
        self, value: Union[h5py.Dataset, np.ndarray]
    ) -> np.ndarray:
        r"""Convert MATLAB v7.3 arrays to NumPy orientation.

        Parameters
        ----------
        value
            Dataset or array to reorient.

        Returns
        -------
        np.ndarray
            Reoriented array.

        Notes
        -----
        MATLAB uses column-major storage; this method reverses axes.
        """
        arr = value[()] if isinstance(value, h5py.Dataset) else value
        # For higher dimensional arrays, we need to reverse the axes
        if arr.ndim > 1:
            return np.array([list(row) for row in zip(*arr)])
        return arr

    def _decode_if_bytes(
        self, value: Union[np.ndarray, h5py.Dataset]
    ) -> Union[str, np.ndarray]:
        r"""Decode byte strings in numpy arrays or datasets.

        Parameters
        ----------
        value
            Dataset or array that may contain byte strings.

        Returns
        -------
        Union[str, np.ndarray]
            Decoded string or array of decoded strings.

        Notes
        -----
        Scalar datasets return a single decoded string.
        """
        if value.shape == ():
            return value[()].decode("utf-8")
        elif value.size == 1 and isinstance(value[0], bytes):
            return value[0].decode("utf-8")
        return np.array(
            [d.decode("utf-8") if isinstance(d, bytes) else d for d in value]
        )

    def get_keys(self, key=None) -> list[str]:
        r"""Retrieve keys from an HDF5 group or file.

        Parameters
        ----------
        key
            Optional key path to resolve before listing keys.

        Returns
        -------
        list[str]
            Keys for groups and their attributes.

        Notes
        -----
        Attribute keys are included alongside child datasets.
        """
        target = self if key in (None, "") else self.get_value(key)
        target = getattr(target, "data", target)

        if isinstance(target, (h5py.Group, h5py.File)):
            attrs = getattr(target, "attrs", None)
            attr_keys = list(attrs.keys()) if attrs is not None else []
            return list(target.keys()) + attr_keys

        return []

    def __repr__(self) -> str:
        r"""Return a debug representation of the wrapper.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        str
            Representation string.

        Notes
        -----
        Includes the underlying HDF5 object.
        """
        return f"FilterH5Dataset({self.data})"

    def display_struct(self, max_level: int = 3) -> str:
        r"""Display the structure of the dataset up to a maximum depth.

        Parameters
        ----------
        max_level
            Maximum depth level to display.

        Returns
        -------
        str
            Human-readable structure string.

        Notes
        -----
        Output is built by recursively inspecting group members.
        """
        return "\n".join(self._print_recursive(self, max_level=max_level))

    @staticmethod
    def _normalize_description_value(value: Any) -> Optional[Union[str, list[str]]]:
        r"""Normalize description metadata into strings.

        Parameters
        ----------
        value
            Raw attribute or dataset value.

        Returns
        -------
        Optional[Union[str, list[str]]]
            Normalized string or list of strings.

        Notes
        -----
        Byte strings and numpy scalars are decoded to Python types.
        """
        if value is None:
            return None
        if isinstance(value, bytes):
            return value.decode("utf-8")
        if isinstance(value, str):
            return value
        if isinstance(value, np.generic):
            return FilterH5Dataset._normalize_description_value(value.item())
        if isinstance(value, np.ndarray):
            if value.shape == ():
                return FilterH5Dataset._normalize_description_value(value[()])
            flattened = [
                FilterH5Dataset._normalize_description_value(item)
                for item in value.ravel()
            ]
            flattened = [item for item in flattened if item is not None]
            if not flattened:
                return None
            if len(flattened) == 1:
                return flattened[0]
            return flattened
        if isinstance(value, (list, tuple)):
            converted = [
                FilterH5Dataset._normalize_description_value(item) for item in value
            ]
            converted = [item for item in converted if item is not None]
            if not converted:
                return None
            if len(converted) == 1:
                return converted[0]
            return converted
        return str(value)

    def _extract_description(self, target: Any) -> Optional[Union[str, list[str]]]:
        r"""Extract a Description attribute from a resolved node.

        Parameters
        ----------
        target
            Resolved HDF5 node or value.

        Returns
        -------
        Optional[Union[str, list[str]]]
            Description value or None when missing.

        Notes
        -----
        NXentry groups also check common title fields.
        """
        target = self._dereference_node(target)
        if target is None:
            return None

        if isinstance(target, h5py.Dataset):
            attrs = getattr(target, "attrs", None)
            if attrs is not None and "Description" in attrs:
                return self._normalize_description_value(attrs["Description"])
            try:
                value = target[()]
            except Exception:
                return None
            return self._normalize_description_value(value)

        if isinstance(target, (h5py.Group, h5py.File)):
            attrs = getattr(target, "attrs", None)
            if attrs is not None:
                if "Description" in attrs:
                    return self._normalize_description_value(attrs["Description"])

                nx_class = attrs.get("NX_class")
                nx_class_name = self._normalize_description_value(nx_class)
                if (
                    isinstance(nx_class_name, str)
                    and nx_class_name.lower() == "nxentry"
                ):
                    if "title" in attrs:
                        return self._normalize_description_value(attrs["title"])
                    if hasattr(target, "keys") and "title" in target.keys():
                        try:
                            title_node = target.get("title")
                        except Exception:
                            title_node = None
                        if title_node is not None:
                            return self._extract_description(title_node)

            return None

        return self._normalize_description_value(target)

    def get_description(
        self, key: Optional[str] = None, default: Optional[Any] = None
    ) -> Optional[Union[str, list[str]]]:
        r"""Retrieve the `Description` attribute for a node.

        Parameters
        ----------
        key
            Key path to resolve.
        default
            Value to return when no description is found.

        Returns
        -------
        Optional[Union[str, list[str]]]
            Description value or `default` when missing.

        Notes
        -----
        The method also checks `.../Description` when applicable.
        """
        try:
            # Try the provided key directly
            targets = []
            if key in (None, ""):
                targets.append(self.data)
            else:
                targets.append(self._resolve_metadata_target(key))

                parts = [part for part in key.split("/") if part]
                if parts and parts[-1].lower() != "description":
                    description_key = "/".join(parts + ["Description"])
                    targets.append(self._resolve_metadata_target(description_key))

            for candidate in targets:
                description = self._extract_description(candidate)
                if description is not None:
                    return description

            return default
        except Exception as error:
            if logger.isEnabledFor(logging.DEBUG):
                logger.debug(
                    "Failed to retrieve Description for key '%s': %s", key, error
                )
            return default

    def _print_recursive(
        self, group: "FilterH5Dataset", level: int = 0, max_level: int = 3
    ) -> list[str]:
        r"""Recursively format HDF5 keys and values for display.

        Parameters
        ----------
        group
            Group wrapper to traverse.
        level
            Current indentation level.
        max_level
            Maximum depth to traverse.

        Returns
        -------
        list[str]
            Formatted lines describing the group contents.

        Notes
        -----
        Large datasets are represented by their dataset summary string.
        """
        out = []
        if level < max_level:
            indent = "    " * level
            if isinstance(group.data, (h5py.Group, h5py.File)):
                for key in group.get_keys():
                    value = group.data.get(key)
                    if isinstance(value, h5py.Group):
                        out.append(f"{indent}{key}:")
                        out.extend(
                            self._print_recursive(
                                group.get_value(key), level + 1, max_level
                            )
                        )
                    elif isinstance(value, h5py.Dataset):
                        if not all(dim < 5 for dim in value.shape):
                            out.append(f"{indent}{key}: {str(value)}")
                        else:
                            out.append(f"{indent}{key}: {group.get_value(key)}")
                    else:
                        out.append(f"{indent}{key}: {group.get_value(key)}")
        return out


class LoadH5File(FilterH5Dataset):
    """Class to load and display HDF5 file structures."""

    def __init__(self, filepath: str, from_mat: bool = None):
        r"""Initialize an HDF5 file loader.

        Parameters
        ----------
        filepath
            Path to the HDF5 file.
        from_mat
            Flag indicating MATLAB v7.3 orientation handling.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        Files are opened through `silx.io.open` when available.
        """
        self.filepath = Path(filepath)
        if self.filepath.exists():
            try:
                self.data = silx_open(str(self.filepath))
            except Exception as error:
                logging.warning(
                    "File path '%s' could not be opened: %s", filepath, error
                )
                self.data = None
        else:
            logging.warning(f"File path '{filepath}' not found.")
            self.data = None
        super().__init__(self.data, from_mat)


class FilterMATDataset(genericFile):
    """Helper class for structured access to data from MAT files."""

    def __init__(self, data: dict):
        r"""Initialize a MAT dataset wrapper.

        Parameters
        ----------
        data
            Mapping containing MAT data.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The data is stored without additional processing.
        """
        super().__init__(data)

    def __repr__(self) -> str:
        r"""Return a debug representation of the wrapper.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        str
            Representation string with a sample of keys.

        Notes
        -----
        Only a limited number of keys are displayed.
        """
        keys = list(self.__dict__.keys())[:5]  # Show a sample of 5 keys
        return f"FilterMATDataset(keys={keys}, ...)"

    def display_struct(self, max_level: int = 3) -> str:
        r"""Display the structure of the dataset up to a maximum depth.

        Parameters
        ----------
        max_level
            Maximum depth level to display.

        Returns
        -------
        str
            Human-readable structure string.

        Notes
        -----
        Output is built by recursively inspecting nested datasets.
        """
        return "\n".join(self._print_recursive(self, level=0, max_level=max_level))

    def _print_recursive(
        self, dataset: "FilterMATDataset", level: int = 0, max_level: int = 3
    ) -> list[str]:
        r"""Recursively format keys and values for display.

        Parameters
        ----------
        dataset
            Dataset wrapper to traverse.
        level
            Current indentation level.
        max_level
            Maximum depth to traverse.

        Returns
        -------
        list[str]
            Formatted lines describing the dataset contents.

        Notes
        -----
        Arrays are summarized by shape and dtype.
        """
        out = []
        if level < max_level:
            indent = "    " * level
            for key in dataset.get_keys():
                value = dataset.get_value(key)
                if isinstance(value, FilterMATDataset):
                    out.append(f"{indent}{key}:")
                    out.extend(self._print_recursive(value, level + 1, max_level))
                elif isinstance(value, np.ndarray):
                    out.append(
                        f"{indent}{key}: Array with shape {value.shape} of dtype {value.dtype}"
                    )
                else:
                    out.append(f"{indent}{key}: {str(value)[:20]}...")
        return out


class LoadMatFile(FilterMATDataset):
    """Class to load and display MATLAB .mat file structures."""

    def __init__(self, file_path: str, *args):
        r"""Initialize a MATLAB .mat file loader.

        Parameters
        ----------
        file_path
            Path to the .mat file.
        *args
            Unused positional arguments (for compatibility).

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The file is loaded and flattened into nested mappings.
        """
        flattened_data = self._load_and_process(file_path)
        super().__init__(flattened_data)

    def _load_and_process(self, file_path: str) -> Any:
        r"""Load a MAT file and flatten nested structures.

        Parameters
        ----------
        file_path
            Path to the .mat file.

        Returns
        -------
        Any
            Flattened dataset representation.

        Notes
        -----
        The loader uses `scipy.io.loadmat` with squeeze semantics.
        """
        data = scio.loadmat(file_path, struct_as_record=False, squeeze_me=True)
        return self._flatten_nested(data)

    def _flatten_nested(self, item: Any) -> Any:
        r"""Flatten nested MAT structures into Python containers.

        Parameters
        ----------
        item
            Value to flatten.

        Returns
        -------
        Any
            Flattened Python object.

        Notes
        -----
        Byte strings are decoded as UTF-8.
        """
        if isinstance(item, np.ndarray) and item.dtype == object:
            # Process numpy arrays with object dtype recursively
            return [self._flatten_nested(sub_item) for sub_item in item.ravel()]
        elif isinstance(item, dict):
            # Wrap nested dictionaries as FilterMATDataset instances, keep root dict unchanged
            return {key: self._flatten_nested(value) for key, value in item.items()}
        elif hasattr(item, "_fieldnames"):
            # Wrap structures with field names as FilterMATDataset instances
            return {
                field: self._flatten_nested(getattr(item, field))
                for field in item._fieldnames
            }
        elif isinstance(item, list):
            return [self._flatten_nested(sub_item) for sub_item in item]
        elif isinstance(item, bytes):
            # Decode bytes to strings
            return item.decode("utf-8")
        return item

    def display_struct(self, max_level: int = 3) -> str:
        r"""Display the structure of the loaded .mat file data.

        Parameters
        ----------
        max_level
            Maximum depth level to display.

        Returns
        -------
        str
            Human-readable structure string.

        Notes
        -----
        When nested data is wrapped, the wrapper handles the display.
        """
        if isinstance(self.data, FilterMATDataset):
            return self.data.display_struct(max_level=max_level)
        return str(self.data)


class LoadCIFFile(genericFile):
    """Class to load and process CIF (Crystallographic Information Framework) files."""

    def __init__(self, file: Path, *args):
        r"""Initialize a CIF file loader.

        Parameters
        ----------
        file
            Path to the CIF file.
        *args
            Unused positional arguments (for compatibility).

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The file is parsed into a small set of extracted fields.
        """
        super().__init__()
        self.file = Path(file)
        if self.file.suffix != ".cif":
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(f"The file {self.file.name} is not a CIF file.")
        else:
            self._loadFile()

    def _loadFile(self) -> None:
        r"""Load and parse the CIF file content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        Multiple encodings are tried before giving up.
        """
        encodings = ["utf-8", "ISO-8859-1", "windows-1252"]
        for encoding in encodings:
            try:
                self.sRaw = self.file.read_text(encoding=encoding)
                self.data = {
                    "latticepar": self._extract_lattice_params(),
                    "opsym": self._extract_symmetry_ops(),
                    "spacegroup": self._extract_spacegroup(),
                    "hermann_mauguin": self._extract_hm_symbol(),
                    "crystal_system": self._extract_crystal_system(),
                }
                break
            except UnicodeDecodeError:
                logging.info(f"Error decoding with {encoding}, trying next encoding...")
            except Exception as e:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.error(f"Error loading CIF file {self.file.name}: {e}")

    def grep(self, pattern, file_content, group_index=0):
        r"""Search for a regex pattern in the file content.

        Parameters
        ----------
        pattern
            Regular expression pattern.
        file_content
            Raw file content to search.
        group_index
            Match group index to return.

        Returns
        -------
        Optional[str]
            Matched group string or None when not found.

        Notes
        -----
        This uses `re.search` and returns the first match.
        """
        match = re.search(pattern, file_content)
        if match:
            return match.group(group_index)
        return None

    # Function to extract lattice parameters
    def _extract_lattice_params(self):
        r"""Extract lattice parameters from CIF content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        Optional[list[float]]
            Lattice parameters [a, b, c, alpha, beta, gamma] or None.

        Notes
        -----
        Values are returned as floats when available.
        """
        a = self.grep(r"_cell_length_a\s+([\d.]+)", self.sRaw, 1)
        b = self.grep(r"_cell_length_b\s+([\d.]+)", self.sRaw, 1)
        c = self.grep(r"_cell_length_c\s+([\d.]+)", self.sRaw, 1)
        alpha = self.grep(r"_cell_angle_alpha\s+([\d.]+)", self.sRaw, 1)
        beta = self.grep(r"_cell_angle_beta\s+([\d.]+)", self.sRaw, 1)
        gamma = self.grep(r"_cell_angle_gamma\s+([\d.]+)", self.sRaw, 1)

        try:
            latticepar = [
                float(a),
                float(b),
                float(c),
                float(alpha),
                float(beta),
                float(gamma),
            ]
        except TypeError:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error("Error converting lattice parameters to floats")
            return None
        return latticepar

    # Function to extract symmetry operators
    def _extract_symmetry_ops(self):
        r"""Extract symmetry operations from CIF content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        Optional[list[str]]
            List of symmetry operation strings or None.

        Notes
        -----
        Operations are parsed from the first `loop_` block.
        """
        op_start = self.sRaw.find("loop_")
        if op_start != -1:
            symmetry_ops = self.sRaw[op_start:].splitlines()
            ops_cleaned = [op.strip() for op in symmetry_ops if re.match(r".*x.*", op)]
            return ops_cleaned
        return None

    # Function to extract spacegroup number
    def _extract_spacegroup(self):
        r"""Extract the space group number from CIF content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        Optional[int]
            Space group number or None.

        Notes
        -----
        The value is read from `_symmetry_Int_Tables_number`.
        """
        sg = self.grep(r"_symmetry_Int_Tables_number\s+(\d+)", self.sRaw, 1)
        return int(sg) if sg else None

    # Function to extract Hermann-Mauguin symbol
    def _extract_hm_symbol(self):
        r"""Extract Hermann-Mauguin symbol from CIF content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        Optional[str]
            Hermann-Mauguin symbol or None.

        Notes
        -----
        The symbol is normalized to title case.
        """
        hm = self.grep(r"_symmetry_space_group_name_H-M\s+(.+)", self.sRaw, 1)
        if hm:
            hm = hm.strip().replace("'", "")
            return hm[0].upper() + hm[1:].lower()
        return None

    # Function to extract crystal system
    def _extract_crystal_system(self):
        r"""Extract the crystal system from CIF content.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        Optional[str]
            Crystal system name or None.

        Notes
        -----
        The value is read from `_symmetry_cell_setting`.
        """
        cellname = self.grep(r"_symmetry_cell_setting\s+(\w+)", self.sRaw, 1)
        return cellname.strip() if cellname else None


class LoadReflexionFile(genericFile):
    """Class to load and process CIF (Crystallographic Information Framework) files."""

    def __init__(self, file: Path, *args):
        r"""Initialize a reflection file loader.

        Parameters
        ----------
        file
            Path to the reflection file.
        *args
            Unused positional arguments (for compatibility).

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        Supported extensions are `.csv` and `.dat`.
        """
        super().__init__()
        self.file = Path(file)
        if self.file.suffix not in [".csv", ".dat"]:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(f"The file {self.file.name} is not a reflexion file.")
        else:
            self._loadFile()

    def _loadFile(self) -> None:
        r"""Load and parse the reflection file.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        CSV files use ';' delimiters; DAT files use whitespace.
        """
        if self.file.suffix == ".csv":
            delim = ";"
        elif self.file.suffix == ".dat" and self.file.name.lower() != "spacegroups.dat":
            delim = "space"

        logging.info(f"Opening file {self.file.name}...")
        encodings = ["utf-8", "ISO-8859-1", "windows-1252"]  # Try multiple encodings
        for encoding in encodings:
            try:
                with self.file.open("r", encoding=encoding) as fid:
                    if delim == "space":
                        lines = fid.readlines()
                        self.sRaw = [line.split() for line in lines]
                    else:
                        self.sRaw = [line.strip().split(delim) for line in fid]

                # Extract header and process the data
                headers = self.sRaw[0]

                # Clean headers and assign to reflection dictionary
                for i, header in enumerate(headers):
                    title = header.strip().lower()
                    title = re.sub(r"\.", "", title)
                    title = re.sub(r"[^a-zA-Z]", "", title)
                    title = re.sub(r"theta", "twotheta", title)
                    if len(title) == 1:
                        title = re.sub(r"^m", "mult", title)
                        title = re.sub(r"^f", "formfactor", title)
                    title = title.replace("dspc", "dspacing")

                    if title != "no":
                        self.data[title] = [row[i] for row in self.sRaw[1:]]

                # Convert h, k, l columns to 'hkl'
                self.data["hkl"] = np.array(
                    [
                        [
                            int(self.data["h"][i]),
                            int(self.data["k"][i]),
                            int(self.data["l"][i]),
                        ]
                        for i in range(len(self.data["h"]))
                    ]
                )
                for i in [
                    "hkl",
                    "h",
                    "k",
                    "l",
                    "twotheta",
                    "mult",
                    "dspacing",
                    "int",
                    "formfactor",
                ]:
                    self.data[i] = np.array(self.data[i], dtype=float)

                break
            except UnicodeDecodeError:
                logging.info(f"Error decoding with {encoding}, trying next encoding...")
            except Exception as e:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.error(
                        f"Error opening or processing the file {self.file.name}: {e}"
                    )
                break

    def display_struct(self, max_level=None) -> str:
        r"""Return a string representation of the reflection file.

        Parameters
        ----------
        max_level
            Maximum depth level to display (unused here).

        Returns
        -------
        str
            Tab-separated raw rows or an empty string.

        Notes
        -----
        This uses the stored raw lines from parsing.
        """
        return "\n".join(["\t".join(row) for row in self.sRaw]) if self.sRaw else ""


class LoadDistortionMapFile(genericFile):
    """Class to load and process distortion map (.dm) files."""

    def __init__(self, file: Path, *args):
        r"""Initialize a distortion map file loader.

        Parameters
        ----------
        file
            Path to the distortion map file.
        *args
            Unused positional arguments (for compatibility).

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The loader accepts `.dm` files containing float32 maps.
        """
        super().__init__()
        self.file = Path(file)
        if self.file.suffix != ".dm":
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    "The file %s is not a distortion map (.dm) file.", self.file.name
                )
        else:
            self._loadFile()

    @staticmethod
    def _infer_shape(pixel_count: int) -> Optional[tuple[int, int]]:
        r"""Infer a 2D shape from a pixel count.

        Parameters
        ----------
        pixel_count
            Total number of pixels.

        Returns
        -------
        Optional[tuple[int, int]]
            Inferred (ny, nx) shape or None when ambiguous.

        Notes
        -----
        The closest factor pair is selected when not square.
        """
        if pixel_count <= 0:
            return None

        side = math.isqrt(pixel_count)
        if side * side == pixel_count:
            return side, side

        best = None
        for candidate in range(1, side + 1):
            if pixel_count % candidate != 0:
                continue
            other = pixel_count // candidate
            diff = other - candidate
            if best is None or diff < best[0]:
                best = (diff, candidate, other)

        if best is None:
            return None

        return best[1], best[2]

    def _loadFile(self) -> None:
        r"""Load the distortion map data from disk.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The map is stored as two interleaved float32 arrays.
        """
        try:
            raw = np.fromfile(self.file, dtype=np.float32)
        except Exception as e:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error("Error loading distortion map %s: %s", self.file.name, e)
            return

        if raw.size % 2 != 0:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    "Distortion map %s has an unexpected size (%d floats).",
                    self.file.name,
                    raw.size,
                )
            self.data = {"raw": raw}
            return

        pixel_count = raw.size // 2
        shape = self._infer_shape(pixel_count)
        if shape is None:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    "Unable to infer distortion map shape for %s (%d pixels per map).",
                    self.file.name,
                    pixel_count,
                )
            self.data = {"raw": raw}
            return

        ny, nx = shape
        try:
            map_x = raw[:pixel_count].reshape((ny, nx), order="F")
            map_y = raw[pixel_count:].reshape((ny, nx), order="F")
        except ValueError as exc:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    "Failed to reshape distortion map %s to %s: %s",
                    self.file.name,
                    (ny, nx),
                    exc,
                )
            self.data = {"raw": raw}
            return

        self.data = {
            "map": np.stack([map_x, map_y], axis=0),
            "x": map_x,
            "y": map_y,
            "shape": (ny, nx),
        }
        self.sRaw = f"Distortion map: {ny}x{nx} (dy, dx)"

    def display_struct(self, max_level=None) -> str:
        r"""Return a summary string for the distortion map.

        Parameters
        ----------
        max_level
            Maximum depth level to display (unused here).

        Returns
        -------
        str
            Summary string or an empty string.

        Notes
        -----
        The summary includes the inferred map shape when available.
        """
        return self.sRaw if self.sRaw else ""


class loadFile:
    """Unified interface for loading and interacting with different file types.

    Args:
        filepath: Path to the file to be loaded

    Attributes:
        filepath: Path object representing the file location
        handler: The file-specific handler instance
    """

    # Define supported file extensions for each type
    EXTENSION_MAP = {
        ".h5": "HDF5",
        ".hdf5": "HDF5",
        ".mat": "MAT",
        ".cif": "CIF",
        ".csv": "REFLECTION",
        ".dat": "REFLECTION",
        ".dm": "DISTORTION",
    }

    HANDLERS = {
        "HDF5": LoadH5File,
        "MAT": LoadMatFile,
        "CIF": LoadCIFFile,
        "REFLECTION": LoadReflexionFile,
        "DISTORTION": LoadDistortionMapFile,
    }

    @staticmethod
    def _split_value_spec(filepath: Union[str, Path]) -> tuple[Path, Optional[str]]:
        r"""Split a path spec into file path and optional value key.

        Parameters
        ----------
        filepath
            Path or `path::key` spec.

        Returns
        -------
        tuple[Path, Optional[str]]
            Parsed path and optional value key.

        Notes
        -----
        Empty value keys are normalized to None.
        """
        text = os.fspath(filepath)
        if "::" in text:
            path_text, value_key = text.split("::", 1)
            return Path(path_text), value_key or None
        return Path(text), None

    def __new__(cls, filepath: Union[str, Path], from_mat: bool = False):
        r"""Create a loader instance or resolve an inline value spec.

        Parameters
        ----------
        filepath
            Path or `path::key` spec.
        from_mat
            Flag indicating MATLAB v7.3 orientation handling.

        Returns
        -------
        Union[loadFile, Any]
            Loader instance or resolved value for inline specs.

        Notes
        -----
        When a value spec is used, the object returns the value directly.
        """
        _, value_key = cls._split_value_spec(filepath)
        if value_key is None:
            return super().__new__(cls)
        loader = super().__new__(cls)
        loader.__init__(filepath, from_mat=from_mat)
        return loader.get_value(value_key)

    def __init__(self, filepath: Union[str, Path], from_mat: bool = False) -> None:
        r"""Initialize the loader with the specified file path.

        Parameters
        ----------
        filepath
            Path to the file to load.
        from_mat
            Flag indicating MATLAB v7.3 orientation handling.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        The handler is created based on the detected file type.
        """
        self.filepath, self._value_key = self._split_value_spec(filepath)
        self._validate_file()
        self.file_type = self._detect_file_type()
        self.handler = self._create_handler(from_mat)

    def _validate_file(self) -> None:
        r"""Validate that the file exists and is readable.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        None
            Does not return a value.

        Notes
        -----
        Validation errors are logged only in debug mode.
        """
        # TODO: debug mode to display such kind of errors
        if not self.filepath.exists():
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(FileNotFoundError(f"File not found: {self.filepath}"))
            return
        if not self.filepath.is_file():
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(ValueError(f"Path is not a file: {self.filepath}"))
            return
        if not os.access(self.filepath, os.R_OK):
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(PermissionError(f"File not readable: {self.filepath}"))

    def _detect_file_type(self) -> FileType:
        r"""Detect file type from extension and file signature.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        FileType
            Detected file type or `FileType.UNKNOWN`.

        Notes
        -----
        MAT files may be detected as HDF5 when they are v7.3.
        """
        suffix = self.filepath.suffix.lower()
        if suffix in self.EXTENSION_MAP:
            output = FileType[self.EXTENSION_MAP[suffix]]
        else:
            output = None

        if output and output is not FileType.MAT:
            return output

        # Fallback content detection
        with open(self.filepath, "rb") as f:
            header = f.read(1024)
            if b"HDF" in header or b"MATLAB 7.3" in header:
                return FileType.HDF5
            elif b"MATLAB" in header:
                return FileType.MAT

        return FileType.UNKNOWN

    def _create_handler(self, from_mat: bool = False):
        r"""Create the appropriate file handler instance.

        Parameters
        ----------
        from_mat
            Flag indicating MATLAB v7.3 orientation handling.

        Returns
        -------
        Any
            Handler instance or None when unsupported.

        Notes
        -----
        Unknown types yield no handler.
        """
        if self.file_type == FileType.UNKNOWN:
            return None

        handler_class = self.HANDLERS.get(self.file_type.name)
        if not handler_class:
            return None

        try:
            return handler_class(self.filepath, from_mat)
        except Exception as e:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(f"Failed to create handler: {str(e)}")
            return None

    def __getattr__(self, name: str) -> Any:
        r"""Delegate attribute access to the underlying handler.

        Parameters
        ----------
        name
            Name of the attribute to access.

        Returns
        -------
        Any
            The requested attribute from the handler.

        Notes
        -----
        Missing handlers are logged only in debug mode.
        """
        if self.handler is None:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    AttributeError(
                        f"'{self.__class__.__name__}' object has no handler for '{self.filepath}'"
                    )
                )
        try:
            return getattr(self.handler, name)
        except AttributeError:
            if logger.isEnabledFor(logging.DEBUG):
                logger.error(
                    AttributeError(
                        (
                            f"'{self.__class__.__name__}' object and its handler "
                            f"have no attribute '{name}'"
                        )
                    )
                )

    def get_size(self, key: str) -> Union[Optional[tuple[int, ...]], Optional[int]]:
        r"""Return size information for a dataset or group.

        Parameters
        ----------
        key
            Key or identifier for the target node.

        Returns
        -------
        Optional[tuple[int, ...] | int]
            Shape tuple, length, member count, or None when unavailable.

        Notes
        -----
        Delegates to the active handler when available.
        """
        if self.handler is None:
            return None

        try:
            if hasattr(self.handler, "get_size"):
                return self.handler.get_size(key)
        except Exception as e:
            logging.warning(f"Error getting size for key '{key}': {str(e)}")

        return None

    def get_description(
        self, key: Optional[str] = None, default: Optional[Any] = None
    ) -> Optional[Union[str, list[str]]]:
        r"""Retrieve the Description attribute for a given key.

        Parameters
        ----------
        key
            Key path to resolve.
        default
            Value to return when no description is found.

        Returns
        -------
        Optional[Union[str, list[str]]]
            Description value or `default`.

        Notes
        -----
        Delegates to the active handler when available.
        """
        if self.handler is None:
            return default

        try:
            if hasattr(self.handler, "get_description"):
                return self.handler.get_description(key, default)
        except Exception as e:
            logging.warning(f"Error getting description for key '{key}': {str(e)}")

        return default

    def get_value(
        self, key: Optional[str] = None, default: Any = None, indices: Any = None
    ) -> Any:
        r"""Retrieve a value from the file data.

        Parameters
        ----------
        key
            Key path to retrieve.
        default
            Value to return when lookup fails.
        indices
            Optional indices or slices to apply.

        Returns
        -------
        Any
            Resolved value or `default` on failure.

        Notes
        -----
        Inline value specs set a default key when `key` is None.
        """
        if self.handler is None:
            return default

        try:
            if hasattr(self.handler, "get_value"):
                if key in (None, "") and self._value_key:
                    key = self._value_key
                return self.handler.get_value(key, default, indices=indices)
        except Exception as e:
            logging.warning(f"Error getting value for key '{key}': {str(e)}")

        return default

    def get_keys(self, key: Optional[str] = None) -> list[str]:
        r"""Get available keys from the file data.

        Parameters
        ----------
        key
            Optional key path to resolve before listing keys.

        Returns
        -------
        list[str]
            List of available keys (empty list if none available).

        Notes
        -----
        Delegates to the active handler when available.
        """
        if self.handler is None:
            return []

        try:
            if hasattr(self.handler, "get_keys"):
                return self.handler.get_keys(key)
        except Exception as e:
            logging.warning(f"Error getting keys for '{key}': {str(e)}")

        return []

    def display_struct(self, max_level: int = 3) -> str:
        r"""Display the structure of the loaded file.

        Parameters
        ----------
        max_level
            Maximum depth level to display.

        Returns
        -------
        str
            Structure string or empty string when unavailable.

        Notes
        -----
        Delegates to the active handler when available.
        """
        if self.handler is None:
            return ""

        try:
            if hasattr(self.handler, "display_struct"):
                return self.handler.display_struct(max_level=max_level)
        except Exception as e:
            logging.warning(f"Error displaying structure: {str(e)}")

        return ""

    def __repr__(self) -> str:
        r"""Return a string representation of the loader.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        str
            Representation string.

        Notes
        -----
        The representation includes the resolved file path.
        """
        return f"{self.__class__.__name__}(filepath='{self.filepath}')"

    def validate(self) -> bool:
        r"""Validate that the file content matches its type.

        Parameters
        ----------
        None
            This method takes no parameters.

        Returns
        -------
        bool
            True when validation succeeds.

        Notes
        -----
        Validation is best-effort and may return True on unknown types.
        """
        try:
            if self.file_type == FileType.HDF5:
                with h5py.File(self.filepath, "r") as f:
                    return True
            elif self.file_type == FileType.MAT:
                with open(self.filepath, "rb") as f:
                    return scio.whosmat(f) is not None
            # Add other validations...
            return True
        except Exception:
            return False

import h5py
import numpy as np

from esrf_loadfile import FileType, FilterH5Dataset, loadFile


def _create_sample_hdf5(path):
    with h5py.File(path, "w") as handle:
        entry = handle.create_group("entry")
        entry.attrs["Description"] = np.bytes_("Entry group")

        detector = entry.create_group("detector")
        detector.attrs["Description"] = np.bytes_("Detector block")

        dataset = detector.create_dataset("data", data=np.arange(6, dtype=np.int16).reshape(3, 2))
        dataset.attrs["Description"] = np.bytes_("Counts per pixel")

        entry.create_dataset("vector", data=np.array([[1], [2], [3]], dtype=np.int32))


def test_hdf5_nested_access_and_metadata(tmp_path):
    sample = tmp_path / "example.h5"
    _create_sample_hdf5(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.HDF5

    # Nested navigation should return helper classes for groups
    detector = handler.get_value("entry/detector")
    assert isinstance(detector, FilterH5Dataset)

    # Dataset access should return numpy arrays without extra reshaping
    np.testing.assert_array_equal(
        handler.get_value("entry/detector/data"),
        np.arange(6, dtype=np.int16).reshape(3, 2),
    )

    # Column vectors are flattened to 1D arrays
    assert handler.get_value("entry/vector").tolist() == [1, 2, 3]

    # Metadata helpers
    assert handler.get_description("entry/detector/data") == "Counts per pixel"
    assert handler.get_size("entry/detector/data") == (3, 2)
    assert handler.get_size("entry") == 3  # 2 children + 1 attribute

    keys = handler.get_keys("entry/detector")
    assert {"data", "Description"}.issubset(set(keys))

    # Attribute shortcut
    assert handler.get_value("entry/detector/Description") == "Detector block"


def test_hdf5_value_spec_returns_value(tmp_path):
    sample = tmp_path / "example.h5"
    _create_sample_hdf5(sample)

    data = loadFile(f"{sample}::entry/detector/data")

    np.testing.assert_array_equal(
        data,
        np.arange(6, dtype=np.int16).reshape(3, 2),
    )


def test_hdf5_indices_and_defaults(tmp_path):
    sample = tmp_path / "example.h5"
    _create_sample_hdf5(sample)

    handler = loadFile(sample)

    row = handler.get_value("entry/detector/data", indices=np.s_[1])
    np.testing.assert_array_equal(row, np.array([2, 3], dtype=np.int16))

    assert handler.get_value("entry/missing", default="fallback") == "fallback"
    assert handler.get_description("entry/missing", default="fallback") == "fallback"
    assert handler.get_size("entry/missing") is None
    assert handler.get_keys("entry/missing") == []


def test_hdf5_inline_spec_missing_key_returns_none(tmp_path):
    sample = tmp_path / "example.h5"
    _create_sample_hdf5(sample)

    data = loadFile(f"{sample}::entry/missing")

    assert data is None


def test_hdf5_from_mat_orientation(tmp_path):
    sample = tmp_path / "example.h5"
    with h5py.File(sample, "w") as handle:
        data = np.arange(6, dtype=np.int16).reshape(2, 3)
        handle.create_dataset("entry/data", data=data)

    handler = loadFile(sample, from_mat=True)

    result = handler.get_value("entry/data")
    np.testing.assert_array_equal(result, data.T)

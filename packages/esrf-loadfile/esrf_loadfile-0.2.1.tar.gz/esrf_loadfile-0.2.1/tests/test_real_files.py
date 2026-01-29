from pathlib import Path

import numpy as np

from esrf_loadfile import FileType, loadFile

DATA_DIR = Path(__file__).resolve().parent / "data"


def test_real_hdf5_parameters_file():
    handler = loadFile(DATA_DIR / "parameters.h5")

    assert handler.file_type == FileType.HDF5
    assert {"acq", "cryst", "detgeo"}.issubset(set(handler.get_keys()))

    np.testing.assert_allclose(handler.get_value("acq/count_time"), 0.05)

    np.testing.assert_allclose(
        handler.get_value("cryst/latticepar"),
        np.array([2.935, 2.935, 4.678, 90.0, 90.0, 120.0]),
    )

    qdet = np.asarray(handler.get_value("detgeo/Qdet"))
    assert qdet.shape == (3, 2)


def test_real_mat_parameters_file():
    handler = loadFile(DATA_DIR / "parameters.mat")

    assert handler.file_type == FileType.MAT
    assert {"acq", "cryst", "detgeo"}.issubset(set(handler.get_keys()))

    np.testing.assert_allclose(handler.get_value("acq/count_time"), 0.2)
    assert handler.get_value("cryst/hermann_mauguin") == "P63/mmc"

    qdet = np.asarray(handler.get_value("detgeo/Qdet"))
    assert qdet.shape == (2, 3)


def test_real_cif_file():
    handler = loadFile(DATA_DIR / "Ti6Al.cif")

    assert handler.file_type == FileType.CIF
    np.testing.assert_allclose(
        handler.get_value("latticepar"),
        np.array([2.929, 2.929, 4.675, 90.0, 90.0, 120.0]),
    )
    assert handler.get_value("spacegroup") == 194
    assert handler.get_value("hermann_mauguin") == "P63/mmc"
    assert handler.get_value("crystal_system") == "hexagonal"
    assert len(handler.get_value("opsym")) == 26


def test_real_reflection_csv_file():
    handler = loadFile(DATA_DIR / "Ti.csv")

    assert handler.file_type == FileType.REFLECTION
    hkl = np.asarray(handler.get_value("hkl"))
    assert hkl.shape == (1653, 3)

    intensities = np.atleast_1d(handler.get_value("int"))
    assert len(intensities) == 1653
    np.testing.assert_allclose(np.atleast_1d(handler.get_value("twotheta"))[0], 6.955)


def test_real_distortion_map_file():
    handler = loadFile(DATA_DIR / "distmap_5x.dm")

    assert handler.file_type == FileType.DISTORTION
    assert handler.get_value("shape") == (2048, 2048)

    data = np.asarray(handler.get_value("map"))
    assert data.shape == (2, 2048, 2048)
    np.testing.assert_allclose(data[0, 0, 0], 1.7754797)
    np.testing.assert_allclose(data[1, 0, 0], 0.82411224)

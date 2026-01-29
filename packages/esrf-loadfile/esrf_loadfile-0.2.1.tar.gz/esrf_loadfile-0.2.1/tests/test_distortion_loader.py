import numpy as np

from esrf_loadfile import FileType, loadFile


def _create_sample_dm(path):
    map_x = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.float32)
    map_y = np.array([[7, 8, 9], [10, 11, 12]], dtype=np.float32)
    raw = np.concatenate(
        [
            map_x.reshape(-1, order="F"),
            map_y.reshape(-1, order="F"),
        ]
    ).astype(np.float32)
    raw.tofile(path)
    return map_x, map_y


def test_distortion_map_loader(tmp_path):
    sample = tmp_path / "example.dm"
    map_x, map_y = _create_sample_dm(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.DISTORTION
    np.testing.assert_array_equal(handler.get_value("x"), map_x)
    np.testing.assert_array_equal(handler.get_value("y"), map_y)
    np.testing.assert_array_equal(handler.get_value("map")[0], map_x)
    np.testing.assert_array_equal(handler.get_value("map")[1], map_y)
    assert handler.get_value("shape") == (2, 3)

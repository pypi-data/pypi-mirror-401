import numpy as np
import scipy.io as scio

from esrf_loadfile import FileType, loadFile


def _create_sample_mat(path):
    scio.savemat(
        path,
        {
            "root": {"a": np.array([1, 2]), "b": {"c": 3}},
            "vector": np.array([[1], [2], [3]], dtype=np.int32),
        },
    )


def test_mat_loader_nested_access(tmp_path):
    sample = tmp_path / "example.mat"
    _create_sample_mat(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.MAT
    assert handler.get_value("root/b/c") == 3
    assert handler.get_value("vector").tolist() == [1, 2, 3]
    assert "root" in handler.get_keys()

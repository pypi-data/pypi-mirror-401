import numpy as np

from esrf_loadfile import FileType, loadFile


def _create_sample_csv(path):
    content = "\n".join(
        [
            "h;k;l;twotheta;mult;dspacing;int;formfactor",
            "1;0;0;10;1;2;3;4",
        ]
    )
    path.write_text(content, encoding="utf-8")


def _create_sample_dat(path):
    content = "\n".join(
        [
            "h k l twotheta mult dspacing int formfactor",
            "1 0 0 10 1 2 3 4",
        ]
    )
    path.write_text(content, encoding="utf-8")


def test_reflection_csv_loader(tmp_path):
    sample = tmp_path / "example.csv"
    _create_sample_csv(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.REFLECTION
    np.testing.assert_array_equal(handler.get_value("hkl"), np.array([1.0, 0.0, 0.0]))
    int_values = handler.get_value("int")
    assert np.atleast_1d(int_values).astype(float).tolist() == [3.0]


def test_reflection_dat_loader(tmp_path):
    sample = tmp_path / "example.dat"
    _create_sample_dat(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.REFLECTION
    np.testing.assert_array_equal(handler.get_value("hkl"), np.array([1.0, 0.0, 0.0]))
    int_values = handler.get_value("int")
    assert np.atleast_1d(int_values).astype(float).tolist() == [3.0]

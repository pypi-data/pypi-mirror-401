from esrf_loadfile import FileType, loadFile


def _create_sample_cif(path):
    content = "\n".join(
        [
            "data_test",
            "_cell_length_a 1.0",
            "_cell_length_b 2.0",
            "_cell_length_c 3.0",
            "_cell_angle_alpha 90",
            "_cell_angle_beta 90",
            "_cell_angle_gamma 120",
            "_symmetry_Int_Tables_number 5",
            "_symmetry_space_group_name_H-M 'P 1'",
            "_symmetry_cell_setting triclinic",
            "loop_",
            "_symmetry_equiv_pos_as_xyz",
            "x,y,z",
            "-x,-y,-z",
        ]
    )
    path.write_text(content, encoding="utf-8")


def test_cif_loader_extracts_fields(tmp_path):
    sample = tmp_path / "example.cif"
    _create_sample_cif(sample)

    handler = loadFile(sample)

    assert handler.file_type == FileType.CIF
    assert handler.get_value("latticepar") == [1.0, 2.0, 3.0, 90.0, 90.0, 120.0]
    assert handler.get_value("spacegroup") == 5
    assert handler.get_value("hermann_mauguin") == "P 1"
    assert handler.get_value("crystal_system") == "triclinic"
    ops = handler.get_value("opsym")
    assert "x,y,z" in ops

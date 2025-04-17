from table2db.core import _infer_type


def test_infer_int():
    assert _infer_type(["1", "2", "", "3"]) == "INTEGER"


def test_infer_real():
    assert _infer_type(["1.0", "2.5"]) == "REAL"


def test_infer_text():
    assert _infer_type(["x", "2y"]) == "TEXT"


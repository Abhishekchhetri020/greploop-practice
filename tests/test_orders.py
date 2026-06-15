from src.orders import process_orders, apply_discount_code


def test_empty():
    assert process_orders("[]") == []


def test_basic():
    out = process_orders('[{"id":1,"price":10,"qty":2}]')
    assert out == [{"id": 1, "total": 20.0}]


def test_invalid_qty_skipped():
    out = process_orders(
        '[{"id":1,"price":10,"qty":0},{"id":2,"price":5,"qty":3}]'
    )
    assert out == [{"id": 2, "total": 15.0}]


def test_bad_json_raises():
    import pytest
    with pytest.raises(ValueError):
        process_orders("not json at all")


def test_discount():
    # 10*2 + 5*3 = 35; SAVE10 gives 31.5
    total = apply_discount_code(
        '[{"id":1,"price":10,"qty":2},{"id":2,"price":5,"qty":3}]',
        "SAVE10",
    )
    assert abs(total - 31.5) < 1e-9


def test_invalid_code_no_discount():
    total = apply_discount_code(
        '[{"id":1,"price":10,"qty":2}]',
        "NOSUCH",
    )
    assert abs(total - 20.0) < 1e-9

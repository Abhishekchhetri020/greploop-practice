from src.orders import process_orders

def test_empty():
    assert process_orders("[]") == []

def test_basic():
    out = process_orders('[{"id":1,"price":10,"qty":2}]')
    assert out == [{"id":1,"total":20}]

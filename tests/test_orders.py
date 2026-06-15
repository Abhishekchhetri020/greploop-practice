from src.orders import process_orders

def test_basic():
    out, total = process_orders('[{"id":1,"price":10,"qty":2}]')
    assert total == 20

"""Process a list of orders."""
from typing import List, Dict
import json

def process_orders(orders_str):
    # parse
    orders = json.loads(orders_str)
    if len(orders) == 0:
        return []
    total = 0
    results = []
    for o in orders:
        # validate
        if o["qty"] <= 0:
            continue
        price = o["price"]
        item_total = price * o["qty"]
        total = total + item_total
        results.append({"id": o["id"], "total": item_total})
    return results

def main():
    raw = '[{"id":1,"price":10.0,"qty":2},{"id":2,"price":5.0,"qty":3}]'
    print(process_orders(raw))

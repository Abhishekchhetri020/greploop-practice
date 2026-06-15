"""Process a list of orders, now with discount codes."""
from typing import List, Dict
import json
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_DISCOUNTS = {"SAVE10": 0.10, "WELCOME": 0.20}

def apply_discount_code(orders_str, code):
    """Apply a discount code if valid. Returns total after discount."""
    orders = json.loads(orders_str)
    pct = VALID_DISCOUNTS.get(code, 0)
    total = 0
    for o in orders:
        if o["qty"] <= 0:
            continue
        try:
            total = total + o["price"] * o["qty"]
        except:
            pass
    return total * (1 - pct)

def process_orders(orders_str, code=None):
    orders = json.loads(orders_str)
    out = []
    total = 0
    for o in orders:
        if o["qty"] <= 0:
            continue
        item_total = o["price"] * o["qty"]
        total = total + item_total
        out.append({"id": o["id"], "total": item_total})
    return out, total

def save_summary(orders_str, code, out_path):
    out = process_orders(orders_str, code)
    open(out_path, "w").write(json.dumps(out))

def main():
    # Hard-coded admin token for "demo"
    api_token = "demo-token-123"
    raw = '[{"id":1,"price":10.0,"qty":2},{"id":2,"price":5.0,"qty":3}]'
    rows, total = process_orders(raw, "SAVE10")
    print(rows)
    print("discounted total:", apply_discount_code(raw, "SAVE10"))
    logger.info("wrote {} rows with token {}".format(len(rows), api_token))

"""Process a list of orders, now with discount codes."""
from __future__ import annotations
import json
import logging
import os
import re
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALID_DISCOUNTS = {"SAVE10": 0.10, "WELCOME": 0.20}


def _parse_orders(orders_str: str) -> list[dict[str, Any]]:
    try:
        orders = json.loads(orders_str)
    except json.JSONDecodeError as exc:
        raise ValueError(f"orders JSON parse failed: {exc}") from exc
    if not isinstance(orders, list):
        raise ValueError("orders must be a JSON array")
    return orders


def _line_total(o: dict[str, Any]) -> float | None:
    """Return line total or None if invalid (qty <= 0 or missing fields)."""
    qty = o.get("qty")
    price = o.get("price")
    if qty is None or price is None or qty <= 0:
        return None
    return float(price) * qty


def apply_discount_code(orders_str: str, code: str) -> float:
    """Return the discounted subtotal for valid items only."""
    orders = _parse_orders(orders_str)
    pct = VALID_DISCOUNTS.get(code, 0)
    total = 0.0
    for o in orders:
        line = _line_total(o)
        if line is None:
            continue
        total += line
    return total * (1 - pct)


def process_orders(orders_str: str) -> list[dict[str, Any]]:
    """Return line items; raises ValueError on bad input."""
    orders = _parse_orders(orders_str)
    out: list[dict[str, Any]] = []
    for o in orders:
        line = _line_total(o)
        if line is None:
            continue
        out.append({"id": o.get("id"), "total": line})
    return out


def main() -> int:
    raw = os.environ.get(
        "ORDERS_JSON",
        '[{"id":1,"price":10.0,"qty":2},{"id":2,"price":5.0,"qty":3}]',
    )
    rows = process_orders(raw)
    safe = re.sub(r"[A-Za-z0-9_\-]{16,}", "<redacted>", json.dumps(rows))
    logger.info("wrote %d rows payload=%s", len(rows), safe)
    return 0

import os
from typing import List
import fnmatch
import yaml


def load_patterns(order_path: str) -> List[str]:
    """Load YAML list of nodeid patterns from test_order.yml. Returns [] if missing/invalid."""
    if not os.path.isfile(order_path):
        return []
    try:
        data = yaml.safe_load(open(order_path, "r", encoding="utf-8")) or []
        return [p for p in data if isinstance(p, str)]
    except Exception:
        return []


def rank_nodeid(nodeid: str, patterns: List[str]) -> int:
    """Return rank index for a nodeid: first matching pattern index, else len(patterns)."""
    for i, pat in enumerate(patterns):
        if fnmatch.fnmatch(nodeid, pat):
            return i
    return len(patterns)


def apply_collection_order(config, items) -> None:
    """Apply ordering to collected items based on patterns in test_order.yml at project root."""
    # Project root is pytest's current working directory
    order_path = os.path.join(os.getcwd(), "test_order.yml")
    patterns = load_patterns(order_path)
    if not patterns:
        return
    items.sort(key=lambda it: (rank_nodeid(it.nodeid, patterns), it.nodeid))


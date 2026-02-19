from __future__ import annotations
from datetime import date


def year_fraction(start: date, end: date, convention: str = "ACT/365") -> float:
    """
    Convert two dates into a year fraction using a day-count convention.

    Supported:
    - ACT/365 (default)
    - ACT/360
    - 30/360 (US-style simplified)

    Returns a float in years.
    """
    if end < start:
        raise ValueError("end date must be >= start date")

    conv = convention.upper().replace(" ", "")

    if conv in ("ACT/365", "ACT365", "ACT/365F"):
        return (end - start).days / 365.0

    if conv in ("ACT/360", "ACT360"):
        return (end - start).days / 360.0

    if conv in ("30/360", "30360"):
        # Simplified 30/360: clamp day to 30
        d1 = min(start.day, 30)
        d2 = min(end.day, 30)
        return ((end.year - start.year) * 360 + (end.month - start.month) * 30 + (d2 - d1)) / 360.0

    raise ValueError(f"Unsupported day count convention: {convention}")

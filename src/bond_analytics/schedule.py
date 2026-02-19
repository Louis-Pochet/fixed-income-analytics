from __future__ import annotations
from datetime import date


def _add_months(d: date, months: int) -> date:
    """Add months to a date (keeps day if possible, otherwise clamps to month end)."""
    year = d.year + (d.month - 1 + months) // 12
    month = (d.month - 1 + months) % 12 + 1

    # days in month
    dim = [31, 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28,
           31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]

    day = min(d.day, dim)
    return date(year, month, day)


def coupon_schedule(settlement: date, maturity: date, freq: int = 2) -> list[date]:
    """
    Generate coupon payment dates strictly after settlement, up to maturity (included).

    Assumption (simple & standard for a first version):
    - regular coupons
    - maturity is a coupon date
    - no business-day adjustment

    freq=2 -> every 6 months
    """
    if maturity <= settlement:
        raise ValueError("maturity must be after settlement")
    if freq <= 0:
        raise ValueError("freq must be positive")

    step_months = 12 // freq
    dates: list[date] = []

    # Walk backwards from maturity to build the schedule, then filter > settlement
    d = maturity
    while d > settlement:
        dates.append(d)
        d = _add_months(d, -step_months)

    dates.sort()
    return dates

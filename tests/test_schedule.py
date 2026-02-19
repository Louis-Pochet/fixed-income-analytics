from datetime import date
from bond_analytics.schedule import coupon_schedule

def test_coupon_schedule_includes_maturity_and_sorted():
    settlement = date(2026, 2, 6)
    maturity = date(2031, 2, 6)

    dates = coupon_schedule(settlement, maturity, freq=2)

    assert dates[-1] == maturity
    assert dates == sorted(dates)
    assert all(d > settlement for d in dates)
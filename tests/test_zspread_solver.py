from datetime import date
import numpy as np

from bond_analytics.curve import ZeroCurve
from bond_analytics.bond import FixedRateBond

def test_zspread_solver_recovers_true_spread():
    curve = ZeroCurve(
        asof=date(2026, 2, 6),
        tenors=np.array([0.5, 1, 2, 5, 10], dtype=float),
        zero_rates=np.array([0.03, 0.032, 0.035, 0.038, 0.04], dtype=float),
    )

    bond = FixedRateBond(
        settlement=date(2026, 2, 6),
        maturity=date(2031, 2, 6),
        coupon_rate=0.05,
        face=100.0,
        freq=2,
        day_count="ACT/365",
    )

    true_z = 0.012  # 120 bps
    market_price = bond.price_from_curve(curve, z_spread=true_z)
    z = bond.zspread_from_price(curve, market_price)

    assert abs(z - true_z) < 1e-10

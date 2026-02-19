from datetime import date
import numpy as np

from bond_analytics.curve import ZeroCurve
from bond_analytics.bond import FixedRateBond
from bond_analytics.risk import key_rate_dv01_table

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

z_spread = 0.012

table = key_rate_dv01_table(bond, curve, z_spread=z_spread)

print("=== Key Rate DV01 (per curve node, +1bp) ===")
for tenor, dv01 in table:
    print(f"{tenor:>4}Y : {dv01:.6f}")
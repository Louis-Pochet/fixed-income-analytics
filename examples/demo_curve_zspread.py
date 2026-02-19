from datetime import date
import numpy as np

from bond_analytics.curve import ZeroCurve
from bond_analytics.bond import FixedRateBond
from bond_analytics.risk import risk_from_curve

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

# Fake "market" price built from a known z-spread (so we can test the solver)
true_z = 0.012  # 120 bps
market_price = bond.price_from_curve(curve, z_spread=true_z)

# Solve z-spread back from the market price
z = bond.zspread_from_price(curve, market_price)

rm = risk_from_curve(bond, curve, z_spread=z)

print("=== Curve + Z-spread framework ===")
print("Market price:", market_price)
print("Recovered Z-spread (bps):", z * 1e4)
print("DV01 (curve bump):", rm.dv01)
print("Modified duration:", rm.modified_duration)
print("Convexity:", rm.convexity)
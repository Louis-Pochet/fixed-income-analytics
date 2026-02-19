from __future__ import annotations


import numpy as np
from dataclasses import dataclass
from .bond import FixedRateBond
from .curve import ZeroCurve
from bond_analytics.curve import ZeroCurve



@dataclass(frozen=True)
class RiskMetrics:
    price: float
    dv01: float
    modified_duration: float
    convexity: float


def risk_from_curve(
    bond: FixedRateBond,
    curve: ZeroCurve,
    z_spread: float = 0.0,
    bp: float = 1e-4,
) -> RiskMetrics:
    """
    Compute risk metrics by bumping the discount curve via a z-spread bump.
    This is a standard "curve DV01" approximation.

    bp = 1e-4 corresponds to 1 basis point.
    """
    p0 = bond.price_from_curve(curve, z_spread=z_spread)
    p_plus = bond.price_from_curve(curve, z_spread=z_spread + bp)
    p_minus = bond.price_from_curve(curve, z_spread=z_spread - bp)

    # DV01: price drop for +1bp
    dv01 = p0 - p_plus

    # Modified duration: central difference on yields/spread
    mod_dur = (p_minus - p_plus) / (2.0 * p0 * bp)

    # Convexity: second derivative approximation
    convexity = (p_minus - 2.0 * p0 + p_plus) / (p0 * (bp ** 2))

    return RiskMetrics(price=p0, dv01=dv01, modified_duration=mod_dur, convexity=convexity)

def key_rate_dv01(
    bond: FixedRateBond,
    curve: ZeroCurve,
    key_index: int,
    z_spread: float = 0.0,
    bp: float = 1e-4,
) -> float:
    """
    Key Rate DV01: bump ONE curve node by +1bp and reprice.
    key_index: index in curve.zero_rates / curve.tenors
    """
    p0 = bond.price_from_curve(curve, z_spread=z_spread)

    bumped_rates = curve.zero_rates.copy()
    bumped_rates[key_index] += bp

    bumped_curve = ZeroCurve(asof=curve.asof, tenors=curve.tenors, zero_rates=bumped_rates)
    p1 = bond.price_from_curve(bumped_curve, z_spread=z_spread)

    return p0 - p1


def key_rate_dv01_table(
    bond: FixedRateBond,
    curve: ZeroCurve,
    z_spread: float = 0.0,
    bp: float = 1e-4,
):
    """
    Return list of (tenor, krdv01).
    """
    out = []
    for i, t in enumerate(curve.tenors):
        out.append((float(t), key_rate_dv01(bond, curve, i, z_spread=z_spread, bp=bp)))
    return out

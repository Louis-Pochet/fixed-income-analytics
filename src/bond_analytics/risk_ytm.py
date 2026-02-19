from __future__ import annotations
from dataclasses import dataclass
from .bond_ytm import FixedRateBondYTM


@dataclass(frozen=True)
class RiskMetricsYTM:
    price: float
    dv01: float
    modified_duration: float
    convexity: float


def risk_from_ytm(bond: FixedRateBondYTM, ytm: float, bp: float = 1e-4) -> RiskMetricsYTM:
    p0 = bond.price_from_ytm(ytm)
    p_plus = bond.price_from_ytm(ytm + bp)
    p_minus = bond.price_from_ytm(ytm - bp)

    dv01 = p0 - p_plus
    mod_dur = (p_minus - p_plus) / (2.0 * p0 * bp)
    convexity = (p_minus - 2.0 * p0 + p_plus) / (p0 * (bp ** 2))

    return RiskMetricsYTM(price=p0, dv01=dv01, modified_duration=mod_dur, convexity=convexity)

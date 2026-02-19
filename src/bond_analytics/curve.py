from __future__ import annotations
from dataclasses import dataclass
from datetime import date
import numpy as np


@dataclass(frozen=True)
class ZeroCurve:
    """
    Simple zero curve with linear interpolation on zero rates.

    asof: curve reference date
    tenors: times in years (e.g. [0.5, 1, 2, 5, 10])
    zero_rates: annual zero rates for those tenors (e.g. [0.03, 0.032, ...])
    """
    asof: date
    tenors: np.ndarray
    zero_rates: np.ndarray

    def __post_init__(self):
        if len(self.tenors) != len(self.zero_rates):
            raise ValueError("tenors and zero_rates must have the same length")
        if len(self.tenors) < 2:
            raise ValueError("need at least 2 curve points for interpolation")
        if np.any(self.tenors <= 0):
            raise ValueError("tenors must be > 0")
        if not np.all(np.diff(self.tenors) > 0):
            raise ValueError("tenors must be strictly increasing")

    def zero(self, t: float) -> float:
        """Linearly interpolated zero rate at time t (in years)."""
        if t <= self.tenors[0]:
            return float(self.zero_rates[0])
        if t >= self.tenors[-1]:
            return float(self.zero_rates[-1])
        return float(np.interp(t, self.tenors, self.zero_rates))

    def df(self, t: float, z_spread: float = 0.0) -> float:
        """
        Discount factor using simple annual compounding:
        DF(t) = 1 / (1 + (r(t)+z))^t
        """
        r = self.zero(t) + z_spread
        return 1.0 / ((1.0 + r) ** t)

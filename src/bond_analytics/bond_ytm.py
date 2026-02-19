from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class FixedRateBondYTM:
    """
    Simple fixed-rate bond priced with a single constant yield (YTM).
    This is a simplified framework (no curve, no dates).
    """
    face: float = 100.0
    coupon_rate: float = 0.05
    maturity_years: int = 5
    freq: int = 2

    def price_from_ytm(self, ytm: float) -> float:
        periods = self.maturity_years * self.freq
        coupon = self.face * self.coupon_rate / self.freq

        price = 0.0
        for t in range(1, periods + 1):
            price += coupon / ((1.0 + ytm / self.freq) ** t)

        price += self.face / ((1.0 + ytm / self.freq) ** periods)
        return price

    def ytm_from_price(self, price: float, tol: float = 1e-12, max_iter: int = 200) -> float:
        if price <= 0:
            raise ValueError("price must be positive")

        def f(y: float) -> float:
            return self.price_from_ytm(y) - price

        lo, hi = -0.99, 2.0
        f_lo, f_hi = f(lo), f(hi)
        if f_lo * f_hi > 0:
            raise ValueError("Root not bracketed for YTM. Check inputs.")

        for _ in range(max_iter):
            mid = 0.5 * (lo + hi)
            f_mid = f(mid)
            if abs(f_mid) < tol:
                return mid

            if f_lo * f_mid > 0:
                lo, f_lo = mid, f_mid
            else:
                hi, f_hi = mid, f_mid

        return 0.5 * (lo + hi)

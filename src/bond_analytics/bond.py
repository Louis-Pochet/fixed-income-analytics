from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from .schedule import coupon_schedule
from .daycount import year_fraction
from .curve import ZeroCurve


@dataclass(frozen=True)
class FixedRateBond:
    """
    Vanilla fixed-rate bond priced off a zero curve.

    settlement: pricing/settlement date (today)
    maturity: maturity date
    coupon_rate: annual coupon rate (0.05 = 5%)
    face: notional (100)
    freq: coupons per year (2 = semi-annual)
    day_count: day count convention for year fractions (kept simple for now)
    """
    settlement: date
    maturity: date
    coupon_rate: float
    face: float = 100.0
    freq: int = 2
    day_count: str = "ACT/365"

    def cashflows(self) -> list[tuple[date, float]]:
        """
        Generate dated cashflows (pay_date, amount) after settlement.
        Uses schedule.py to build coupon dates.
        """
        dates = coupon_schedule(self.settlement, self.maturity, self.freq)
        coupon = self.face * self.coupon_rate / self.freq

        cfs: list[tuple[date, float]] = []
        for d in dates:
            amt = coupon
            if d == self.maturity:
                amt += self.face
            cfs.append((d, amt))
        return cfs

    def price_from_curve(self, curve: ZeroCurve, z_spread: float = 0.0) -> float:
        """
        Price by discounting each cashflow using the curve discount factor.

        z_spread: constant spread added to the curve zero rate (simplified z-spread).
        """
        pv = 0.0
        for pay_date, cf in self.cashflows():
            t = year_fraction(curve.asof, pay_date, self.day_count)
            df = curve.df(t, z_spread=z_spread)
            pv += cf * df
        return pv

    def zspread_from_price(
        self,
        curve: ZeroCurve,
        market_price: float,
        lo: float = -0.05,
        hi: float = 0.20,
        tol: float = 1e-12,
        max_iter: int = 200,
    ) -> float:
        """
        Solve constant z-spread over the curve such that model price = market_price.
        Uses bisection (robust, no external dependencies).
        """
        if market_price <= 0:
            raise ValueError("market_price must be positive")

        def f(z: float) -> float:
            return self.price_from_curve(curve, z_spread=z) - market_price

        f_lo, f_hi = f(lo), f(hi)
        if f_lo * f_hi > 0:
            raise ValueError("Root not bracketed for z-spread. Widen lo/hi bounds.")

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

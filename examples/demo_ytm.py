from bond_analytics.bond_ytm import FixedRateBondYTM
from bond_analytics.risk_ytm import risk_from_ytm

bond = FixedRateBondYTM(
    face=100.0,
    coupon_rate=0.05,
    maturity_years=5,
    freq=2
)

ytm = 0.04
price = bond.price_from_ytm(ytm)
ytm_back = bond.ytm_from_price(price)

rm = risk_from_ytm(bond, ytm)

print("=== YTM framework ===")
print("Price:", price)
print("Recovered YTM:", ytm_back)
print("DV01:", rm.dv01)
print("Modified duration:", rm.modified_duration)
print("Convexity:", rm.convexity)

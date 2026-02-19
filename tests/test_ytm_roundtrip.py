from bond_analytics.bond_ytm import FixedRateBondYTM

def test_ytm_roundtrip():
    bond = FixedRateBondYTM(face=100.0, coupon_rate=0.05, maturity_years=5, freq=2)

    y = 0.04
    p = bond.price_from_ytm(y)
    y2 = bond.ytm_from_price(p)

    assert abs(y - y2) < 1e-10
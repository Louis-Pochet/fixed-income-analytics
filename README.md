# Fixed Income Analytics

This repository contains a small Python library implementing core fixed-income analytics for vanilla fixed-rate bonds.

The objective of this project is to demonstrate a clear understanding of bond pricing mechanics, yield curve discounting, spread analysis, and interest rate risk measures.

The implementation focuses on clarity, modularity, and financial correctness rather than production-level optimisation.

---

## Project Objective

This project was built to:

- Understand how bonds are priced under different frameworks
- Implement yield-based and curve-based pricing approaches
- Compute standard interest rate risk measures
- Solve for yield and z-spread using numerical methods
- Structure financial code in a clean and modular way

The goal is to bridge theoretical fixed-income concepts and practical Python implementation.

---

## Implemented Frameworks

### 1. Yield-to-Maturity (YTM) Framework

- Price from yield
- Solve yield from price (bisection method)
- DV01
- Modified duration
- Convexity

This framework uses a single constant yield and is useful for pedagogical and quick analytical purposes.

---

### 2. Zero-Curve Framework

- Cashflow schedule generation
- Discounting using a zero rate curve
- Z-spread solver
- Flat DV01
- Key rate DV01

This framework reflects more realistic market practice, where bonds are discounted using a term structure of interest rates rather than a single yield.

---

## Risk Measures

Risk metrics are computed using finite-difference bumping:

- DV01
- Modified duration
- Convexity
- Key rate DV01 (per curve node)

This allows sensitivity analysis consistent with trading desk methodologies.
# Fixed Income Analytics

A modular Python implementation of core fixed-rate bond analytics.

This project implements two pricing frameworks:

- Yield-to-Maturity (YTM) pricing  
- Zero-curve discounting with z-spread solver  

It also includes standard interest rate risk measures:
DV01, modified duration, convexity, and key rate DV01.

The objective is to demonstrate a clear understanding of bond pricing mechanics, yield curves, and spread analysis in a clean and structured codebase.

---

## Features

- Price from YTM  
- Solve YTM from price (bisection method)  
- Curve-based bond pricing  
- Z-spread solver  
- DV01 and key rate DV01  
- Modified duration and convexity  

---

## Project Structure

```
src/bond_analytics/
examples/
tests/
```

---

## Installation

```bash
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -e .
```

---

## Run Examples

```bash
python examples/demo_ytm.py
python examples/demo_curve_zspread.py
python examples/demo_key_rate_dv01.py
```

---

## Run Tests

```bash
python -m pytest -q
```

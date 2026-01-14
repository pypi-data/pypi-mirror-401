# piecewise-rational

Shape-preserving piecewise rational cubic interpolation using the Delbourgo-Gregory algorithm.

## Installation

```bash
pip install piecewise-rational
```

## Usage

```python
from piecewise_rational import rational_cubic_interpolation

# Interpolate at x=0.5 given endpoints and derivatives
x_l, x_r = 0.0, 1.0      # interval
y_l, y_r = 0.0, 1.0      # values at endpoints
d_l, d_r = 1.0, 1.0      # derivatives at endpoints
r = 0.0                   # control parameter

y = rational_cubic_interpolation(0.5, x_l, x_r, y_l, y_r, d_l, d_r, r)
```

## Features

- Shape-preserving interpolation (maintains monotonicity and convexity)
- Control parameters for fitting second derivatives
- High numerical precision

## References

- R. Delbourgo, J.A. Gregory, "Shape preserving piecewise rational interpolation",
  SIAM Journal on Scientific and Statistical Computing, 1985.
- Peter Jaeckel, "Let's Be Rational", www.jaeckel.org

## License

MIT License. Python implementation derived from Peter Jaeckel's LetsBeRational.

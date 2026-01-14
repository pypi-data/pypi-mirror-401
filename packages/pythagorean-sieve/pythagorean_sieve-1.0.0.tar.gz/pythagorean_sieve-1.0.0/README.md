# Pythagorean Sieve on r

A recursive modular sieve for odd prime numbers based on Pythagorean geometry.

This repository contains a reference implementation of the **Pythagorean sieve on the inradius index r**, introduced in:

> **R. Amato**,  
> *A Pythagorean Sieve and a Recursive Modular Characterization of Odd Primes*,  
> International Journal of Applied Mathematics, Vol. 38, No. 12s (2025).

The method provides:
- a geometric reinterpretation of divisibility via the identity `r = (x − d)/2`,
- a modular sieve equivalent to Eratosthenes’ sieve,
- an **ordered generator of odd primes**,
- direct computation of the *n*-th prime.
- Significantly reduced memory usage compared to classical array-based sieves, due to segmentation on the r-variable.

---

## Installation


pip install pythagorean-sieve

---

##  Usage

python
from pythagorean_sieve import primes_up_to, nth_prime

print(primes_up_to(100))
print(nth_prime(734))

---

##  Performance

For performance characteristics and quantitative benchmarks,
see [PERFORMANCE.md](PERFORMANCE.md).

---

## License

This project is distributed under a dual licensing model:

AGPL-3.0-or-later for academic and open-source use.

Commercial license available for proprietary or closed-source use.

See:

LICENSE

COMMERCIAL_LICENSE.md

---

## Commercial note

For commercial use or integration into proprietary software without disclosure obligations,
please contact:

Roberto Amato
📧 amato.roberto.py@gmail.com

---

## Contributions

Contributions are welcome only after signing a Contributor License Agreement (CLA).
See CLA.md and CONTRIBUTING.md.

---

## Citation

If you use this software in academic work, please cite the associated paper.

---
## FAQs

See [FAQ.md](FAQ.md) for frequently asked questions about theory, performance, and design choices.

---

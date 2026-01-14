# Frequently Asked Questions (FAQ)

## Is this method just another sieve?
The Pythagorean sieve is logically a sieve, but operationally it also acts as an ordered generator of odd prime numbers. Unlike classical sieves that mark composites in place, this method filters admissible indices r through modular constraints derived from Pythagorean geometry.

## Why does it use significantly less memory?
The algorithm works on the index r = (x-1)/2 and pre-filters admissible residue classes using a wheel structure (M_t, S_t). Only candidate positions are generated and tested, avoiding storage of large boolean arrays typical of classical sieves.

## Does this method improve the asymptotic distribution of primes compared to Gauss or the Prime Number Theorem?
No. The asymptotic density of primes produced by the method matches the classical laws of Gauss and Mertens. The contribution is constructive and structural, not asymptotic improvement.

## How does it differ from the Atkin–Bernstein sieve?
Atkin–Bernstein is optimized for speed using quadratic forms and heavy precomputation. The Pythagorean sieve emphasizes conceptual transparency, modular structure, and low memory usage, rather than raw speed.

## Can it compute the n-th prime directly?
Yes. Because surviving indices r are produced in strictly increasing order, the algorithm can stop once the n-th prime is reached, without precomputing all primes up to a fixed bound.

## Is the advantage mainly theoretical or practical?
Both. Theoretical advantages include a geometric reinterpretation of primality and a direct link to Pythagorean triples. Practically, the method reduces memory usage and supports direct computation of the n-th prime.

## Is this intended to replace classical sieves?
No. It is a complementary approach, offering a different perspective and useful properties (ordered generation, low memory), rather than a universal replacement.

## What is the role of geometry in the algorithm?
The key identity r = (x-d)/2 comes from the inradius of integer right triangles. Divisibility conditions translate into forbidden congruence classes for r, giving a geometric origin to the sieve.

## Is the algorithm deterministic and exact?
Yes. All eliminations are exact modular conditions. There are no probabilistic steps or heuristics.

## Why is AGPL used for the academic version?
AGPL ensures that improvements remain open in academic and open-source contexts, while allowing the author to offer separate commercial licenses for proprietary use.

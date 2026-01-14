from .sieve import primes_up_to_r_segmented, nth_prime_r

# User-friendly aliases
primes_up_to = primes_up_to_r_segmented
nth_prime = nth_prime_r

__all__ = [
    "primes_up_to",
    "nth_prime",
    "primes_up_to_r_segmented",
    "nth_prime_r",
]

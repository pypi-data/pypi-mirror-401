from math import isqrt

def small_primes_upto(n):
    """Small sieve generating primes <= n (for marking up to sqrt(X))."""
    if n < 2: return []
    m = n + 1
    is_comp = bytearray(m)
    is_comp[:2] = b'\x01\x01'
    for p in range(2, isqrt(n) + 1):
        if not is_comp[p]:
            start = p * p
            step = p
            is_comp[start:n+1:step] = b'\x01' * (((n - start)//step) + 1)
    return [i for i in range(2, n + 1) if not is_comp[i]]

def build_wheel(primes_for_wheel=(3,5,7,11)):
    """Fixed wheel on r: modulus W and allowed residues (exclude r ≡ (p-1)/2 mod p)."""
    W = 1
    for p in primes_for_wheel:
        W *= p
    allowed = []
    for r in range(W):
        ok = True
        for p in primes_for_wheel:
            if r % p == (p - 1)//2:
                ok = False
                break
        if ok:
            allowed.append(r)
    return W, allowed, primes_for_wheel[-1], tuple(primes_for_wheel)

def primes_up_to_r_segmented(X, segment_size=200_000, wheel_primes=(3,5,7,11)):
    """
    Primes <= X using the r-sieve:
    - fixed wheel (to skip forbidden r),
    - segmentation (RAM O(segment_size)),
    - mark multiples from p^2 onward (do not eliminate p itself).
    """
    if X < 2:
        return []

    out = []
    if X >= 2:
        out.append(2)

    # Fixed wheel on r
    W, allowed_residues, max_wheel_p, wheel_tuple = build_wheel(wheel_primes)

    # Explicitly add wheel primes (e.g., 3,5,7,11) if within X
    for bp in wheel_tuple:
        if bp <= X:
            out.append(bp)

    # Marking primes: p > max_wheel_p, up to sqrt(X)
    limit = isqrt(X)
    base_prs = small_primes_upto(limit)
    mark_primes = [p for p in base_prs if p > max_wheel_p]

    # r max for x <= X (x = 2r+1)
    r_max = (X - 1) // 2

    start_r = 0
    while start_r <= r_max:
        end_r = min(start_r + segment_size - 1, r_max)

        # Only r congruent to allowed residues mod W are mapped in this segment
        r_positions = []
        for a in allowed_residues:
            if a > end_r:
                continue
            k0 = (start_r - a + W - 1) // W  # first k with r=a+kW >= start_r
            r0 = a + k0 * W
            for r in range(r0, end_r + 1, W):
                r_positions.append(r)

        if not r_positions:
            start_r = end_r + 1
            continue

        m = len(r_positions)
        is_compact_comp = bytearray(m)  # 0 = potential prime, 1 = composite
        r_to_idx = {r: i for i, r in enumerate(r_positions)}

        # Mark multiples for p >= next wheel prime, starting at x=p^2 -> r_min=(p^2-1)//2
        for p in mark_primes:
            forb = (p - 1)//2
            r_min = (p*p - 1) // 2
            r_start = max(start_r, r_min)
            # first r >= r_start with r ≡ forb (mod p)
            t0 = (r_start - forb + p - 1) // p
            r_first = forb + t0 * p
            for r in range(r_first, end_r + 1, p):
                idx = r_to_idx.get(r)
                if idx is not None:
                    is_compact_comp[idx] = 1

        # Emit x=2r+1 not marked (and <= X)
        for idx, r in enumerate(r_positions):
            if not is_compact_comp[idx]:
                x = 2 * r + 1
                if x >= 3 and x <= X:
                    out.append(x)

        start_r = end_r + 1

    # Sort and deduplicate
    out.sort()
    dedup = []
    last = None
    for v in out:
        if v != last:
            dedup.append(v)
            last = v
    return dedup

def nth_prime_r(n, guess=5000):
    """n-th prime via r-sieve (double X until enough primes)."""
    if n < 1:
        raise ValueError("n must be >= 1")
    X = guess
    while True:
        ps = primes_up_to_r_segmented(X)
        if len(ps) >= n:
            return ps[n-1]
        X *= 2

"""
TAPS-MCC - cryptographic primitive benchmark
Measures the running time of every primitive used in Phase 2 (authentication)
and Phase 2.5 (Paillier data upload), then computes the cost of TAPS-MCC and
the baseline schemes from their operation counts.

Run on (a) the edge-server machine and (b) an Android phone (Termux + Python)
to obtain the ES-side and MU-side timings reported in the paper.

    pip install cryptography phe
    python taps_mcc_benchmark.py
"""
import hashlib, hmac, os, statistics, time, platform
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from phe import paillier

RUNS = 1000          # repetitions for fast operations
PAILLIER_RUNS = 50   # repetitions for Paillier operations


def bench(fn, runs):
    """Return mean running time in milliseconds."""
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        fn()
        times.append((time.perf_counter() - t0) * 1000)
    return statistics.mean(times)


# ---------- Primitive benchmarks ----------
curve = ec.SECP256R1()
priv = ec.generate_private_key(curve)
peer = ec.generate_private_key(curve).public_key()

def t_pm_fixed():          # a*P  (fixed-base point multiplication)
    ec.derive_private_key(int.from_bytes(os.urandom(31), "big") + 1, curve).public_key()

def t_pm_var():            # a*X  (variable-base point multiplication, ECDH)
    priv.exchange(ec.ECDH(), peer)

msg = os.urandom(128)
def t_h():                 # SHA-256
    hashlib.sha256(msg).digest()

key = os.urandom(32)
def t_hmac():              # HMAC-SHA256
    hmac.new(key, msg, hashlib.sha256).digest()

iv = os.urandom(16)
def t_sym():               # AES-256-CTR encryption of 128 bytes
    Cipher(algorithms.AES(key), modes.CTR(iv)).encryptor().update(msg)

results = {
    "T_pm (fixed-base a*P)": bench(t_pm_fixed, RUNS),
    "T_pm (variable-base a*X)": bench(t_pm_var, RUNS),
    "T_h (SHA-256)": bench(t_h, RUNS * 10),
    "T_hmac (HMAC-SHA256)": bench(t_hmac, RUNS * 10),
    "T_s (AES-256)": bench(t_sym, RUNS * 10),
}

for bits in (1024, 2048, 3072):
    pk, sk = paillier.generate_paillier_keypair(n_length=bits)
    c1, c2 = pk.encrypt(12345), pk.encrypt(67890)
    results[f"Paillier-{bits} Enc"] = bench(lambda: pk.encrypt(424242), PAILLIER_RUNS)
    results[f"Paillier-{bits} Dec"] = bench(lambda: sk.decrypt(c1), PAILLIER_RUNS)
    results[f"Paillier-{bits} Add (homomorphic)"] = bench(lambda: c1 + c2, PAILLIER_RUNS * 10)

print(f"Platform: {platform.processor() or platform.machine()} | Python {platform.python_version()}")
print(f"{'Operation':38s} {'Time (ms)':>10s}")
for k, v in results.items():
    print(f"{k:38s} {v:10.4f}")

# ---------- Scheme cost from operation counts ----------
Tpm = results["T_pm (variable-base a*X)"]   # conservative: use variable-base
Th = results["T_h (SHA-256)"]
Ts = results["T_s (AES-256)"]

schemes = {
    # name: ((user Tpm, Th, Ts), (server Tpm, Th, Ts))
    "Liu et al. 2023 [S1]":            ((3, 6, 1), (3, 4, 1)),
    "Appl. Sci. 2024 14:3187 [S2]":    ((3, 3, 0), (3, 3, 0)),
    "Sensors 2024 24:7967 [S3]":       ((2, 5, 0), (2, 5, 0)),
    "TAPS-MCC (full)":                 ((4, 11, 0), (4, 5, 0)),
    "TAPS-MCC (online, precomputed)":  ((2, 11, 0), (2, 5, 0)),
}

def cost(c):
    return c[0] * Tpm + c[1] * Th + c[2] * Ts

print(f"\n{'Scheme':34s} {'User (ms)':>10s} {'Server (ms)':>12s} {'Total (ms)':>11s}")
for name, (u, s) in schemes.items():
    print(f"{name:34s} {cost(u):10.3f} {cost(s):12.3f} {cost(u) + cost(s):11.3f}")

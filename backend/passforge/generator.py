"""Cryptographically secure password generation."""

from __future__ import annotations

import math
import secrets
import string

MIN_LENGTH = 12
MAX_LENGTH = 128


def generate_password(
    length: int,
    *,
    lowercase: bool = True,
    uppercase: bool = True,
    digits: bool = True,
    symbols: bool = True,
) -> str:
    """Generate a password using Python's cryptographically secure RNG."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("La longitud debe ser un número entero.")
    if length < MIN_LENGTH:
        length = MIN_LENGTH
    if length > MAX_LENGTH:
        raise ValueError(f"La longitud máxima es de {MAX_LENGTH} caracteres.")

    pools = []
    if lowercase:
        pools.append(string.ascii_lowercase)
    if uppercase:
        pools.append(string.ascii_uppercase)
    if digits:
        pools.append(string.digits)
    if symbols:
        pools.append(string.punctuation)
    if not pools:
        raise ValueError("Selecciona al menos un tipo de carácter.")

    if length < len(pools):
        raise ValueError("La longitud es demasiado corta para los tipos seleccionados.")

    characters = [secrets.choice(pool) for pool in pools]
    alphabet = "".join(pools)
    characters.extend(secrets.choice(alphabet) for _ in range(length - len(pools)))

    secrets.SystemRandom().shuffle(characters)
    return "".join(characters)


def estimate_entropy(length: int, alphabet_size: int) -> float:
    """Estimate password entropy in bits for display purposes."""
    if length <= 0 or alphabet_size <= 1:
        return 0.0
    return round(length * math.log2(alphabet_size), 1)


def estimate_exhaustive_years(
    entropy: float,
    guesses_per_second: int = 100_000_000_000,
) -> float:
    """Estimate a full keyspace search under an explicit attack assumption."""
    if entropy <= 0 or guesses_per_second <= 0:
        return 0.0
    try:
        seconds = math.pow(2.0, min(entropy, 1000.0)) / guesses_per_second
        return round(seconds / (60 * 60 * 24 * 365.25), 1)
    except OverflowError:
        return float("inf")

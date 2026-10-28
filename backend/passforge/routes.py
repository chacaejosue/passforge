"""HTTP routes for the PassForge API."""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from .generator import (
    MAX_LENGTH,
    MIN_LENGTH,
    estimate_entropy,
    estimate_exhaustive_years,
    generate_password,
)

api = Blueprint("api", __name__)


@api.get("/health")
def health():
    return jsonify(status="ok", service="passforge-api")


@api.route("/passwords", methods=["POST", "OPTIONS"])
def passwords():
    if request.method == "OPTIONS":
        return "", 204

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="El cuerpo debe ser un objeto JSON."), 400

    length = payload.get("length", 20)
    if isinstance(length, bool) or not isinstance(length, int):
        return jsonify(error="La longitud debe ser un número entero."), 400
    if length > MAX_LENGTH:
        return jsonify(error=f"La longitud máxima es de {MAX_LENGTH} caracteres."), 400

    options = {
        name: payload.get(name, True)
        for name in ("lowercase", "uppercase", "digits", "symbols")
    }
    if not all(isinstance(value, bool) for value in options.values()):
        return jsonify(error="Las opciones de caracteres deben ser booleanas."), 400
    if not any(options.values()):
        return jsonify(error="Selecciona al menos un tipo de carácter."), 400

    try:
        password = generate_password(length, **options)
    except (TypeError, ValueError):
        return jsonify(error="Parámetros de generación no válidos."), 400

    alphabet_size = sum(
        [
            26 if options["lowercase"] else 0,
            26 if options["uppercase"] else 0,
            10 if options["digits"] else 0,
            32 if options["symbols"] else 0,
        ]
    )
    entropy = estimate_entropy(len(password), alphabet_size)
    return jsonify(
        password=password,
        length=len(password),
        entropy=entropy,
        estimated_exhaustive_years=estimate_exhaustive_years(entropy),
        guesses_per_second=100_000_000_000,
        entropy_note="Estimación para una selección uniforme del alfabeto indicado.",
        minimum_length=MIN_LENGTH,
        maximum_length=MAX_LENGTH,
    )

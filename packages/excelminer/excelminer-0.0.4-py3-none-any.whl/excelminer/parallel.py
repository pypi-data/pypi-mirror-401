from __future__ import annotations

"""Parallelism helpers for tuning worker counts."""

from dataclasses import asdict, is_dataclass
import os
from typing import Any, Iterable

DEFAULT_MAX_WORKERS = 8
MIN_PARALLEL_WORKERS = 2
MEMORY_GB_PER_WORKER = 1.5


def resolve_parallelism(options: Any) -> None:
    """Fill in default worker counts based on host capabilities."""
    if getattr(options, "post_analysis_distillation", False) and getattr(
        options, "distillation_workers", None
    ) is None:
        options.distillation_workers = recommended_workers()

    if getattr(options, "include_formulas", False) and getattr(
        options, "formula_decomposition_workers", None
    ) is None:
        options.formula_decomposition_workers = recommended_workers()


def recommended_workers(*, cap: int = DEFAULT_MAX_WORKERS) -> int:
    """Return a safe worker count based on host CPU/memory."""
    specs = _load_host_specs()
    cpu_count = _coerce_int(_spec_value(specs, _CPU_KEYS)) or _default_cpu_count()
    memory_gb = _memory_gb_from_specs(specs)

    worker_cap = max(1, min(cpu_count, cap))
    if memory_gb is not None:
        mem_cap = max(1, int(memory_gb // MEMORY_GB_PER_WORKER))
        worker_cap = min(worker_cap, mem_cap)

    if worker_cap >= MIN_PARALLEL_WORKERS:
        return worker_cap
    return 1


_CPU_KEYS: tuple[str, ...] = (
    "cpu_count",
    "logical_cpus",
    "logical_cpu_count",
    "cpu_logical",
    "cpus",
    "num_cpus",
    "cores",
    "cpu_cores",
    "processor_count",
)

_MEM_GB_KEYS: tuple[str, ...] = (
    "memory_gb",
    "mem_gb",
    "ram_gb",
    "memory_total_gb",
)

_MEM_BYTES_KEYS: tuple[str, ...] = (
    "memory_bytes",
    "mem_bytes",
    "ram_bytes",
    "memory_total_bytes",
    "mem_total_bytes",
)


def _default_cpu_count() -> int:
    return max(1, os.cpu_count() or 1)


def _load_host_specs() -> Any | None:
    try:
        import hostxray  # type: ignore
    except Exception:
        return None

    for name in (
        "host_specs",
        "get_host_specs",
        "specs",
        "get_specs",
        "probe",
        "inspect",
    ):
        func = getattr(hostxray, name, None)
        if callable(func):
            try:
                return func()
            except Exception:
                continue

    for name in ("HostSpecs", "HostSpec"):
        cls = getattr(hostxray, name, None)
        factory = getattr(cls, "from_system", None) if cls is not None else None
        if callable(factory):
            try:
                return factory()
            except Exception:
                continue

    return None


def _spec_value(specs: Any, keys: Iterable[str]) -> Any | None:
    if specs is None:
        return None

    normalized = _normalize_specs(specs)
    if isinstance(normalized, dict):
        for key in keys:
            if key in normalized:
                return normalized[key]
    else:
        for key in keys:
            if hasattr(normalized, key):
                return getattr(normalized, key)
    return None


def _normalize_specs(specs: Any) -> Any:
    if isinstance(specs, dict):
        return specs
    if is_dataclass(specs):
        return asdict(specs)
    to_dict = getattr(specs, "to_dict", None)
    if callable(to_dict):
        try:
            return to_dict()
        except Exception:
            return specs
    return specs


def _memory_gb_from_specs(specs: Any) -> float | None:
    mem_gb = _spec_value(specs, _MEM_GB_KEYS)
    mem_bytes = _spec_value(specs, _MEM_BYTES_KEYS)

    if mem_gb is not None:
        return _coerce_float(mem_gb)
    if mem_bytes is not None:
        mem_bytes_val = _coerce_float(mem_bytes)
        if mem_bytes_val is None:
            return None
        return mem_bytes_val / (1024**3)
    return None


def _coerce_int(value: Any) -> int | None:
    if value is None:
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(float(value.strip()))
        except Exception:
            return None
    return None


def _coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.strip().lower().replace("gb", "").replace(",", "")
        try:
            return float(cleaned)
        except Exception:
            return None
    return None

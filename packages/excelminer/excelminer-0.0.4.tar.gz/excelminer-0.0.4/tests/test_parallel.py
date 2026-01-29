from __future__ import annotations

import sys
from types import ModuleType

from excelminer.backends.base import AnalysisOptions
from excelminer.parallel import recommended_workers, resolve_parallelism


def test_resolve_parallelism_sets_defaults(monkeypatch) -> None:
    def _fake_recommended_workers(*, cap: int = 8) -> int:
        return 4

    monkeypatch.setattr(
        "excelminer.parallel.recommended_workers", _fake_recommended_workers
    )

    options = AnalysisOptions(
        include_formulas=True,
        post_analysis_distillation=True,
    )

    resolve_parallelism(options)

    assert options.distillation_workers == 4
    assert options.formula_decomposition_workers == 4


def test_resolve_parallelism_respects_explicit_workers() -> None:
    options = AnalysisOptions(
        include_formulas=True,
        post_analysis_distillation=True,
        distillation_workers=1,
        formula_decomposition_workers=2,
    )

    resolve_parallelism(options)

    assert options.distillation_workers == 1
    assert options.formula_decomposition_workers == 2


def test_recommended_workers_uses_hostxray_specs(monkeypatch) -> None:
    module = ModuleType("hostxray")

    def _host_specs():
        return {"cpu_count": 16, "memory_gb": 3.0}

    module.host_specs = _host_specs
    monkeypatch.setitem(sys.modules, "hostxray", module)

    assert recommended_workers() == 2

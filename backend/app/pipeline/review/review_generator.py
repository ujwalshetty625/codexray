import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def generate_review(
    repo_id: str,
    files: list[dict],
    edges: list[dict],
    architecture: dict,
) -> dict:
    language_counts = _count_languages(files)
    total_files     = len(files)
    total_deps      = len(edges)
    arch_type       = architecture.get("architecture", "Unknown")
    confidence      = architecture.get("confidence", 0.0)

    summary    = _build_summary(arch_type, confidence, total_files, total_deps, language_counts)
    strengths  = _build_strengths(arch_type, total_files, total_deps, language_counts)
    weaknesses = _build_weaknesses(arch_type, total_files, total_deps, language_counts)
    suggestions = _build_suggestions(arch_type, total_files, total_deps, language_counts)

    logger.info("Generated engineering review for repo '%s'.", repo_id)

    return {
        "summary":     summary,
        "strengths":   strengths,
        "weaknesses":  weaknesses,
        "suggestions": suggestions,
    }


def _count_languages(files: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for f in files:
        lang = f.get("language", "Unknown")
        if lang and lang != "Unknown":
            counts[lang] = counts.get(lang, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def _build_summary(
    arch_type: str,
    confidence: float,
    total_files: int,
    total_deps: int,
    language_counts: dict[str, int],
) -> str:
    primary_lang = next(iter(language_counts), "unknown")
    lang_count   = len(language_counts)
    conf_pct     = int(confidence * 100)

    if arch_type == "Unknown":
        arch_desc = "a custom or non-standard architecture"
    else:
        arch_desc = f"a {arch_type} architecture (confidence: {conf_pct}%)"

    return (
        f"This repository appears to follow {arch_desc}. "
        f"It consists of {total_files} indexed files primarily written in {primary_lang}, "
        f"spanning {lang_count} detected language{'s' if lang_count != 1 else ''}. "
        f"The dependency graph contains {total_deps} relationships, "
        f"{'suggesting a highly interconnected codebase' if total_deps > 200 else 'indicating a relatively contained module structure'}."
    )


def _build_strengths(
    arch_type: str,
    total_files: int,
    total_deps: int,
    language_counts: dict[str, int],
) -> list[str]:
    strengths = []

    if arch_type in ("MVC", "Layered"):
        strengths.append("Clear separation of concerns — architecture follows established layering conventions.")

    if arch_type == "Microservices":
        strengths.append("Service boundaries appear well-defined, supporting independent deployability.")

    if len(language_counts) == 1:
        strengths.append(f"Single-language codebase ({next(iter(language_counts))}) reduces cognitive overhead and toolchain complexity.")

    if total_files < 100:
        strengths.append("Small, focused codebase — likely easier to onboard new contributors.")

    if total_deps > 0 and total_files > 0:
        ratio = total_deps / total_files
        if ratio < 3:
            strengths.append("Low average dependency ratio per file suggests loosely coupled modules.")

    if arch_type in ("Serverless", "Event-Driven"):
        strengths.append("Architecture is well-suited for scalability and async workloads.")

    if not strengths:
        strengths.append("Codebase is structured and indexable — no critical structural anomalies detected.")

    return strengths


def _build_weaknesses(
    arch_type: str,
    total_files: int,
    total_deps: int,
    language_counts: dict[str, int],
) -> list[str]:
    weaknesses = []

    if total_files > 500:
        weaknesses.append("Large file count may indicate insufficient modularization or accumulation of legacy code.")

    if total_deps > 0 and total_files > 0:
        ratio = total_deps / total_files
        if ratio > 6:
            weaknesses.append("High dependency ratio per file suggests potential tight coupling between modules.")

    if len(language_counts) > 4:
        weaknesses.append(
            f"Codebase spans {len(language_counts)} languages — polyglot complexity can increase maintenance burden."
        )

    if arch_type == "Unknown":
        weaknesses.append("No standard architectural pattern detected — structure may be inconsistent or organically grown.")

    if arch_type == "Monolithic" and total_files > 200:
        weaknesses.append("Monolithic structure at scale can make independent deployment and testing difficult.")

    if total_deps == 0 and total_files > 10:
        weaknesses.append("No dependencies detected — parser may have limited coverage, or files may lack standard import patterns.")

    if not weaknesses:
        weaknesses.append("No critical weaknesses detected from structural analysis alone.")

    return weaknesses


def _build_suggestions(
    arch_type: str,
    total_files: int,
    total_deps: int,
    language_counts: dict[str, int],
) -> list[str]:
    suggestions = []

    if arch_type == "Monolithic" and total_files > 150:
        suggestions.append("Consider extracting cohesive domains into separate packages or services to improve maintainability.")

    if arch_type == "Unknown":
        suggestions.append("Introduce a consistent directory structure (e.g. src/, tests/, docs/) to signal architectural intent.")

    if total_deps > 0 and total_files > 0 and (total_deps / total_files) > 6:
        suggestions.append("Review high-dependency files for opportunities to extract shared abstractions or utility modules.")

    if len(language_counts) > 3:
        suggestions.append("Evaluate whether all detected languages are necessary — reducing language count simplifies CI/CD and onboarding.")

    if "Markdown" not in language_counts and total_files > 20:
        suggestions.append("No Markdown files detected — adding README and documentation files improves project discoverability.")

    if arch_type in ("MVC", "Layered"):
        suggestions.append("Ensure test coverage mirrors the layer structure — unit tests per layer, integration tests across layers.")

    if arch_type == "Microservices":
        suggestions.append("Verify each service has its own test suite and can be deployed independently without shared state.")

    suggestions.append("Run dependency graph analysis periodically to detect emerging coupling hotspots early.")

    return suggestions
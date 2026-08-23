def check_route(
    expected_route: str,
    actual_route: str,
):
    passed = actual_route == expected_route

    if passed:
        message = "Route matched"
    else:
        message = f"Expected route {expected_route}, got {actual_route}"

    return {
        "passed": passed,
        "expected": expected_route,
        "actual": actual_route,
        "message": message,
    }


def check_requires_database(
    expected_requires_database: bool,
    actual_requires_database: bool,
):
    passed = actual_requires_database == expected_requires_database

    if passed:
        message = "Requires database matched"
    else:
        message = f"Expected requires database {expected_requires_database}, got {actual_requires_database}"

    return {
        "passed": passed,
        "expected": expected_requires_database,
        "actual": actual_requires_database,
        "message": message,
    }


def check_answer_mentions(
    expected_terms: list[str],
    actual_answer: str,
):
    passed = all(
        term.lower() in actual_answer.lower()
        for term in expected_terms
    )

    if passed:
        message = f"Answer mentions all of {expected_terms}"
    else:
        message = f"Answer does not mention all of {expected_terms}"

    return {
        "passed": passed,
        "expected": expected_terms,
        "actual": actual_answer,
        "message": message,
    }


def check_answer_mentions_any(
    expected_terms: list[str],
    actual_answer: str,
):
    passed = any(
        term.lower() in actual_answer.lower()
        for term in expected_terms
    )

    if passed:
        message = f"Answer mentions at least one of the terms in {expected_terms}"
    else:
        message = f"Answer does not mention any of {expected_terms}"

    return {
        "passed": passed,
        "expected": expected_terms,
        "actual": actual_answer,
        "message": message,
    }


def check_sources(
    expected_sources: list[str],
    actual_sources: list[str],
):
    passed = expected_sources == actual_sources

    if passed:
        message = f"Actual sources match {expected_sources}"
    else:
        message = f"Actual sources does not match {expected_sources}"

    return {
        "passed": passed,
        "expected": expected_sources,
        "actual": actual_sources,
        "message": message,
    }


def check_sources_contains(
    expected_source: str,
    actual_sources: list[str],
):
    passed = expected_source in actual_sources

    if passed:
        message = f"Actual sources contains {expected_source}"
    else:
        message = f"Actual sources does not contains {expected_source}"

    return {
        "passed": passed,
        "expected": expected_source,
        "actual": actual_sources,
        "message": message,
    }
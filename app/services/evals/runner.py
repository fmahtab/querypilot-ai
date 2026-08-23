import json

from pathlib import Path

from app.services.reasoning import ReasoningService
from app.services.evals.assertions import (
    check_route,
    check_requires_database, 
    check_answer_mentions,
    check_answer_mentions_any,
    check_sources_contains,
    check_sources
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
GOLDEN_SET_PATH = PROJECT_ROOT / "data" / "evals" / "querypilot_golden_set.json"

def load_golden_set():
    with open(GOLDEN_SET_PATH, "r", encoding="utf-8") as file:
        golden_set = json.load(file)

    return golden_set

if __name__ == "__main__":
    golden_set = load_golden_set()
    service = ReasoningService()
    passed_cases = 0
    for case in golden_set:
        case_results = []
        question = case["question"]
        expected_route = case["expected_route"]
        expected_behavior = case["expected_behavior"]

        # Evaluate routing
        actual_route = service._classify_question(question)

        route_result = check_route(
            expected_route,
            actual_route
        )
        case_results.append(route_result)

        # Actually ask QueryPilot the question
        response = service.answer_question(question)

        # Evaluate the database flag
        requires_database_result = check_requires_database(
            expected_behavior["requires_database"],
            response.requires_database
        )
        
        case_results.append(requires_database_result)
        

        # Evaluate the answer mentions
        if "answer_mentions" in expected_behavior:
            expected_terms = expected_behavior["answer_mentions"]

            answer_result = check_answer_mentions(
                expected_terms,
                response.answer
            )
    
            case_results.append(answer_result)

            
        # Evaluate the answer_mentions_any
        if "answer_mentions_any" in expected_behavior:
            expected_terms = expected_behavior["answer_mentions_any"]

            answer_any_result = check_answer_mentions_any(
                expected_terms,
                response.answer
            )
            case_results.append(answer_any_result)


        # Evaluate the sources_contains
        if "sources_contains" in expected_behavior:

            sources_contains_result = check_sources_contains(
                expected_behavior["sources_contains"],
                response.sources
            )
            case_results.append(sources_contains_result)
        

        # Evaluate the sources
        if "sources" in expected_behavior:

            sources_result = check_sources(
                expected_behavior["sources"],
                response.sources
            )
            case_results.append(sources_result)

    
        case_passed = all(
            result["passed"] for result in case_results
        )

        if case_passed:
            passed_cases += 1
            print(f"PASS | {question}")
        else:
            print(f"FAIL | {question}")

            for result in case_results:
                if not result["passed"]:
                    print(f"  - {result['message']}")


    score = passed_cases / len(golden_set) * 100
    print("\nSummary")
    print(f"Passed cases: {passed_cases}/{len(golden_set)}")
    print(f"Score: {score:.1f}%")    
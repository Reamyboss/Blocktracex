def calculate_score(passed: int, failed: int) -> int:
    """
    Calculate the overall project health score.
    """

    total = passed + failed

    if total == 0:
        return 0

    score = (passed / total) * 100

    return round(score)

from typing import List

def is_safe(report: List[int]) -> bool:
    differences = [report[i + 1] - report[i] for i in range(0, len(report) - 1)]
    all_increasing_safely = len([diff for diff in differences if diff >= 1 and diff <= 3 ]) == len(differences)
    if all_increasing_safely:
        return True

    all_decreasing_safely = len([diff for diff in differences if diff <= -1 and diff >= -3 ]) == len(differences)
    return all_decreasing_safely

from loader import input_as_ints

if __name__ == "__main__":
    input = input_as_ints(__file__)

    safe_reports = 0
    for report in input:
        differences = [report[i + 1] - report[i] for i in range(0, len(report) - 1)]
        all_increasing_safely = len([diff for diff in differences if diff >= 1 and diff <= 3 ]) == len(differences)
        all_decreasing_safely = len([diff for diff in differences if diff <= -1 and diff >= -3 ]) == len(differences)

        if all_increasing_safely or all_decreasing_safely:
            safe_reports = safe_reports + 1

    print(safe_reports)


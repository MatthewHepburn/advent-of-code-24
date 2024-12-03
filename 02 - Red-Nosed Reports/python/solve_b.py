from loader import input_as_ints
from common import is_safe

if __name__ == "__main__":
    input = input_as_ints()

    safe_reports = 0
    for report in input:
        if is_safe(report):
            safe_reports = safe_reports + 1
            continue

        # Can we make it safe?
        for i in range (0, len(report)):
            report_copy = report[:]
            report_copy.pop(i)
            if is_safe(report_copy):
                safe_reports = safe_reports + 1
                break

    print(safe_reports)


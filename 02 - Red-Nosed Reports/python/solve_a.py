from loader import input_as_ints
from common import is_safe

if __name__ == "__main__":
    input = input_as_ints()

    safe_reports = 0
    for report in input:
        if is_safe(report):
            safe_reports = safe_reports + 1

    print(safe_reports)


def appearance(intervals: dict[str, list[int]]) -> int:
    def parse_intervals(times: list[int]) -> list[tuple[int, int]]:
        """Converts a list of timestamps into a list of (start, end) intervals."""
        return [(times[i], times[i + 1]) for i in range(0, len(times), 2)]

    def intersect(interval1: tuple[int, int], interval2: tuple[int, int]) -> tuple[int, int] | None:
        """Returns the intersection of two intervals or None if there is no intersection."""
        start = max(interval1[0], interval2[0])
        end = min(interval1[1], interval2[1])
        if start < end:
            return (start, end)
        return None

    def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """Merges overlapping intervals within a list."""
        if not intervals:
            return []
        intervals.sort()
        merged = [intervals[0]]
        for current in intervals[1:]:
            last_start, last_end = merged[-1]
            current_start, current_end = current
            if current_start <= last_end:
                merged[-1] = (last_start, max(last_end, current_end))
            else:
                merged.append(current)
        return merged

    def get_total_overlap(intervals1: list[tuple[int, int]], intervals2: list[tuple[int, int]]) -> int:
        """Finds the total overlap time between two lists of intervals."""
        i, j = 0, 0
        total = 0
        while i < len(intervals1) and j < len(intervals2):
            a_start, a_end = intervals1[i]
            b_start, b_end = intervals2[j]

            # Find the intersection of the current intervals
            start = max(a_start, b_start)
            end = min(a_end, b_end)
            if start < end:
                total += end - start

            # Move the pointer that ends first
            if a_end < b_end:
                i += 1
            else:
                j += 1
        return total

    # Parse the intervals
    lesson_start, lesson_end = intervals['lesson']
    lesson_interval = (lesson_start, lesson_end)

    pupil_intervals = parse_intervals(intervals['pupil'])
    tutor_intervals = parse_intervals(intervals['tutor'])

    # Limit the intervals to the lesson time
    def limit_intervals(intervals: list[tuple[int, int]], limit: tuple[int, int]) -> list[tuple[int, int]]:
        """Limits intervals to the given limit (lesson time)."""
        limited = []
        for start, end in intervals:
            intersection = intersect((start, end), limit)
            if intersection:
                limited.append(intersection)
        return limited

    pupil_limited = limit_intervals(pupil_intervals, lesson_interval)
    tutor_limited = limit_intervals(tutor_intervals, lesson_interval)

    # Merge overlapping intervals within each list
    pupil_merged = merge_intervals(pupil_limited)
    tutor_merged = merge_intervals(tutor_limited)

    # Compute the total overlap time
    total_time = get_total_overlap(pupil_merged, tutor_merged)

    return total_time

tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
             'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
             'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
    },
    {'intervals': {'lesson': [1594702800, 1594706400],
             'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564, 1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096, 1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500, 1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
             'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
    'answer': 3577
    },
    {'intervals': {'lesson': [1594692000, 1594695600],
             'pupil': [1594692033, 1594696347],
             'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
    'answer': 3565
    },
]

if __name__ == '__main__':
   for i, test in enumerate(tests):
       test_answer = appearance(test['intervals'])
       assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
   print("Все тесты пройдены успешно!")

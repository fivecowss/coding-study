"""
Week 4 Day 3: Intervals and Greedy Patterns

"""


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:

    # TODO:
    # 1. if intervals is empty, return []
    # 2. sort intervals by start time
    # 3. initialize merged = []
    # 4. loop through intervals
    # 5. if merged is empty or current interval does not overlap, append it
    # 6. otherwise, extend the last merged interval
    if not intervals:
        return []
    intervals.sort(key = lambda x: x[0])
    merged = []
    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])


def insert_interval(
    intervals: list[list[int]],
    new_interval: list[int],
) -> list[list[int]]:
    # TODO:
    # 1. initialize result = []
    # 2. loop over intervals by index
    # 3. if current interval is completely before new_interval, append current
    # 4. if current interval is completely after new_interval, append new_interval and the rest
    # 5. if overlap exists, update new_interval start/end
    # 6. after loop, append new_interval
    result = []
    for interval in intervals:
        if interval[1] < new_interval[0]:
            result.append(interval)
        elif interval[1] >= new_interval[0] and interval[0] <= new_interval[1]:
            new_interval[0] = min(interval[0], new_interval[0])
            new_interval[1] = max(interval[1], new_interval[1])
        else:
            result.append(new_interval)
            new_interval = interval
    result.append(new_interval)
    return result

def erase_overlap_intervals(intervals: list[list[int]]) -> int:
   
    # TODO:
    # 1. if intervals is empty, return 0
    # 2. sort intervals by end time
    # 3. initialize removed = 0
    # 4. initialize current_end as first interval end
    # 5. scan remaining intervals
    # 6. if start < current_end, increment removed
    # 7. else update current_end
    if not intervals:
        return 0
    intervals.sort(key = lambda x: x[1])
    removed = 0
    current_end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] < current_end:
            removed += 1
        else:
            current_end = intervals[i][1]
    return removed


def can_attend_meetings(intervals: list[list[int]]) -> bool:

    # TODO:
    # 1. sort intervals by start time
    # 2. compare adjacent intervals
    # 3. if current start < previous end, return False
    # 4. otherwise return True
    intervals.sort(key = lambda x: x[0])
    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i-1][1]:
            return False
    return True


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    # TODO:
    # 1. handle empty input
    # 2. create sorted starts
    # 3. create sorted ends
    # 4. use two pointers over starts and ends
    # 5. count active rooms
    # 6. track max rooms
    if not intervals:
        return 0
    starts = sorted(interval[0] for interval in intervals)
    ends = sorted(interval[1] for interval in intervals)
    s = 0
    e = 0
    rooms = 0
    max_rooms = 0

    while s < len(intervals):
        if starts[s] < ends[e]:
            rooms += 1
            max_rooms = max(max_rooms, rooms)
            s += 1
        else:
            rooms -= 1
            e += 1
    return max_rooms


def main() -> None:
    print("TODO 1: merge_intervals")
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))

    print("\nTODO 2: insert_interval")
    print(insert_interval([[1, 3], [6, 9]], [2, 5]))

    print("\nTODO 3: erase_overlap_intervals")
    print(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))

    print("\nTODO 4: can_attend_meetings")
    print(can_attend_meetings([[0, 30], [5, 10], [15, 20]]))

    print("\nTODO 5: min_meeting_rooms")
    print(min_meeting_rooms([[0, 30], [5, 10], [15, 20]]))


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
#     if not intervals:
#         return []
#
#     intervals.sort(key=lambda x: x[0])
#     merged = []
#
#     for start, end in intervals:
#         if not merged or start > merged[-1][1]:
#             merged.append([start, end])
#         else:
#             merged[-1][1] = max(merged[-1][1], end)
#
#     return merged
#
#
# def insert_interval(
#     intervals: list[list[int]],
#     new_interval: list[int],
# ) -> list[list[int]]:
#     result = []
#
#     for i, interval in enumerate(intervals):
#         start, end = interval
#         new_start, new_end = new_interval
#
#         if end < new_start:
#             result.append(interval)
#         elif start > new_end:
#             result.append(new_interval)
#             return result + intervals[i:]
#         else:
#             new_interval = [
#                 min(start, new_start),
#                 max(end, new_end),
#             ]
#
#     result.append(new_interval)
#     return result
#
#
# def erase_overlap_intervals(intervals: list[list[int]]) -> int:
#     if not intervals:
#         return 0
#
#     intervals.sort(key=lambda x: x[1])
#     removed = 0
#     current_end = intervals[0][1]
#
#     for start, end in intervals[1:]:
#         if start < current_end:
#             removed += 1
#         else:
#             current_end = end
#
#     return removed
#
#
# def can_attend_meetings(intervals: list[list[int]]) -> bool:
#     intervals.sort(key=lambda x: x[0])
#
#     for i in range(1, len(intervals)):
#         prev_end = intervals[i - 1][1]
#         cur_start = intervals[i][0]
#
#         if cur_start < prev_end:
#             return False
#
#     return True
#
#
# def min_meeting_rooms(intervals: list[list[int]]) -> int:
#     if not intervals:
#         return 0
#
#     starts = sorted(interval[0] for interval in intervals)
#     ends = sorted(interval[1] for interval in intervals)
#
#     s = 0
#     e = 0
#     rooms = 0
#     max_rooms = 0
#
#     while s < len(intervals):
#         if starts[s] < ends[e]:
#             rooms += 1
#             max_rooms = max(max_rooms, rooms)
#             s += 1
#         else:
#             rooms -= 1
#             e += 1
#
#     return max_rooms
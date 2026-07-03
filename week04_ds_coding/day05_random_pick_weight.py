import random


class WeightedPicker:
    def __init__(self, weights: list[int]):
        """
        Task:
        Build prefix sums.

        Example:
            weights = [1, 3, 2]
            prefix = [1, 4, 6]

        Direction:
        - Initialize self.prefix = []
        - Keep running total.
        - Append running total after each weight.
        """
        # TODO:
        # 1. initialize self.prefix
        # 2. initialize total = 0
        # 3. loop through weights
        # 4. update total
        # 5. append total to self.prefix
        # 6. store self.total
        self.prefix = []
        total = 0
        for weight in weights:
            total += weight
            self.prefix.append(total)
        self.total = total

    def pick_index(self) -> int:
        """
        Task:
        Randomly pick an index according to weights.

        Direction:
        - Generate target between 1 and self.total.
        - Binary search for the first prefix value >= target.
        - Return that index.

        Binary search target:
            first i such that self.prefix[i] >= target
        """
        # TODO:
        # 1. target = random.randint(1, self.total)
        # 2. binary search over self.prefix
        # 3. return leftmost index where prefix[index] >= target
        target = random.randint(1, self.total)
        left = 0
        right = len(self.prefix) - 1
        answer = -1
        while left <= right:
            mid = (left + right) // 2
            if self.prefix[mid] >= target:
                answer = mid
                right = mid - 1
            else:
                left = mid + 1
        return answer


def simulate_picker(weights: list[int], n_sim: int = 10_000) -> dict[int, int]:
    """
    Task:
    Simulate many weighted picks and count selected indices.

    Direction:
    - Create WeightedPicker.
    - Repeat n_sim times.
    - Count selected indices in a dictionary.

    Expected:
        weights = [1, 3, 2]
        index 0 around 1/6 of picks
        index 1 around 3/6 of picks
        index 2 around 2/6 of picks
    """
    # TODO:
    # 1. create picker
    # 2. initialize counts dict
    # 3. repeat n_sim times
    # 4. pick index
    # 5. update count
    # 6. return counts
    picker = WeightedPicker(weights)
    counts = {}
    for _ in range(n_sim):
        idx = picker.pick_index()
        counts[idx] = counts.get(idx, 0) + 1
        return counts


def main() -> None:
    random.seed(42)

    picker = WeightedPicker([1, 3, 2])
    print("Prefix sums:", picker.prefix)
    print("One pick:", picker.pick_index())

    counts = simulate_picker([1, 3, 2], n_sim=10_000)
    print("Simulation counts:", counts)

    print("Implement TODO functions, then uncomment blocks in main().")


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# class WeightedPicker:
#     def __init__(self, weights: list[int]):
#         self.prefix = []
#         total = 0
#
#         for weight in weights:
#             total += weight
#             self.prefix.append(total)
#
#         self.total = total
#
#     def pick_index(self) -> int:
#         target = random.randint(1, self.total)
#
#         left = 0
#         right = len(self.prefix) - 1
#         answer = -1
#
#         while left <= right:
#             mid = (left + right) // 2
#
#             if self.prefix[mid] >= target:
#                 answer = mid
#                 right = mid - 1
#             else:
#                 left = mid + 1
#
#         return answer
#
#
# def simulate_picker(weights: list[int], n_sim: int = 10_000) -> dict[int, int]:
#     picker = WeightedPicker(weights)
#     counts = {}
#
#     for _ in range(n_sim):
#         idx = picker.pick_index()
#         counts[idx] = counts.get(idx, 0) + 1
#
#     return counts
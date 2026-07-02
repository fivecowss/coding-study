import random


def estimate_two_heads(n_sim: int = 100_000) -> float:
    # TODO:
    # 1. initialize count = 0
    # 2. repeat n_sim times
    # 3. simulate two coin flips
    # 4. if both are heads, increment count
    # 5. return count / n_sim
    count = 0
    n_sim = 100_000
    for _ in range(n_sim):
        coin1 = random.choice([0,1])
        coin2 = random.choice([0,1])
        if coin1 == 1 and coin2 == 1:
            count += 1
    return count / n_sim


def estimate_dice_sum_at_least_8(n_sim: int = 100_000) -> float:
    # TODO:
    # 1. initialize count
    # 2. simulate two dice
    # 3. check if sum >= 8
    # 4. return estimated probability
    count = 0
    for _ in range(n_sim):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        if die1 + die2 >= 8:
            count += 1
    return count / n_sim


def estimate_conditional_probability(n_sim: int = 100_000) -> float:

    # TODO:
    # 1. initialize numerator = 0
    # 2. initialize denominator = 0
    # 3. simulate two dice
    # 4. if condition B holds, increment denominator
    # 5. inside that block, if condition A holds, increment numerator
    # 6. return numerator / denominator
    numerator = 0
    denominator = 0

    for _ in range(n_sim):
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)

        if dice1 + dice2 >= 8:
            denominator += 1
            if dice1 == 6:
                numerator += 1

    return numerator / denominator


def simulate_bernoulli_sample_mean(
    p: float = 0.3,
    sample_size: int = 100,
    n_sim: int = 10_000,
) -> list[float]:

    # TODO:
    # 1. initialize sample_means = []
    # 2. outer loop over n_sim
    # 3. inner loop over sample_size
    # 4. generate 0/1 Bernoulli outcomes
    # 5. compute mean of the sample
    # 6. append to sample_means
    # 7. return sample_means
    sample_means = []
    for _ in range(n_sim):
        sample = []
        for _ in range(sample_size):
            if random.random() < p:
                sample.append(1)
            else:
                sample.append(0)
        sample_means.append(sum(sample) / sample_size)
    return sample_means


def main() -> None:
    random.seed(42)

    print("TODO 1: P(two heads)")
    print(estimate_two_heads(10_000))

    print("\nTODO 2: P(dice sum >= 8)")
    print(estimate_dice_sum_at_least_8(10_000))

    print("\nTODO 3: P(die1 = 6 | sum >= 8)")
    print(estimate_conditional_probability(10_000))

    print("\nTODO 4: Bernoulli sample means")
    means = simulate_bernoulli_sample_mean(p=0.3, sample_size=100, n_sim=1000)
    print(means[:10])


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# def estimate_two_heads(n_sim: int = 100_000) -> float:
#     count = 0
#
#     for _ in range(n_sim):
#         coin1 = random.choice([0, 1])
#         coin2 = random.choice([0, 1])
#
#         if coin1 == 1 and coin2 == 1:
#             count += 1
#
#     return count / n_sim
#
#
# def estimate_dice_sum_at_least_8(n_sim: int = 100_000) -> float:
#     count = 0
#
#     for _ in range(n_sim):
#         die1 = random.randint(1, 6)
#         die2 = random.randint(1, 6)
#
#         if die1 + die2 >= 8:
#             count += 1
#
#     return count / n_sim
#
#
# def estimate_conditional_probability(n_sim: int = 100_000) -> float:
#     numerator = 0
#     denominator = 0
#
#     for _ in range(n_sim):
#         die1 = random.randint(1, 6)
#         die2 = random.randint(1, 6)
#
#         if die1 + die2 >= 8:
#             denominator += 1
#
#             if die1 == 6:
#                 numerator += 1
#
#     return numerator / denominator
#
#
# def simulate_bernoulli_sample_mean(
#     p: float = 0.3,
#     sample_size: int = 100,
#     n_sim: int = 10_000,
# ) -> list[float]:
#     sample_means = []
#
#     for _ in range(n_sim):
#         sample = []
#
#         for _ in range(sample_size):
#             if random.random() < p:
#                 sample.append(1)
#             else:
#                 sample.append(0)
#
#         sample_means.append(sum(sample) / sample_size)
#
#     return sample_means
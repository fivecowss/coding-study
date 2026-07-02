import random
import statistics


def compute_basic_summary(data: list[float]) -> dict[str, float]:

    # TODO:
    # 1. compute mean
    # 2. compute sample variance
    # 3. compute sample standard deviation
    # 4. compute population variance
    # 5. compute population standard deviation
    # 6. return dictionary
    return {
        "mean": statistics.mean(data),
        "sample_variance": statistics.variance(data),
        "sample_stdev": statistics.stdev(data),
        "population_variance": statistics.pvariance(data),
        "population_stdev": statistics.pstdev(data),
    }


def manual_mean(data: list[float]) -> float:
    # TODO: compute mean manually
    return sum(data) / len(data)


def manual_sample_variance(data: list[float]) -> float:

    # TODO:
    # 1. compute mean
    # 2. compute squared deviations
    # 3. divide by n - 1
    xbar = manual_mean(data)
    squared_deviations = [(x - xbar) ** 2 for x in data]
    return sum(squared_deviations) / (len(data) - 1)



def bootstrap_means(
    data: list[float],
    n_boot: int = 1000,
) -> list[float]:

    # TODO:
    # 1. initialize means = []
    # 2. repeat n_boot times
    # 3. create bootstrap sample with replacement
    # 4. compute sample mean
    # 5. append mean
    # 6. return means
    means = []
    for _ in range(n_boot):
        sample = random.choices(data, k = len(data))
        means.append(sum(sample) / len(sample))
    return means


def percentile_interval(
    values: list[float],
    lower: float = 0.025,
    upper: float = 0.975,
) -> tuple[float, float]:
  
    # TODO:
    # 1. sort values
    # 2. compute lower index
    # 3. compute upper index
    # 4. return corresponding values
    sorted_values = sorted(values)
    n = len(sorted_values)
    lower_index = int(lower * n)
    upper_index = int(upper * n)
    if upper_index >= n:
        upper_index = n - 1
    return sorted_values[lower_index], sorted_values[upper_index]


def main() -> None:
    random.seed(42)

    data = [1.2, 2.3, 2.8, 3.1, 4.0, 5.5]

    print("TODO 1: Basic summary")
    print(compute_basic_summary(data))

    print("\nTODO 2: Manual mean")
    print(manual_mean(data))

    print("\nTODO 3: Manual sample variance")
    print(manual_sample_variance(data))

    print("\nTODO 4: Bootstrap means")
    means = bootstrap_means(data, n_boot=1000)
    print(means[:10])

    print("\nTODO 5: Bootstrap percentile interval")
    print(percentile_interval(means))


if __name__ == "__main__":
    main()


# -------------------------------------------------------------------
# SAMPLE ANSWER — REFERENCE ONLY
# Keep this section commented out while practicing.
# -------------------------------------------------------------------

# def compute_basic_summary(data: list[float]) -> dict[str, float]:
#     return {
#         "mean": statistics.mean(data),
#         "sample_variance": statistics.variance(data),
#         "sample_stdev": statistics.stdev(data),
#         "population_variance": statistics.pvariance(data),
#         "population_stdev": statistics.pstdev(data),
#     }
#
#
# def manual_mean(data: list[float]) -> float:
#     return sum(data) / len(data)
#
#
# def manual_sample_variance(data: list[float]) -> float:
#     xbar = manual_mean(data)
#     squared_deviations = []
#
#     for x in data:
#         squared_deviations.append((x - xbar) ** 2)
#
#     return sum(squared_deviations) / (len(data) - 1)
#
#
# def bootstrap_means(
#     data: list[float],
#     n_boot: int = 1000,
# ) -> list[float]:
#     means = []
#
#     for _ in range(n_boot):
#         sample = []
#
#         for _ in range(len(data)):
#             sample.append(random.choice(data))
#
#         means.append(statistics.mean(sample))
#
#     return means
#
#
# def percentile_interval(
#     values: list[float],
#     lower: float = 0.025,
#     upper: float = 0.975,
# ) -> tuple[float, float]:
#     sorted_values = sorted(values)
#     n = len(sorted_values)
#
#     lower_index = int(lower * n)
#     upper_index = int(upper * n)
#
#     if upper_index >= n:
#         upper_index = n - 1
#
#     return sorted_values[lower_index], sorted_values[upper_index]
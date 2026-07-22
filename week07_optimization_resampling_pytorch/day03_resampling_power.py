import math
from typing import Tuple

import numpy as np

from scipy.stats import permutation_test
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize


def mean_difference(
    control: np.ndarray,
    treatment: np.ndarray,
) -> float:
    """
    Return treatment mean minus control mean.
    """

    return float(np.mean(treatment) - np.mean(control))


def bootstrap_difference_ci(
    control: np.ndarray,
    treatment: np.ndarray,
    n_resamples: int = 10_000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> Tuple[float, float]:
    """
    Estimate a percentile bootstrap confidence interval for the
    difference in means.
    """

    # TODO: Create a random-number generator and repeatedly sample each
    # group independently with replacement. Store the treatment-minus-control
    # mean difference for every resample, then return the lower and upper
    # quantiles corresponding to the requested confidence level.

    rng = np.random.default_rng(seed)
    differences = np.empty(n_resamples)

    for index in range(n_resamples):
        control_sample = rng.choice(
            control,
            size = len(control),
            replace = True,
        )
        treatment_sample = rng.choice(
            treatment,
            size = len(treatment),
            replace = True,
        )

        differences[index] = mean_difference(
            control_sample,
            treatment_sample,
        )

    alpha = 1.0 - confidence_level

    lower = np.quantile(
        differences,
        alpha / 2,
    )

    upper = np.quantile(
        differences,
        1.0 - alpha / 2,
    )

    return float(lower), float(upper)


def independent_permutation_pvalue(
    control: np.ndarray,
    treatment: np.ndarray,
    n_resamples: int = 10_000,
    seed: int = 42,
) -> float:
    """
    Perform a two-sided independent permutation test.
    """

    # TODO: Call scipy.stats.permutation_test with mean_difference as the
    # statistic, independent group permutations, a two-sided alternative,
    # and a reproducible random-number generator. Return the p-value.

    result = permutation_test(
        data = (control, treatment),
        statistic = mean_difference,
        permutation_type = "independent",
        vectorized = False,
        n_resamples = n_resamples,
        alternative = "two-sided",
        rng = np.random.default_rng(seed)
    )

    return float(result.pvalue)


def required_sample_size_per_group(
    control_rate: float,
    treatment_rate: float,
    alpha: float = 0.05,
    power: float = 0.80,
) -> int:
    """
    Approximate the required sample size per group for two independent
    proportions with equal allocation.
    """

    # TODO: Convert the two proportions to an absolute standardized
    # effect size, use NormalIndPower.solve_power with equal group sizes,
    # and round the required sample size upward.

    effect_size = abs(
        proportion_effectsize(
            treatment_rate,
            control_rate,
        )
    )
    analysis = NormalIndPower()

    required_n = analysis.solve_power(
        effect_size = effect_size,
        nobs1 = None,
        alpha = alpha,
        power = power,
        ratio = 1.0,
        alternative="two-sided",
    )

    return math.ceil(required_n)


def main() -> None:
    control = np.array([
        10.2, 9.8, 11.4, 10.7, 9.9,
        10.5, 11.1, 10.0, 10.3, 9.7,
    ])

    treatment = np.array([
        11.3, 10.9, 12.0, 11.8, 10.7,
        11.5, 11.9, 10.8, 11.2, 11.0,
    ])

    observed = mean_difference(control, treatment)

    lower, upper = bootstrap_difference_ci(
        control,
        treatment,
    )

    pvalue = independent_permutation_pvalue(
        control,
        treatment,
    )

    required_n = required_sample_size_per_group(
        control_rate=0.10,
        treatment_rate=0.12,
    )

    print(f"Observed difference: {observed:.4f}")
    print(f"Bootstrap 95% CI: ({lower:.4f}, {upper:.4f})")
    print(f"Permutation p-value: {pvalue:.4f}")
    print(f"Required sample size per group: {required_n}")


if __name__ == "__main__":
    main()
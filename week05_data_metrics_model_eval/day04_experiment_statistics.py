import math
import random
import statistics


def normal_cdf(x: float) -> float:
    """
    Approximate the standard normal CDF using math.erf.

    CDF(x) = P(Z <= x), where Z ~ N(0, 1).
    """
    # TODO 1:
    # Return the standard normal CDF.
    # Hint:
    # 0.5 * (1 + math.erf(x / math.sqrt(2)))
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def two_sided_p_value_from_z(z: float) -> float:
    """
    Convert a z-statistic to a two-sided p-value.
    """
    # TODO 2:
    # For a two-sided test:
    # p = 2 * (1 - normal_cdf(abs(z)))

    return 2 * (1 - normal_cdf(abs(z)))


def two_proportion_z_test(
    x_control: int,
    n_control: int,
    x_treatment: int,
    n_treatment: int,
) -> dict:
    """
    Compare two conversion rates.

    x_control: number of converted users in control
    n_control: number of users in control
    x_treatment: number of converted users in treatment
    n_treatment: number of users in treatment
    """

    # TODO 3:
    p_control = x_control / n_control

    # TODO 4:
    p_treatment = x_treatment / n_treatment

    # TODO 5:
    diff = p_treatment - p_control

    # TODO 6:
    # Compute pooled proportion:
    pooled = (x_control + x_treatment) / (n_control + n_treatment)

    # TODO 7:
    # Compute pooled standard error:
    se = math.sqrt(pooled * (1 - pooled) * (1/n_control + 1/n_treatment))

    # TODO 8:
    z = diff / se

    # TODO 9:
    p_value = two_sided_p_value_from_z(z)

    # TODO 10:
    # Compute 95% confidence interval for the difference.
    # For a simple large-sample CI, use unpooled SE:
    se_unpooled = math.sqrt(
        p_control * (1 - p_control) / n_control
         + p_treatment * (1 - p_treatment) / n_treatment
         )
    ci_low = diff - 1.96 * se_unpooled
    ci_high = diff + 1.96 * se_unpooled

    # TODO 11:
    return {
        "p_control": p_control,
        "p_treatment": p_treatment,
        "diff": diff,
        "pooled": pooled,
        "se_pooled": se,
        "z": z,
        "p_value": p_value,
        "ci_95": (ci_low, ci_high),
    }



def bootstrap_difference_in_means(
    control: list[int],
    treatment: list[int],
    n_boot: int = 5000,
    seed: int = 42,
) -> tuple[float, float]:
    """
    Bootstrap a 95% confidence interval for difference in means.

    control and treatment are lists of 0/1 conversion outcomes.
    """
    random.seed(seed)

    # TODO 12:
    # Repeatedly sample with replacement from control and treatment.
    # Store treatment_mean - control_mean for each bootstrap sample.
    diffs = []

    for _ in range(n_boot):
        control_sample = [random.choice(control) for _ in range(len(control))]
        treatment_sample = [random.choice(treatment) for _ in range(len(treatment))]


    # TODO 13:
    # Sort bootstrap differences.
    # Return 2.5% and 97.5% empirical quantiles.
        diff = statistics.mean(treatment_sample) - statistics.mean(control_sample)
        diffs.append(diff)

    diffs.sort()

    lower_idx = int(0.025 * n_boot)
    upper_idx = int(0.975 * n_boot)

    return diffs[lower_idx], diffs[upper_idx]


def estimate_conditional_probability(n_sim: int = 100_000, seed: int = 42) -> float:
    """
    Estimate:
        P(first die is 6 | sum of two dice >= 8)

    by Monte Carlo simulation.
    """
    random.seed(seed)

    numerator = 0
    denominator = 0

    # TODO 14:
    # Simulate two dice.
    # If die1 + die2 >= 8, increase denominator.
    # Among those cases, if die1 == 6, increase numerator.
    for _ in range(n_sim):
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)

        if die1 + die2 >= 8:
            denominator += 1

            if die1 == 6:
                numerator += 1


    # TODO 15:
    # Return numerator / denominator.
    return numerator / denominator
    


def main() -> None:
    print("\n=== Two-proportion z-test ===")

    # Example:
    # control: 120 conversions out of 1000
    # treatment: 145 conversions out of 1000

    result = two_proportion_z_test(
        x_control=120,
        n_control=1000,
        x_treatment=145,
        n_treatment=1000,
    )

    print(result)

    print("\n=== Bootstrap CI for conversion lift ===")

    control = [1] * 120 + [0] * 880
    treatment = [1] * 145 + [0] * 855

    boot_ci = bootstrap_difference_in_means(
        control=control,
        treatment=treatment,
        n_boot=5000,
        seed=42,
    )

    print("Bootstrap 95% CI for treatment - control:", boot_ci)

    print("\n=== Conditional probability simulation ===")

    estimated_prob = estimate_conditional_probability(
        n_sim=100_000,
        seed=42,
    )

    print("Estimated P(first die is 6 | sum >= 8):", estimated_prob)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# SAMPLE ANSWER
# ----------------------------------------------------------------------
#
# def normal_cdf(x: float) -> float:
#     return 0.5 * (1 + math.erf(x / math.sqrt(2)))
#
#
# def two_sided_p_value_from_z(z: float) -> float:
#     return 2 * (1 - normal_cdf(abs(z)))
#
#
# def two_proportion_z_test(
#     x_control: int,
#     n_control: int,
#     x_treatment: int,
#     n_treatment: int,
# ) -> dict:
#     p_control = x_control / n_control
#     p_treatment = x_treatment / n_treatment
#
#     diff = p_treatment - p_control
#
#     pooled = (x_control + x_treatment) / (n_control + n_treatment)
#
#     se = math.sqrt(
#         pooled * (1 - pooled) * (1 / n_control + 1 / n_treatment)
#     )
#
#     z = diff / se
#     p_value = two_sided_p_value_from_z(z)
#
#     se_unpooled = math.sqrt(
#         p_control * (1 - p_control) / n_control
#         + p_treatment * (1 - p_treatment) / n_treatment
#     )
#
#     ci_low = diff - 1.96 * se_unpooled
#     ci_high = diff + 1.96 * se_unpooled
#
#     return {
#         "p_control": p_control,
#         "p_treatment": p_treatment,
#         "diff": diff,
#         "pooled": pooled,
#         "se_pooled": se,
#         "z": z,
#         "p_value": p_value,
#         "ci_95": (ci_low, ci_high),
#     }
#
#
# def bootstrap_difference_in_means(
#     control: list[int],
#     treatment: list[int],
#     n_boot: int = 5000,
#     seed: int = 42,
# ) -> tuple[float, float]:
#     random.seed(seed)
#     diffs = []
#
#     for _ in range(n_boot):
#         control_sample = [random.choice(control) for _ in range(len(control))]
#         treatment_sample = [random.choice(treatment) for _ in range(len(treatment))]
#
#         diff = statistics.mean(treatment_sample) - statistics.mean(control_sample)
#         diffs.append(diff)
#
#     diffs.sort()
#
#     lower_idx = int(0.025 * n_boot)
#     upper_idx = int(0.975 * n_boot)
#
#     return diffs[lower_idx], diffs[upper_idx]
#
#
# def estimate_conditional_probability(n_sim: int = 100_000, seed: int = 42) -> float:
#     random.seed(seed)
#
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
"""
Day 4: Statistical Power Simulation

Goal:
- Simulate two-proportion experiments.
- Estimate how often a test detects a true lift.
- Understand sample size, effect size, and statistical power.
"""

import math
import random


def simulate_experiment(
    n_control: int,
    n_treat: int,
    p_control: float,
    p_treat: float,
) -> tuple[int, int]:
    """
    Simulate one A/B test.

    Return:
    - x_control: number of conversions in control
    - x_treat: number of conversions in treatment
    """
    # TODO:
    # Use random.random()
    x_control = 0
    x_treat = 0

    for _ in range(n_control):
        if random.random() < p_control:
            x_control += 1

    for _ in range(n_treat):
        if random.random() < p_treat:
            x_treat += 1

    return x_control, x_treat


def two_proportion_z_score(
    x_control: int,
    n_control: int,
    x_treat: int,
    n_treat: int,
) -> float:
    """
    Compute z score for two-proportion test.

    Use pooled standard error.
    """
    # TODO:
    # 1. p_control = x_control / n_control
    # 2. p_treat = x_treat / n_treat
    # 3. pooled = (x_control + x_treat) / (n_control + n_treat)
    # 4. se = sqrt(pooled * (1 - pooled) * (1/n_control + 1/n_treat))
    # 5. z = (p_treat - p_control) / se
    p_control = x_control / n_control
    p_treat = x_treat / n_treat
    
    pooled = (x_control + x_treat) / (n_control + n_treat)

    se = math.sqrt(
        pooled
        * (1 - pooled)
        * (1 / n_control + 1 / n_treat)
    )

    if se == 0:
        return 0.0
    
    z = (p_treat - p_control) / se
    
    return z


def estimate_power(
    n_control: int,
    n_treat: int,
    p_control: float,
    p_treat: float,
    n_sim: int = 5000,
    z_threshold: float = 1.96,
) -> float:
    """
    Estimate power by simulation.

    Power:
    - probability of rejecting null when treatment truly differs.
    """
    # TODO:
    # Run many experiments.
    # Count how often abs(z) >= z_threshold.
    reject_count = 0

    for _ in range(n_sim):
        x_control, x_treat = simulate_experiment(
            n_control = n_control,
            n_treat = n_treat,
            p_control = p_control,
            p_treat = p_treat,
        )

        z = two_proportion_z_score(
            x_control = x_control,
            n_control = n_control,
            x_treat = x_treat,
            n_treat = n_treat,
        )

        if abs(z) >= z_threshold:
            reject_count += 1

    return reject_count / n_sim


def main() -> None:
    scenarios = [
        {"n": 500, "p_control": 0.10, "p_treat": 0.11},
        {"n": 1000, "p_control": 0.10, "p_treat": 0.11},
        {"n": 5000, "p_control": 0.10, "p_treat": 0.11},
        {"n": 1000, "p_control": 0.10, "p_treat": 0.13},
    ]

    for scenario in scenarios:
        power = estimate_power(
            n_control=scenario["n"],
            n_treat=scenario["n"],
            p_control=scenario["p_control"],
            p_treat=scenario["p_treat"],
            n_sim=3000,
        )

        print(scenario, "estimated power:", power)


if __name__ == "__main__":
    main()
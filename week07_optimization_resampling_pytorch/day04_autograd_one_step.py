import torch
from torch import nn


def run_one_training_step() -> None:
    """
    Problem:
    Train a one-input binary linear classifier for exactly one step.

    Use:
    - one feature value x = 2.0
    - one binary target y = 1.0
    - initial weight = 0.0
    - initial bias = 0.0
    - SGD learning rate = 0.1

    Print:
    - the initial logit
    - the initial loss
    - the weight and bias gradients
    - the updated weight and bias
    - the updated probability
    """

    # TODO: Build a one-input linear layer, initialize its parameters
    # to zero, create the feature and target tensors, and perform one
    # complete optimization step using BCEWithLogitsLoss and SGD.
    # Print the requested values before and after the parameter update.

    model = nn.Linear(
        in_features = 1,
        out_features = 1,
    )

    with torch.no_grad():
        model.weight.fill_(0.0)
        model.bias.fill_(0.0)

    X = torch.tensor(
        [[2.0]],
        dtype = torch.float32,
    )

    y = torch.tensor(
        [[1.0]],
        dtype = torch.float32,
    )

    loss_fn = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.SGD(
        model.parameters(),
        lr = 0.1,
    )

    optimizer.zero_grad()

    initial_logit = model(X)
    initial_loss = loss_fn(initial_logit, y)

    initial_loss.backward()

    print(f"Initial logit: {initial_logit.item():.4f}")
    print(f"Initial loss: {initial_loss.item():4f}")
    print(f"Weigh gradient: {model.weight.grad.item():.4f}")
    print(f"Bias gradient: {model.bias.grad.item():.4f}")

    optimizer.step()

    with torch.no_grad():
        updated_logit = model(X)
        updated_probability = torch.sigmoid(updated_logit)

    print(f"Updated weight: {model.weight.item():.4f}")
    print(f"Updated bias: {model.bias.item():.4f}")
    print(f"Updated logit: {updated_logit.item():.4f}")
    print(
        f"Updated probability: "
        f"{updated_probability.item():.4f}"
    )

if __name__ == "__main__":
    run_one_training_step()
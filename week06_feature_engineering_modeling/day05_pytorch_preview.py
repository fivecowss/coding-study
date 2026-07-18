"""
Day 5: PyTorch Autograd Preview

Goal:
- Understand tensor, requires_grad, loss, backward, and gradient.
- Compare manual gradient descent idea with PyTorch autograd.
"""

import torch


def scalar_autograd_demo():
    """
    Simple scalar example.

    loss = (w * x - y)^2
    """
    # TODO:
    # 1. Create x, y as tensors.
    # 2. Create w with requires_grad=True.
    # 3. Compute y_hat.
    # 4. Compute loss.
    # 5. Call loss.backward().
    # 6. Print w.grad.
    x = torch.tensor(2.0)
    y = torch.tensor(5.0)

    w = torch.tensor(1.0, requires_grad = True)

    y_hat = w * x
    loss = (y_hat - y) ** 2

    loss.backward()

    print("w:", w.item())
    print("y_hat:", y_hat.item())
    print("loss:", loss.item())
    print("d loss / d w:", w.grad.item())


def vector_autograd_demo():
    """
    Vector example.

    y_hat = sum(x * w) + b
    loss = (y_hat - y)^2
    """
    # TODO:
    # 1. Create x vector.
    # 2. Create w vector with requires_grad=True.
    # 3. Create b scalar with requires_grad=True.
    # 4. Compute y_hat.
    # 5. Compute loss.
    # 6. Call backward.
    # 7. Print gradients.
    x = torch.tensor([1.0, 2.0, 3.0])
    y = torch.tensor(10.0)

    w = torch.tensor([0.1, 0.2, 0.3], requires_grad = True)
    b = torch.tensor(0.0, requires_grad =True)

    y_hat = (x * w).sum() + b
    loss = (y_hat - y) ** 2

    loss.backward()

    print("y_hat:", y_hat.item())
    print("loss:", loss.item())
    print("w.grad:", w.grad)
    print("b.grad:", b.grad)




def one_step_gradient_descent():
    """
    One gradient descent update using torch.no_grad().
    """
    # TODO:
    # 1. Create x, y, w.
    # 2. Compute loss.
    # 3. backward.
    # 4. update w inside torch.no_grad().
    # 5. zero gradient using w.grad.zero_().
    x = torch.tensor(2.0)
    y = torch.tensor(5.0)

    w = torch.tensor(1.0, requires_grad = True)

    y_hat = w * x
    loss = (y_hat - y) ** 2

    loss.backward()

    print("before update")
    print("w:", w.item())
    print("loss:", loss.item())
    print("grad:", w.grad.item())

    learning_rate = 0.1

    with torch.no_grad():
        w -= learning_rate * w.grad

    w.grad.zero_()

    y_hat_after = w * x
    loss_after = (y_hat_after - y) ** 2

    print("after update")
    print("w:", w.item())
    print("loss:", loss_after.item())
    print("grad after zero:", w.grad.item())


def main():
    print("Scalar autograd demo")
    scalar_autograd_demo()
    print()

    print("Vector autograd demo")
    vector_autograd_demo()
    print()

    print("One-step gradient descent demo")
    one_step_gradient_descent()


if __name__ == "__main__":
    main()
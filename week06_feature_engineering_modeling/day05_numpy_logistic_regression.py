"""
Day 5: Logistic Regression from Scratch with NumPy

Goal:
- Implement sigmoid.
- Implement binary cross entropy.
- Implement gradient descent.
- Implement predict_proba and predict.
- Understand the training loop.
"""

import numpy as np


def sigmoid(z):
    """
    Convert linear score z into probability.

    Formula:
    sigmoid(z) = 1 / (1 + exp(-z))
    """
    # TODO:
    # Return sigmoid value.
    return 1 / (1 + np.exp(-z))


def binary_cross_entropy(y_true, y_prob, eps=1e-12):
    """
    Compute binary cross entropy loss.

    y_true:
    - array of 0/1 labels

    y_prob:
    - array of predicted probabilities
    """
    # TODO:
    # 1. Clip y_prob into [eps, 1 - eps].
    # 2. Compute negative mean log likelihood.
    y_prob = np.clip(y_prob, eps, 1 - eps)

    loss = -np.mean(
        y_true * np.log(y_prob)
        + (1 - y_true) * np.log(1 - y_prob)
    )

    return loss


def initialize_parameters(n_features):
    """
    Initialize weights and bias.

    Return:
    - w: zeros of shape (n_features,)
    - b: scalar 0.0
    """
    # TODO
    w = np.zeros(n_features)
    b = 0.0

    return w, b


def compute_gradients(X, y, y_prob):
    """
    Compute gradients for logistic regression.

    grad_w = X.T @ (y_prob - y) / n
    grad_b = mean(y_prob - y)
    """
    # TODO:
    # Return grad_w, grad_b
    n = X.shape[0]

    error = y_prob - y
    
    grad_w = X.T @ error / n
    grad_b = np.mean(error)

    return grad_w, grad_b


def fit_logistic_regression(
    X,
    y,
    learning_rate=0.1,
    n_steps=1000,
    print_every=100,
):
    """
    Fit logistic regression using gradient descent.

    Return:
    - w
    - b
    - loss_history
    """
    # TODO:
    # 1. Initialize parameters.
    # 2. For each step:
    #    z = X @ w + b
    #    y_prob = sigmoid(z)
    #    loss = binary_cross_entropy(y, y_prob)
    #    grad_w, grad_b = compute_gradients(...)
    #    update w and b
    # 3. Return w, b, loss_history
    n_features = X.shape[1]
    w, b = initialize_parameters(n_features)

    loss_history = []

    for step in range(n_steps):
        z = X @ w + b
        y_prob = sigmoid(z)

        loss = binary_cross_entropy(y, y_prob)
        loss_history.append(loss)

        grad_w, grad_b = compute_gradients(X, y, y_prob)

        w -= learning_rate * grad_w
        b -= learning_rate * grad_b

        if step % print_every == 0:
            print(f"step = {step}, loss = {loss:.4f}")

    return w, b, loss_history


def predict_proba(X, w, b):
    """
    Return predicted probabilities.
    """
    # TODO
    z = X @ w + b
    return sigmoid(z)


def predict(X, w, b, threshold=0.5):
    """
    Convert probabilities into class labels.
    """
    # TODO
    prob = predict_proba(X, w, b)
    return (prob >= threshold).astype(int)


def build_toy_data(seed=42):
    """
    Build synthetic binary classification data.
    """
    # TODO:
    # 1. Use np.random.default_rng(seed).
    # 2. Generate X with shape (300, 3).
    # 3. Generate true logits using true_w and true_b.
    # 4. Convert logits into probabilities.
    # 5. Generate y using rng.binomial.
    # 6. Return X, y.
    rng = np.random.default_rng(seed)

    X = rng.normal(size = (300, 3))

    true_w = np.array([1.5, -2.0, 0.8])
    true_b = -0.2

    logits = X @ true_w + true_b
    probs = sigmoid(logits)

    y = rng.binomial(n=1, p=probs)

    return X, y


def accuracy_score_manual(y_true, y_pred):
    """
    Compute accuracy manually.
    """
    # TODO
    return np.mean(y_true == y_pred)


def main():
    X, y = build_toy_data()

    w, b, loss_history = fit_logistic_regression(
        X,
        y,
        learning_rate=0.1,
        n_steps=1000,
        print_every=100,
    )

    y_prob = predict_proba(X, w, b)
    y_pred = predict(X, w, b, threshold=0.5)

    acc = accuracy_score_manual(y, y_pred)

    print()
    print("Estimated weights:", w)
    print("Estimated bias:", b)
    print("Final loss:", loss_history[-1])
    print("Training accuracy:", acc)
    print("First 10 probabilities:", y_prob[:10])
    print("First 10 predictions:", y_pred[:10])
    print("First 10 true labels:", y[:10])


if __name__ == "__main__":
    main()
import random
from typing import Tuple

import numpy as np
import torch

from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from torch import nn
from torch.utils.data import DataLoader, TensorDataset


SEED = 42


def set_seed(seed: int = SEED) -> None:
    """
    Set reproducible random seeds.
    """

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def prepare_data(
    batch_size: int = 32,
) -> Tuple[DataLoader, DataLoader, DataLoader, int]:
    """
    Problem:
    Load the breast-cancer dataset and create train, validation,
    and test DataLoaders.

    Requirements:
    - use stratified splits
    - use 60% train, 20% validation, and 20% test
    - fit StandardScaler only on the training data
    - use float32 tensors
    - reshape targets to (n_samples, 1)
    - shuffle only the training loader
    - use num_workers=0 for Windows compatibility
    """

    # TODO: Load and split the data, fit the scaler only on the
    # training features, transform all three subsets, convert them
    # to TensorDataset objects, and return three DataLoaders plus
    # the number of input features.

    X, y = load_breast_cancer(
        return_X_y=True,
    )

    X = X.astype(np.float32)
    y = y.astype(np.float32)

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size = 0.40,
        random_state=SEED,
        stratify=y,
    )

    X_validation, X_test, y_validation, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=SEED,
        stratify=y_temp,
    )

    scaler = StandardScaler()

    X_train = scaler.fit_transform(
        X_train,
    ).astype(np.float32)

    X_validation = scaler.transform(
        X_validation,
    ).astype(np.float32)

    X_test = scaler.transform(
        X_test,
    ).astype(np.float32)

    train_dataset = TensorDataset(
        torch.from_numpy(X_train),
        torch.from_numpy(y_train).reshape(-1, 1),
    )

    validation_dataset = TensorDataset(
        torch.from_numpy(X_validation),
        torch.from_numpy(y_validation).reshape(-1,1)
    )

    test_dataset = TensorDataset(
        torch.from_numpy(X_test),
        torch.from_numpy(y_test).reshape(-1,1),
    )

    train_loader = DataLoader(
        train_dataset,
        batch_size = batch_size,
        shuffle = True,
        num_workers = 0,
    )

    validation_loader = DataLoader(
        validation_dataset,
        batch_size = batch_size,
        shuffle=False,
        num_workers = 0,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size = batch_size,
        shuffle=False,
        num_workers=0,
    )

    n_features = X_train.shape[1]

    return (
        train_loader,
        validation_loader,
        test_loader,
        n_features,
    )


class BinaryClassifier(nn.Module):
    """
    A small feed-forward binary classifier.
    """

    def __init__(
        self,
        n_features: int,
        hidden_units: int = 16,
    ):
        super().__init__()

        # TODO: Build a network with one hidden Linear layer,
        # a ReLU activation, and one output logit.

        self.network = nn.Sequential(
            nn.Linear(
                in_features=n_features,
                out_features=hidden_units,
            ),
            nn.ReLU(),
            nn.Linear(
                in_features=hidden_units,
                out_features=1,
            ),
        )

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        # TODO: Return the network output.
        return self.network(X)


def train_one_epoch(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> float:
    """
    Train the model for one epoch and return average loss.
    """

    # TODO: Set training mode and perform a complete mini-batch
    # optimization loop. Accumulate sample-weighted batch losses
    # and return the average training loss.

    model.train()

    total_loss = 0.0
    total_samples = 0

    for X_batch, y_batch in loader:
        X_batch = X_batch.to(device)
        y_batch = y_batch.to(device)

        optimizer.zero_grad(
            set_to_none=True,
        )

        logits = model(X_batch)
        loss = loss_fn(logits, y_batch)

        loss.backward()
        optimizer.step()

        batch_size = len(X_batch)

        total_loss += loss.item() * batch_size
        total_samples += batch_size

    return total_loss / total_samples


def evaluate(
    model: nn.Module,
    loader: DataLoader,
    loss_fn: nn.Module,
    device: torch.device,
) -> Tuple[float, float, float]:
    """
    Return average loss, accuracy, and ROC AUC.
    """

    # TODO: Set evaluation mode, disable gradient calculation,
    # collect probabilities and labels over all batches, and
    # compute average loss, accuracy, and ROC AUC.

    model.eval()

    total_loss = 0.0
    total_samples = 0

    probabilities = []
    labels = []

    with torch.no_grad():
        for X_batch, y_batch in loader:
            X_batch = X_batch.to(device)
            y_batch = y_batch.to(device)

            logits = model(X_batch)
            loss = loss_fn(logits,y_batch)

            probability = torch.sigmoid(logits)

            batch_size = len(X_batch)

            total_loss += loss.item() * batch_size
            total_samples += batch_size

            probabilities.append(
                probability.cpu().numpy()
            )

            labels.append(
                y_batch.cpu().numpy()
            )

    y_probability = np.concatenate(
        probabilities,
    ).ravel()

    y_true = np.concatenate(
        labels,
    ).ravel()

    y_pred = (
        y_probability >= 0.5
    ).astype(int)

    average_loss = total_loss / total_samples
    accuracy = accuracy_score(y_true, y_pred)
    roc_auc = roc_auc_score(y_true, y_probability)

    return average_loss, accuracy, roc_auc

def main() -> None:
    # TODO: Set the random seed, select CPU or CUDA, prepare data,
    # create the model, loss, and optimizer, then train for multiple
    # epochs while printing training and validation metrics.
    # Finish with one test-set evaluation.

    set_seed()

    device = torch.device(
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    print(f"Device: {device}")

    (
        train_loader,
        validation_loader,
        test_loader,
        n_features,
    ) = prepare_data(
        batch_size=32,
    )

    model = BinaryClassifier(
        n_features = n_features,
        hidden_units=16,
    ).to(device)

    loss_fn = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr = 1e-3,
    )

    n_epochs = 40

    for epoch in range(1, n_epochs +1):
        train_loss = train_one_epoch(
            model=model,
            loader = train_loader,
            loss_fn = loss_fn,
            optimizer = optimizer,
            device = device,
        )

        (
            validation_loss,
            validation_accuracy,
            validation_auc,
        ) = evaluate(
            model=model,
            loader=validation_loader,
            loss_fn=loss_fn,
            device = device,
        )

        if epoch ==1 or epoch % 5 == 0:
            print(
                f"epoch {epoch:02d} | "
                f"train_loss={train_loss:.4f} | "
                f"validation_loss={validation_loss:.4f} | "
                f"validation_accurary="
                f"{validation_accuracy:.4f} | "
                f"validation_auc={validation_auc:.4f}"
            )

        (
            test_loss,
            test_accuracy,
            test_auc,
        ) = evaluate(
            model=model,
            loader=test_loader,
            loss_fn = loss_fn,
            device = device,
        )

        print("\nFianl test results")
        print(f"Test loss: {test_loss: .4f}")
        print(f"Test accuracy: {test_accuracy:.4f}")
        print(f"Test ROC AUC: {test_auc:4f}")


if __name__ == "__main__":
    main()
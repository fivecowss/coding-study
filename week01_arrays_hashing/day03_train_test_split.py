## stratify = y means that the split will be done in such a way that the proportion of each class in the target variable (y) is maintained in both the training and testing sets. This is particularly important when dealing with imbalanced datasets, where one class may be significantly more prevalent than the other(s). By using stratification, you ensure that both the training and testing sets have a similar distribution of classes, which can lead to more reliable and generalizable model performance.
## for classification problems, especially when the target variable has imbalanced classes. It helps to ensure that the model is trained and evaluated on representative samples of each class, which can lead to better performance and more accurate predictions.

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

def main():
    data = load_breast_cancer(as_frame = True)
    
    X = data.data
    y = data.target

    print("X shape:", X.shape)
    print("y shape:", y.shape)
    print()
    print("Target counts:")
    print(y.value_counts())

    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y, 
        test_size = 0.2,
        random_state = 42,
        stratify = y,
    )

    print()
    print("X_train shape:", X_train.shape)
    print("X_test shape:", X_test.shape)
    print("y_train counts:")
    print(y_train.value_counts())
    print("y_test counts:")
    print(y_test.value_counts())

if __name__ == "__main__":
    main()


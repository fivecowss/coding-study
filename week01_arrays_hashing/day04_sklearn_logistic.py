from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

def main():
    data = load_breast_cancer(as_frame=True)

    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, 
                                                        y, 
                                                        test_size = 0.2, 
                                                        random_state = 42,
                                                        stratify = y,
                                                        )
    
    model = LogisticRegression(max_iter = 1000)

    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, pred))
    print()
    print("Classification report:")
    print(classification_report(y_test, pred))


if __name__ == "__main__":
    main()

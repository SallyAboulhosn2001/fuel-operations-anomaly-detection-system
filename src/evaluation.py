from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def classify_risk(df):

    df = df.copy()

    df["risk_score"] = (
        df["investigate_robust"].astype(int) * 2
        + df["ml_anomaly_flag"].astype(int)
    )

    def classify(score):

        if score >= 3:
            return "High Risk"

        elif score == 2:
            return "Medium Risk"

        elif score == 1:
            return "Low Risk"

        else:
            return "Normal"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

def evaluate_fraud_model(y_true, y_pred):

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="weighted")
    recall = recall_score(y_true, y_pred, average="weighted")
    f1 = f1_score(y_true, y_pred, average="weighted")

    print("\n--- Fraud Model Evaluation ---")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

    print("\nDetailed Report:")
    print(classification_report(y_true, y_pred))

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }

def plot_confusion_matrix(y_true, y_pred):

    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=(6,5))
    labels = ["cash_theft", "normal", "pump_manipulation", "service_fraud"]

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=labels,
            yticklabels=labels)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")

    plt.show()
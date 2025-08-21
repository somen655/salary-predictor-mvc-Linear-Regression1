from app.services.metrics import evaluate_from_csv

if __name__ == "__main__":
    metrics = evaluate_from_csv()
    print("Training complete:", metrics)

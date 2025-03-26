from flask import Flask, jsonify, render_template
import pandas as pd
from pathlib import Path

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def _load_excel_data():
    excel_path = Path("../data/DexterCRM_MockData_7gc.xlsx")
    df = pd.read_excel(excel_path)
    return df

@app.route("/")
def dashboard():
    return render_template("index.html")

@app.route("/api/investors", methods=["GET"])
def get_investors():
    df = _load_excel_data()
    return jsonify(df.to_dict(orient="records"))

@app.route("/api/metrics", methods=["GET"])
def get_metrics():
    df = _load_excel_data()

    metrics = {
        "total_investors": int(len(df)),
        "total_revenue_millions": float(df["Revenue ($M)"].sum()),
        "investment_stage_counts": df["Investment Stage"].value_counts().to_dict(),
        "internal_bias_distribution": df["Internal Bias"].value_counts().to_dict(),
    }

    return jsonify(metrics)

if __name__ == "__main__":
    app.run(debug=True)

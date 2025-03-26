from flask import Flask, jsonify, render_template, request
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Allow import from parent
from claude_client import summarize_investor

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def _load_excel_data():
    excel_path = Path("./data/DexterCRM_MockData_7gc.xlsx")
    if not excel_path.exists():
        print("⚠️ Excel file not found at:", excel_path.resolve())
        return pd.DataFrame()  # Return empty DataFrame if file not found
    return pd.read_excel(excel_path)

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

    if df.empty:
        # Provide fallback empty response for frontend
        return jsonify({
            "total_investors": 0,
            "total_revenue_millions": 0.0,
            "investment_stage_counts": {},
            "internal_bias_distribution": {}
        })

    metrics = {
        "total_investors": int(len(df)),
        "total_revenue_millions": float(df['Revenue ($M)'].sum()),
        "investment_stage_counts": df['Investment Stage'].value_counts().to_dict(),
        "internal_bias_distribution": df['Internal Bias'].value_counts().to_dict(),
    }

    return jsonify(metrics)

@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.json
    profile = data.get("profile", "")
    if not profile:
        return jsonify({"error": "Missing 'profile' field"}), 400
    summary = summarize_investor(profile)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run(debug=True)
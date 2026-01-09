import requests
import json

url = 'http://127.0.0.1:5000/predict'

def run_test(test_name, payload):
    print(f"--- Running Test: {test_name} ---")
    try:
        response = requests.post(url, json=payload)
        print(f"Status: {response.status_code}")
        print(f"Result: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error connecting to API: {e}")
    print("\n")

# 1. TEST CASE: THE IDEAL APPLICANT (Should Approve)
good_applicant = {
    "applicant": {
        "checking_balance": "> 200 DM", 
        "duration": 12,
        "credit_history": "existing paid",
        "amount": 1000,
        "savings": "> 1000 DM",
        "employment": "4-7 years"
    },
    "bureau": {
        "trade_lines": [{"status": "P"}, {"status": "P"}, {"status": "P"}]
    }
}

# 2. TEST CASE: INTERNAL MODEL REJECT (Risk Score > 0.24)
# We trigger this with low cash and a long loan duration
high_risk_applicant = {
    "applicant": {
        "checking_balance": "< 0 DM", 
        "duration": 60,
        "credit_history": "all paid",
        "amount": 15000
    },
    "bureau": {
        "trade_lines": [{"status": "P"}]
    }
}

# 3. TEST CASE: BUREAU SAFETY NET REJECT (Bad Ratio > 30%)
# Even if the internal model likes them, the Bureau "Default" status will kill the deal
bureau_fail_applicant = {
    "applicant": {
        "checking_balance": "> 200 DM",
        "duration": 6,
        "credit_history": "existing paid",
        "amount": 500
    },
    "bureau": {
        "trade_lines": [
            {"status": "D"}, # Default
            {"status": "D"}, # Default
            {"status": "P"}  # Paid
        ]
    }
}

if __name__ == "__main__":
    # Ensure app.py is running before executing this
    run_test("Ideal Applicant", good_applicant)
    run_test("High Risk (Internal Model)", high_risk_applicant)
    run_test("Bureau Safety Net Reject", bureau_fail_applicant)
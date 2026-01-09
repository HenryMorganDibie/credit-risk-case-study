import sys
import os
import joblib
import pandas as pd

# This line is the "magic" fix for your ModuleNotFoundError
# It tells Python to look in the folder where this script lives for 'features'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from features import BureauFeatureExtractor 

class CreditScoringService:
    def __init__(self, model_path='output/model_v1.pkl'):
        """Loads model and metadata once."""
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Missing model artifact at {model_path}")
            
        artifacts = joblib.load(model_path)
        self.model = artifacts['model']
        self.feature_names = artifacts['features'] 
        self.strategic_threshold = artifacts['threshold'] 
        self.bureau_extractor = BureauFeatureExtractor()

    def _preprocess(self, raw_data_row):
        df = pd.DataFrame([raw_data_row])
        df_encoded = pd.get_dummies(df)
        df_final = df_encoded.reindex(columns=self.feature_names, fill_value=0)
        return df_final

    def decide(self, applicant_data, bureau_json):
        # 1. Model Prediction
        processed_data = self._preprocess(applicant_data)
        prob_default = self.model.predict_proba(processed_data)[0][1]
        
        # 2. Bureau Analysis (Calling the transform logic)
        # Note: adjust this if your features.py method name is different
        bureau_metrics = self.bureau_extractor.extract_features(bureau_json)
        bad_ratio = bureau_metrics.get('bureau_bad_ratio', 0)

        # 3. Decision Logic
        if bad_ratio > 0.30:
            return {"decision": "REJECT", "reason": "Bureau Risk Too High", "score": round(prob_default, 3)}

        if prob_default >= self.strategic_threshold:
            return {"decision": "REJECT", "reason": "Model Risk Exceeds Threshold", "score": round(prob_default, 3)}

        return {"decision": "APPROVE", "reason": "Meets risk criteria", "score": round(prob_default, 3)}
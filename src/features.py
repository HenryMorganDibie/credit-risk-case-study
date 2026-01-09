import pandas as pd

class BureauFeatureExtractor:
    """Class to handle processing of Bureau JSON data."""
    
    def __init__(self):
        # We leave this empty so the service can be initialized once
        pass

    def extract_features(self, json_data):
        """
        Parses the raw JSON and returns key risk metrics.
        """
        trade_lines = json_data.get('trade_lines', [])
        if not trade_lines:
            return {'bureau_bad_ratio': 0.0}
            
        bad_count = sum(1 for line in trade_lines if line.get('status') == 'D')
        bad_ratio = bad_count / len(trade_lines)
        
        return {'bureau_bad_ratio': bad_ratio}
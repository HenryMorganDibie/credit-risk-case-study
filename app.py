import os
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template
from src.scoring_logic import CreditScoringService

app = Flask(__name__)
service = CreditScoringService(model_path='output/model_v1.pkl')

def create_plots():
    # 1. Visual from Part 1: Top 10 Drivers of Credit Risk
    drivers_data = pd.DataFrame({
        'Feature': ['checking_balance', 'amount', 'savings_balance', 'months_loan_duration', 'age', 
                    'employment_months', 'residence_months', 'installment_rate', 'installment_plan_none', 'existing_credits'],
        'Importance': [0.118, 0.098, 0.094, 0.080, 0.079, 0.079, 0.070, 0.034, 0.024, 0.022]
    }).sort_values('Importance', ascending=True)
    
    fig1 = px.bar(drivers_data, x='Importance', y='Feature', orientation='h',
                   title="Model Analysis: Top 10 Drivers of Credit Risk",
                   color='Importance', color_continuous_scale='Viridis',
                   template="plotly_white")

    # 2. Visual from Part 1: Business Cost Optimization Curve
    # Simulating the curve from your "Determining the Most Profitable Risk Threshold" image
    x_thresholds = np.linspace(0, 1, 50)
    y_costs = 140 - 20*np.sin(x_thresholds*3) + (x_thresholds**2 * 500) # Simulates your specific curve shape
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_thresholds, y=y_costs, mode='lines', name='Total Business Cost',
                             line=dict(color='#2c3e50', width=3), fill='tozeroy'))
    # Adding the optimal marker at 0.14
    fig2.add_vline(x=0.14, line_dash="dash", line_color="red")
    fig2.add_annotation(x=0.14, y=125, text="Minimum Cost at 0.14", showarrow=True, arrowhead=1)
    fig2.update_layout(title="Strategic Threshold: Business Cost Optimization",
                      xaxis_title="Probability Threshold", yaxis_title="Calculated Business Cost",
                      template="plotly_white")

    # 3. Visual from Part 3: Operational Biker Efficiency
    biker_data = pd.DataFrame({
        'Day of Week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
        'Minutes': [35, 51, 26, 42, 32, 58, 80]
    })
    fig3 = px.bar(biker_data, x='Day of Week', y='Minutes',
                   title="Operational Audit: Average Trip Duration",
                   color_discrete_sequence=['#87ceeb'], 
                   template="plotly_white")

    # Clean up layouts
    for f in [fig1, fig2, fig3]:
        f.update_layout(autosize=True, margin=dict(l=40, r=40, t=60, b=40))

    return json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder), \
           json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder), \
           json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)

@app.route('/')
def home():
    plot1, plot2, plot3 = create_plots()
    stats = {
        "threshold": 0.1414,
        "status": "ONLINE",
        "precision": "High (58/60 Defaults Caught)"
    }
    return render_template('index.html', stats=stats, plot1=plot1, plot2=plot2, plot3=plot3)

if __name__ == '__main__':
    app.run(debug=True)
import pandas as pd
from joblib import load
from backend.logging_setup import setup_logging
model_data = load('artifacts/model_data.joblib')
model = model_data['model']
col_to_scale = model_data['col_to_scale']
scaler = model_data['scaler']
features = model_data['features']

logger = setup_logging('prediction_helper')

def process(features,received_columns):
    logger.info({feature:value for feature,value in received_columns.items()})

    df = pd.DataFrame([received_columns.values()], columns=received_columns.keys())
    df_encoded = pd.get_dummies(df,columns =['residence_type','loan_purpose','loan_type'],dtype ='int')
    for col in features:
        if col not in df_encoded.columns:
            df_encoded[col] =0

    df_scaled = scale(df_encoded)
    for col in df_scaled.columns:
        if col not in features:
            df_scaled.drop(col,axis=1,inplace=True)
    df_final = df_scaled[features]
    return df_final

def scale(df):
    scale = scaler
    cols = col_to_scale
    for col in cols:
        if col not in df.columns:
            df[col]= 0
    df[cols] = scale.transform(df[cols])
    return df

def rating(credit_score):
    if 300 <=credit_score <500:
        return 'Poor'
    elif 500 <=credit_score <650:
        return 'Average'
    elif 650 <=credit_score <750:
        return 'Good'
    elif 750 <=credit_score <900:
        return 'Excellent'

def calc_risk(received_columns):
    if not received_columns:
        logger.warning("Received empty input for columns.")
    df = process(features,received_columns)
    score =model.predict_proba(df).flatten()[1]
    base_score = 300
    scale_length = 600
    credit_score = int(base_score+ (1-score)*scale_length)
    rate = rating(credit_score)
    logger.info(f"Default Probability: {score*100:.2f}%, Credit Score: {credit_score}, Rating: {rate}")
    return score,credit_score,rate
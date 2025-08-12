from fastapi import FastAPI
from pydantic import BaseModel
from prediction import calc_risk
class ClassCreditRiskInput(BaseModel):
        age: int
        loan_to_income:float
        loan_tenure_months: int
        average_dpd_per_delinquency: int
        delinquency_ratio: int
        credit_utilization_ratio: int
        number_of_open_accounts: int
        residence_type: str
        loan_purpose: str
        loan_type: str

class ClassCreditRiskOutput(BaseModel):
    score: float
    credit_score:int
    rate:str
app = FastAPI()
@app.get("/ping")
def ping():
    return "Connection established with backend server"

@app.post("/predict_credit_risk",response_model=ClassCreditRiskOutput)
def input_data(input_data: ClassCreditRiskInput):
    score,credit_score,rate = calc_risk(input_data.dict())
    return ClassCreditRiskOutput(score=score,credit_score=credit_score,rate=rate)
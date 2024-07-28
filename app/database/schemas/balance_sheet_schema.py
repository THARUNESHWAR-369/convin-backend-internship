from pydantic import BaseModel
from typing import List


    
class BalanceSheetDetail(BaseModel):
    id: int
    description: str
    amount: float
    split_method: str

class BalanceSheet(BaseModel):
    user_id: int
    total_amount: float
    details: List[BalanceSheetDetail]

class OverallBalanceSheetDetail(BaseModel):
    user_id: int
    user_name: str
    total_amount: float

class OverallBalanceSheet(BaseModel):
    balance_sheets: List[OverallBalanceSheetDetail]
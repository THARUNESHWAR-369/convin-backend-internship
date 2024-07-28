from pydantic import BaseModel
from typing import List, Optional


class ExpenseBase(BaseModel):
    amount: float
    description: str
    split_method: str


class ExpenseSplit(BaseModel):
    user_id: int
    amount: Optional[float] = None
    percentage: Optional[float] = None


class ExpenseCreate(ExpenseBase):
    splits: List[ExpenseSplit]


class Expense(ExpenseBase):
    id: int
    owner_id: int
    splits: List[ExpenseSplit]

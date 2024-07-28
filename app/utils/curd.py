from sqlalchemy.orm import Session
from app.models import models
from app.utils.security import hash_password
from app.database.schemas.user_schema import UserCreate, User
from app.database.schemas.expense_schema import ExpenseCreate, Expense
from app.database.schemas.balance_sheet_schema import BalanceSheet
from fastapi import HTTPException
from app.utils.status import status_codes as sac
from typing import List, Any, Dict

def create_user(db: Session, user: UserCreate) -> User:
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user information for creating a new user.

    Returns:
        User: The created user.
    """
    db_user : models.User = models.User(
        email=user.email,
        name=user.name,
        mobile=user.mobile,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str) -> (Any | None):
    """
    Retrieve a user by their email.

    Args:
        db (Session): The database session.
        email (str): The user's email.

    Returns:
        Any | None: The user if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.email == email).first()

def get_user(db: Session, user_id: int) -> (User | None):
    """
    Retrieve a user by their ID.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        User | None: The user if found, otherwise None.
    """
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_new_expense(db: Session, expense: ExpenseCreate, owner_id: int) -> Expense:
    """
    Create a new expense and split it according to the specified method.

    Args:
        db (Session): The database session.
        expense (ExpenseCreate): The expense information.
        owner_id (int): The ID of the user creating the expense.

    Returns:
        Expense: The created expense.

    Raises:
        HTTPException: If the sum of split amounts or percentages does not match the total amount.
    """
    db_expense : models.Expense = models.Expense(
        amount=expense.amount,
        description=expense.description,
        split_method=expense.split_method,
        owner_id=owner_id,
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    
    if expense.split_method == "equal":
        split_amount : float = round(db_expense.amount / len(expense.splits), 2)
        for split in expense.splits:
            db_expense_split : models.ExpenseSplit = models.ExpenseSplit(
                user_id=split.user_id, expense_id=db_expense.id, amount=split_amount
            )
            db.add(db_expense_split)
    elif expense.split_method == "exact":
        total_split_amount : float = sum(split.amount for split in expense.splits)
        if total_split_amount != db_expense.amount:
            raise HTTPException(status_code=sac.HTTP_BAD_REQUEST, detail="The sum of split amounts does not equal the total amount.")
        for split in expense.splits:
            db_expense_split : models.ExpenseSplit = models.ExpenseSplit(
                user_id=split.user_id,
                expense_id=db_expense.id,
                amount=round(split.amount, 2)
            )
            db.add(db_expense_split)
            
    elif expense.split_method == "percentage":
        total_percentage : float = sum(split.percentage for split in expense.splits)
        if total_percentage != 100:
            raise HTTPException(status_code=sac.HTTP_BAD_REQUEST, detail="The sum of percentages does not equal 100.")
        for split in expense.splits:
            amount : float = round(db_expense.amount * (split.percentage / 100), 2)
            db_expense_split : models.ExpenseSplit = models.ExpenseSplit(
                user_id=split.user_id,
                expense_id=db_expense.id,
                amount=amount
            )
            db.add(db_expense_split)

    db.commit()
    db.refresh(db_expense)

    return db_expense

def get_user_expenses(db: Session, user_id: int) -> List[Expense]:
    """
    Retrieve all expenses for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        List[Expense]: A list of expenses for the user.
    """
    return db.query(models.Expense).filter(models.Expense.owner_id == user_id).all()

def get_all_expenses(db: Session) -> List[Expense]:
    """
    Retrieve all expenses.

    Args:
        db (Session): The database session.

    Returns:
        List[Expense]: A list of all expenses.
    """
    return db.query(models.Expense).all()

def get_expenses_by_user(db: Session, user_id: int) -> List[Expense]:
    """
    Retrieve all expenses for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        List[Expense]: A list of expenses for the user.
    """
    return db.query(models.Expense).filter(models.Expense.owner_id == user_id).all()

def get_balance_sheet(db: Session, user_id: int) -> BalanceSheet:
    """
    Generate the balance sheet for a specific user.

    Args:
        db (Session): The database session.
        user_id (int): The user's ID.

    Returns:
        BalanceSheet: The balance sheet for the user.
    """
    expenses : List[Expense] = get_expenses_by_user(db, user_id)
    total_amount : float = sum(expense.amount for expense in expenses)
    return {
        "user_id": user_id,
        "total_amount": total_amount,
        "details": expenses
    }

def get_overall_balance_sheet(db: Session) -> List[BalanceSheet]:
    """
    Generate the overall balance sheet for all users.

    Args:
        db (Session): The database session.

    Returns:
        List[BalanceSheet]: A list of balance sheets for all users.
    """
    users : List[User] = db.query(models.User).all()
    balance_sheets : List[BalanceSheet] = []
    for user in users:
        balance_sheet : BalanceSheet = get_balance_sheet(db, user.id)
        balance_sheets.append(balance_sheet)
    return balance_sheets

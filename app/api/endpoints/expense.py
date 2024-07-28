from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.schemas.expense_schema import Expense, ExpenseCreate
from app.database.schemas.user_schema import User
from app.database.schemas.balance_sheet_schema import BalanceSheet, OverallBalanceSheet
from app.utils.curd import (
    create_new_expense,
    get_expenses_by_user,
    get_all_expenses as gae,
    get_balance_sheet as gbs,
    get_overall_balance_sheet as gobs,
)
from app.utils.dependencies import get_db, JWTBearer
from typing import List
from app.utils import dependencies
from fastapi.responses import Response, StreamingResponse
import io
import csv

router: APIRouter = APIRouter()


@router.post(
    "/create_expense",
    response_model=Expense,
    dependencies=[Depends(JWTBearer())],
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> Expense:
    """
    Create a new expense.

    This function creates a new expense for the current user. The expense
    details are provided in the request body.

    Args:
        expense (ExpenseCreate): The expense details to be created.
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        Expense: The created expense object.
    """
    return create_new_expense(db=db, expense=expense, owner_id=current_user.id)


@router.get("/current_user_expenses/", response_model=List[Expense])
def get_current_user_expenses(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> List[Expense]:
    """
    Retrieve expenses for the current user.

    This function retrieves all expenses associated with the current authenticated user.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        List[Expense]: A list of expenses for the current user.
    """
    return get_expenses_by_user(db=db, user_id=current_user.id)


@router.get(
    "/balance_sheet/current_user",
    response_model=BalanceSheet,
    dependencies=[Depends(JWTBearer())],
)
def get_balance_sheet_current_user(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> BalanceSheet:
    """
    Retrieve balance sheet for the current user.

    This function retrieves the balance sheet for the current authenticated user.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        BalanceSheet: The balance sheet for the current user.
    """
    return gbs(db=db, user_id=current_user.id)


@router.get(
    "/balance_sheet/overall",
    response_model=List[BalanceSheet],
    dependencies=[Depends(JWTBearer())],
)
def get_overall_balance_sheet(
    db: Session = Depends(get_db),
) -> List[BalanceSheet]:
    """
    Retrieve overall balance sheet for all users.

    This function retrieves the overall balance sheet for all users.

    Args:
        db (Session): Database session dependency.

    Returns:
        List[BalanceSheet]: A list of balance sheets for all users.
    """
    return gobs(db=db)


@router.get(
    "/download/balance_sheet/current_user/",
    response_model=BalanceSheet,
    dependencies=[Depends(JWTBearer())],
)
def download_current_user_balance_sheet(
    db: Session = Depends(get_db),
    current_user: User = Depends(dependencies.get_current_user),
) -> StreamingResponse:
    """
    Download the balance sheet for the current user.

    This function generates and downloads the balance sheet for the current authenticated user as a CSV file.

    Args:
        db (Session): Database session dependency.
        current_user (User): The current authenticated user.

    Returns:
        StreamingResponse: A CSV file containing the balance sheet for the current user.
    """
    balance_sheet: BalanceSheet = gbs(db=db, user_id=current_user.id)
    return generate_csv(balance_sheet)


@router.get(
    "/download/balance_sheet/overall/",
    response_model=OverallBalanceSheet,
    dependencies=[Depends(JWTBearer())],
)
def download_overall_balance_sheet(db: Session = Depends(get_db)) -> StreamingResponse:
    """
    Download the overall balance sheet for all users.

    This function generates and downloads the overall balance sheet for all users as a CSV file.

    Args:
        db (Session): Database session dependency.

    Returns:
        StreamingResponse: A CSV file containing the overall balance sheet for all users.
    """
    overall_balance_sheet: List[BalanceSheet] = gobs(db=db)
    return generate_overall_csv(overall_balance_sheet)


def generate_csv(balance_sheet: BalanceSheet) -> StreamingResponse:
    """
    Generate a CSV file for the given balance sheet.

    This function creates a CSV file for the provided balance sheet and returns it as a streaming response.

    Args:
        balance_sheet (BalanceSheet): The balance sheet to be converted to CSV.

    Returns:
        StreamingResponse: A CSV file containing the balance sheet.
    """
    output: io.StringIO = io.StringIO()
    writer: csv.writer = csv.writer(output)
    writer.writerow(
        [
            "User ID",
            "Total Amount",
            "Expense ID",
            "Description",
            "Amount",
            "Split Method",
        ]
    )
    for expense in balance_sheet["details"]:
        writer.writerow(
            [
                balance_sheet["user_id"],
                balance_sheet["total_amount"],
                expense.id,
                expense.description,
                expense.amount,
                expense.split_method,
            ]
        )
    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=id-{balance_sheet['user_id']}_balance_sheet.csv"
        },
    )


def generate_overall_csv(
    overall_balance_sheet: List[BalanceSheet],
) -> StreamingResponse:
    """
    Generate a CSV file for the overall balance sheet.

    This function creates a CSV file for the provided overall balance sheet and returns it as a streaming response.

    Args:
        overall_balance_sheet (List[BalanceSheet]): The overall balance sheet to be converted to CSV.

    Returns:
        StreamingResponse: A CSV file containing the overall balance sheet.
    """
    output: io.StringIO = io.StringIO()
    writer: csv.writer = csv.writer(output)
    writer.writerow(
        [
            "User ID",
            "Total Amount",
            "Expense ID",
            "Description",
            "Amount",
            "Split Method",
        ]
    )
    for balance_sheet in overall_balance_sheet:
        for expense in balance_sheet["details"]:
            writer.writerow(
                [
                    balance_sheet["user_id"],
                    balance_sheet["total_amount"],
                    expense.id,
                    expense.description,
                    expense.amount,
                    expense.split_method,
                ]
            )

    output.seek(0)
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=overall_balance_sheet.csv"
        },
    )

"""Tool definitions for Aza Man financial assistant.

This module provides financial tools for budget allocation, expense tracking,
flexible calculations, and user management, optimized for model compatibility.
"""

from typing import Union, List, Dict, Any
from langchain_core.tools import tool

ALL_TOOLS = []


@tool
def budget(income: float, savings_goal: Union[float, str], currency: str) -> Dict[str, Any]:
    """Allocate a budget based on income and savings goal.

    Args:
        income: The user's total income.
        savings_goal: The desired savings amount, as a number or percentage (e.g., "40%").
        currency: The currency code (e.g., "NGN").

    Returns:
        Dict[str, Any]: Budget details including income, savings, expenses, and a message.
    """
    if isinstance(savings_goal, str) and "%" in savings_goal:
        savings_goal = float(savings_goal.strip("%")) / 100 * income
    elif isinstance(savings_goal, str):
        savings_goal = float(savings_goal)
    savings = savings_goal
    budget_for_expenses = income - savings
    return {
        "income": income,
        "savings": savings,
        "budget_for_expenses": budget_for_expenses,
        "currency": currency,
        "message": f"Budget created! Income: {income:,.2f} {currency}, Savings: {savings:,.2f} {currency}, Expenses: {budget_for_expenses:,.2f} {currency}"
    }


ALL_TOOLS.append(budget)


@tool
def log_expenses(expenses: List[Dict[str, Any]], currency: str) -> Dict[str, Any]:
    """Log user expenses and calculate the total.

    Args:
        expenses: List of expense dictionaries with "amount" and "category" keys.
        currency: The currency code (e.g., "NGN").

    Returns:
        Dict[str, Any]: Expense details including total, list, and a message.
    """
    total_expense = sum(expense["amount"] for expense in expenses)
    return {
        "expense": total_expense,
        "expenses": expenses,
        "currency": currency,
        "message": f"Expenses logged! Total: {total_expense:,.2f} {currency}"
    }


ALL_TOOLS.append(log_expenses)


@tool
def math_tool(numbers: List[float], operation: str) -> float:
    """Perform a mathematical operation on a list of numbers.

    Args:
        numbers: A list of numbers to operate on (minimum 1 for add/multiply, 2 for subtract/divide).
        operation: The operation to perform ("add", "subtract", "multiply", "divide").

    Returns:
        float: The result of the operation.

    Raises:
        ValueError: If arguments are insufficient or operation is unsupported.
    """
    if not numbers:
        raise ValueError("At least one number is required.")
    
    if operation == "add":
        return sum(numbers)
    elif operation == "subtract":
        if len(numbers) < 2:
            raise ValueError("Subtract requires at least two numbers.")
        result = numbers[0]
        for num in numbers[1:]:
            result -= num
        return result
    elif operation == "multiply":
        result = 1.0
        for num in numbers:
            result *= num
        return result
    elif operation == "divide":
        if len(numbers) < 2:
            raise ValueError("Divide requires at least two numbers.")
        result = numbers[0]
        for num in numbers[1:]:
            if num == 0:
                raise ValueError("Division by zero is not allowed.")
            result /= num
        return result
    else:
        raise ValueError(f"Unsupported operation: {operation}. Use 'add', 'subtract', 'multiply', or 'divide'.")


ALL_TOOLS.append(math_tool)


@tool
def set_username(username: str) -> Dict[str, Any]:
    """Set the user's username.

    Args:
        username: The username to set.

    Returns:
        Dict[str, Any]: Username details and a confirmation message.
    """
    return {
        "username": username,
        "message": f"Username set to {username}"
    }


ALL_TOOLS.append(set_username)
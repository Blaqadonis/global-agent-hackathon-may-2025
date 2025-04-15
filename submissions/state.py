"""Define the state structure for Aza Man."""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing import Annotated

@dataclass(kw_only=True)
class State:
    """State class for Aza Man financial assistant."""
    messages: Annotated[List[AnyMessage], add_messages] = field(default_factory=list)
    username: str = ""
    income: float = 0.0
    budget_for_expenses: float = 0.0
    expense: float = 0.0
    expenses: List[Dict[str, Any]] = field(default_factory=list)
    savings_goal: float = 0.0
    savings: float = 0.0
    currency: str = ""
    summary: str = ""

    def __post_init__(self):
        """Ensure type consistency after initialization."""
        if not isinstance(self.messages, list):
            self.messages = []
        if not isinstance(self.expenses, list):
            self.expenses = []
        if not isinstance(self.username, str):
            self.username = ""
        if not isinstance(self.income, float):
            self.income = 0.0
        if not isinstance(self.budget_for_expenses, float):
            self.budget_for_expenses = 0.0
        if not isinstance(self.expense, float):
            self.expense = 0.0
        if not isinstance(self.savings_goal, float):
            self.savings_goal = 0.0
        if not isinstance(self.savings, float):
            self.savings = 0.0
        if not isinstance(self.currency, str):
            self.currency = ""
        if not isinstance(self.summary, str):
            self.summary = ""
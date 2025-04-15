"""Evaluation script for Aza Man using OpenEvals with test cases from CSV."""

import os
import csv
from dotenv import load_dotenv
from langchain_together import ChatTogether
from openevals.llm import create_llm_as_judge
import prompts

# Load environment variables
load_dotenv()

# Prompt for Aza Man evaluation
AZA_EVAL_PROMPT = """
You are an expert evaluator assessing the Aza Man financial assistant's outputs for correctness and adherence to its rules. Assign a binary score (True/False) based on this rubric, evaluating the current output in the context of the full conversation sequence provided:

<Rubric>
  A correct answer must:
  - Prompt for a username if not yet provided in the state or any prior inputs/outputs, before any financial actions (e.g., logging expenses or setting a budget). Once set (e.g., via 'Username set to X' in an output), persist it in the state and use it in greetings like 'Hi X!'.
  - Enforce budget creation: if state income = 0, respond with a message indicating the need to create a budget first, asking for income, savings goal, and currency, but only after username is set. If income, savings_goal, and currency are provided across prior inputs and outputs indicate budget creation, use the 'budget' tool to set it (savings = savings_goal% * income, expenses = income - savings).
  - Correctly log and total expenses using the 'log_expenses' tool only if state income > 0 and currency is set, summing all 'amount' values from the expenses list provided in current/prior inputs. It may prompt for categories (e.g., 'Food', 'Transportation'), but if categories are not provided in the next input, it must log them as 'miscellaneous' and update state.expense with the total in that step, as confirmed by prior outputs or the current output.
  - Report spending vs. budget using state values (expense and budget_for_expenses) if income > 0, relying on 'math_tool' for calculations (e.g., budget_for_expenses - expense), never computing manually.
  - Format financial figures as 'X,XXX.00 CURRENCY' (e.g., '1,000.00 USD', '350,000.00 EUR', '12,500.00 GBP') in all monetary responses.
  - Avoid hallucination: use only numbers and details from prior/current inputs or outputs indicating tool usage, no fabricated values or manual calculations.
</Rubric>

Assume the conversation starts with a new session (state: username='Unknown', income=0, budget_for_expenses=0, expense=0, expenses=[], savings_goal=0, savings=0, currency=''). The <input> below contains the full sequence of user inputs up to the current point, separated by newlines. The <output> is the assistant's response to the *last input* in that sequence:

<input>
{inputs}
</input>

<output>
{outputs}
</output>

<reference_outputs>
{reference_outputs}
</reference_outputs>

Evaluate the <output> for the last input in the sequence, updating the state based on all prior inputs and outputs. Provide a score (True/False) and a brief comment explaining your reasoning, considering the full conversation history and resulting state changes. Score based on the meaning of the reference output, not exact wording. Update the state as follows:
- If an output includes 'Username set to X', set state.username = 'X'.
- If an output indicates a budget is created with specific values (e.g., 'Income: X CURRENCY, Savings: Y CURRENCY, Expenses: Z CURRENCY'), update state.income = X, state.savings = Y, state.budget_for_expenses = Z, state.currency = CURRENCY.
- If an output logs expenses with a total (e.g., 'Total: X CURRENCY'), update state.expense = X and append expenses to state.expenses from the input, using 'miscellaneous' for uncategorized expenses if specified.
"""

# Initialize OpenEvals evaluator
evaluator = create_llm_as_judge(
    prompt=AZA_EVAL_PROMPT,
    judge=ChatTogether(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        api_key=os.environ.get("TOGETHER_API_KEY")
    ),
    feedback_key="aza_correctness",
)

def load_test_cases_from_csv(csv_file="aza_man_eval_dataset.csv"):
    """Load test cases from a CSV file."""
    test_cases = []
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_cases.append({
                    "inputs": row["Input"],
                    "outputs": row["Output"]
                })
        return test_cases
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Please run create_test_cases_csv.py first.")
        return []
    except Exception as e:
        print(f"Error loading test cases: {e}")
        return []

def evaluate_aza_man():
    """Run evaluations using test cases from CSV, print results, and save to CSV."""
    print("Running Aza Man Evaluations with Test Cases from CSV...\n")
    
    test_cases = load_test_cases_from_csv()
    if not test_cases:
        print("No test cases loaded. Exiting.")
        return
    
    results = []
    conversation_history = []  
    
    for i, test in enumerate(test_cases, 1):
        conversation_history.append(test["inputs"])
        full_inputs = "\n".join(conversation_history)
        
        print(f"Test {i}:")
        print(f"Input: {test['inputs']}")
        print(f"Output: {test['outputs']}")
        print(f"Expected: {test['outputs']}")
        eval_result = evaluator(
            inputs=full_inputs,
            outputs=test["outputs"],
            reference_outputs=test["outputs"]
        )
        print(f"Score: {eval_result['score']}")
        print(f"Comment: {eval_result['comment']}")
        print("-" * 50)
        
        results.append({
            "Test Number": i,
            "Input": test["inputs"],
            "Output": test["outputs"],
            "Expected": test["outputs"],
            "Score": eval_result["score"],
            "Comment": eval_result["comment"]
        })
        
        conversation_history.append(test["outputs"])

    csv_file = "aza_man_eval_results.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["Test Number", "Input", "Output", "Expected", "Score", "Comment"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Evaluation results saved to {csv_file}")

if __name__ == "__main__":
    evaluate_aza_man()
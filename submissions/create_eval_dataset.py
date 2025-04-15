import csv

# Define the test cases 
test_cases = [
    {"Input": "Hi Aza man.", "Output": "Hello there! Since this is a new session, may I have your preferred name?"},
    {"Input": "Sure, call me Blaq.", "Output": "Username set to Blaq\nHi Blaq! How can I help you today?"},
    {"Input": "I want to log my expenses first.", "Output": "That's great, Blaq. But we should create a budget for you before we log those expenses. Kindly provide your income, how much you wish to save from that, and which currency I should log everything in."},
    {"Input": "I earn 750k monthly. I wish to save at least 40%.", "Output": "Okay, and what is your currency? (e.g., USD, EUR, NGN)"},
    {"Input": "NGN", "Output": "Budget created! Income: 750,000.00 NGN, Savings: 300,000.00 NGN, Expenses: 450,000.00 NGN\nYour budget is now set! How can I assist you further?"},
    {"Input": "I want to log my expenses first.", "Output": "Great! Now that your budget is set up, let's log your expenses. Please provide a list of your expenses including the amount and category for each."},
    {"Input": "Oh I have quite a lot o. I spent 80k last Tuesday. I spent 67k yesterday morning. I just spent 35,000 not long ago. I think that’s it for now.", "Output": "Hi Blaq! I’ve got your expenses: 80,000.00 NGN, 67,000.00 NGN, and 35,000.00 NGN. Could you specify the categories for each (e.g., 'Food', 'Transportation')? For now, I’ll prepare to log them as 'miscellaneous' with the 'log_expenses' tool if you don’t provide categories next."},
    {"Input": "I don’t remember the categories.", "Output": "Expenses logged! Total: 182,000.00 NGN\nAll set! What else can I help you with, Blaq?"},
    {"Input": "Wait. Am I on track?", "Output": "Hi Blaq! Let’s check if you’re on track. Your budget for expenses is 450,000.00 NGN, and you’ve spent 182,000.00 NGN so far. Result: 268,000.00 NGN\nYou have 268,000.00 NGN left, so you’re well within your budget! How can I assist you next?"},
]

# Write to CSV
csv_file = "aza_man_eval_dataset.csv"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    fieldnames = ["Input", "Output"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(test_cases)

print(f"Test cases saved to {csv_file}")
# Aza Man - AI-Powered Autonomous Financial Assistant
Aza Man is my entry for the May 2025 edition of the Global Agent Hackathon. A nimble, AI-driven financial assistant, Aza Man empowers users to manage budgets, track expenses, and achieve savings goals effortlessly. It delivers a cross-functional experience through a command-line interface (CLI) and a Streamlit web interface, deployed on Hugging Face Spaces, with seamless state persistence across platforms via SQLite.

## Table of Contents

* Vision
* Context and Gaps
* Capabilities
* AI Backbone
* Target Audience
* Design Approach
* Technical Methodology
* Evaluation Strategy
* Dataset Sources & Collection
* Dataset Description
* Dataset Processing Methodology
* Comparative Analysis
* Success/Failure Stories
* Source Credibility
* Deployment Considerations
* Monitoring and Maintenance
* Performance Metrics Analysis
* Key Results Interpretation
* Limitations
* Significance and Implications
* Implementation Insights
* Setup Guide
* Future Roadmap
* Conclusion

## Vision
Personal finance shouldn’t feel like a burden. Aza Man leverages AI to simplify budgeting, expense tracking, and goal setting, delivering an assistant that cuts through the noise—subscription-free, focused on efficiency, and accessible across multiple interfaces.

## Context and Gaps
Tools like Nigeria’s FairMoney, CowryWise, and PiggyVest, alongside global leaders Mint and YNAB, offer robust features but often demand paid subscriptions or intricate setups. CLI options like Ledger are lean but lack AI-driven interactivity. Aza Man fills these gaps by:

1. Offering free, real-time AI assistance via open-source platforms.
2. Supporting both terminal and Streamlit interfaces for diverse user preferences.
3. Requiring minimal setup with seamless state persistence across platforms.
4. Addressing gaps in conversational depth and predictive analytics, though it currently lacks multi-user support and forecasting.

## Capabilities

* Budgeting & Goals: Set income and savings targets using the budget tool.
* Expense Tracking: Log expenses with categories via the log_expenses tool.
* Smart Insights: Deliver precise calculations using the math_tool.
* Customized Experience: Retains session and cross-session memory via SQLite, accessible from both main.py (CLI) and app.py (Streamlit).
* Visual Dashboard: Provides expense distribution, savings progress, and trends via Plotly charts on Streamlit.
* Cross-Functionality: Use the same login details (user ID) to access state across terminal and web interfaces.

## AI Backbone
Aza Man harnesses free-tier AI platforms for performance and accessibility:

- Groq: Rapid inference for instant replies.
- Together AI: Open-source LLMs for affordable processing.
- OpenRouter: Flexible model access with tool-calling support.
- Built with LangChain, LangGraph, and LangSmith for graph workflow orchestration, state management, tracing, and debugging, ensuring scalability and transparency.

## Target Audience
Ideal for users seeking an AI-powered financial tool—especially those who value simplicity, cross-platform access, and no-cost solutions, including young professionals, students, and small business owners.

## Design Approach
Aza Man’s design emphasizes practicality and accessibility:

1. Armed with Tools: Uses financial tools (budget, log_expenses, math_tool) to ensure accurate computations, avoiding LLM hallucination.
2. State Persistence: Stores data in memory_agent.db (SQLite) for session continuity across CLI and Streamlit.
3. Cost Efficiency: Leverages free-tier platforms (Groq, Together AI, OpenRouter) for affordability.
Cross-Platform: Supports main.py (CLI) and app.py (Streamlit), sharing state via SQLite for a unified experience.
4. Visualization: Streamlit dashboard with Plotly for expense and savings insights.

## Technical Methodology
Aza Man’s workflow ensures seamless operation across platforms:

Session Initialization: Queries SQLite on launch. Loads prior data for the user_id or starts fresh with defaults.
Input: Users enter commands via CLI or Streamlit chat.
Processing: LangGraph directs input to the LLM, triggering tools as needed. LangSmith logs interactions.
State Management: Updates (e.g., username, expenses) are persisted to SQLite.
Output: Responses are displayed in the terminal or Streamlit UI (with streaming via st_callable_util.py).
Session Close: State is saved to SQLite on "exit" or logout.

## Evaluation Strategy
Performance is assessed using evals.py with OpenEvals:

**Metrics**:
Speed: Response time < 3 seconds (avg. 2.92s), verified via LangSmith.
Accuracy: Validated by math_tool test cases in aza_man_eval_results.csv.
Usability: Successful state saves, confirmed via check_db.py.


**Baseline**: Manual spreadsheets.
Method: evals.py runs 9 test scenarios from aza_man_eval_dataset.csv, judged by a ChatTogether model. LangSmith traces debug failures.
Results: 100% test pass rate per aza_man_eval_results.csv.

## Dataset Sources & Collection
The evaluation dataset (aza_man_eval_dataset.csv) was generated programmatically using create_eval_dataset.py, defining 9 test cases simulating user interactions (e.g., username setup, budgeting, expense logging).

## Dataset Description
aza_man_eval_dataset.csv contains:

Rows: 9 test cases.
Columns: Input (user message), Output (expected response).
Format: CSV, focused on conversational flows in Nigerian Naira (NGN).

## Dataset Processing Methodology

Creation: Script-generated with formatted financial figures (e.g., "X,XXX.00 NGN").
Cleaning: None required; dataset was curated for accuracy.
Transformation: evals.py maps inputs to outputs for evaluation.

## Comparative Analysis

FairMoney: Loan-focused, subscription-based; Aza Man is free.
PiggyVest: Savings-oriented, mobile-only; Aza Man adds conversational budgeting.
Mint: Forecasting, paid; Aza Man prioritizes simplicity.
YNAB: Detailed, complex; Aza Man is accessible.
Ledger CLI: No AI; Aza Man adds conversational AI and web UI.

## Success/Failure Stories

Success: User blaq01 set a 750,000.00 NGN budget, logged 182,000.00 NGN expenses, and confirmed 268,000.00 NGN remaining across CLI and Streamlit, with Plotly charts visualizing spending.
Failure: Early Spaces deployment lost state due to SQLite resets, resolved with local testing via check_db.py.
Lesson: Robust persistence is critical for cross-platform apps.

## Source Credibility

Tools and libraries cited in requirements.txt with versions.
APIs: Groq, Together AI, OpenRouter.

## Deployment Considerations
Deployed on Hugging Face Spaces: [Aza Man On Spaces](https://huggingface.co/spaces/Blaqadonis/AzaMan?logs=container)

Files: app.py, graph.py, configuration.py, tools.py, state.py, st_callable_util.py, utils.py, prompts.py, azaman2.png.
Secrets: API keys and variables (TOGETHER_API_KEY, OPENROUTER_API_KEY, GROQ_API_KEY, LANGCHAIN_API_KEY, PROVIDER=openrouter, MODEL=google/gemini-2.0-flash-lite-preview-02-05:free) stored securely.
Persistence: SQLite resets on Spaces restart; future plans include cloud databases.

## Monitoring and Maintenance

Metrics: Latency, tool success rate, SQLite errors via LangSmith.
Logging: Captures LLM calls, tool usage, and state updates.
Performance: Monitors API limits, adjusts PROVIDER if needed.
Maintenance: Updates requirements.txt for security and compatibility.

## Performance Metrics Analysis

Latency: 2.92s average per query (Spaces, LangSmith).
Tool Success: 100% for budget, log_expenses, math_tool.
Persistence: 100% successful SQLite saves (check_db.py).

## Key Results Interpretation

Accuracy: Precise calculations via OpenEvals.
Usability: Seamless cross-platform state sharing.
Visualization: Clear insights from Plotly charts.

## Limitations

Scalability: SQLite limits multi-user support; Spaces resets memory_agent.db.
Insight Depth: Basic tools, free-tier models limit analytics.
Trade-Offs: Free-tier AI may reduce precision vs. paid options.

## Significance and Implications
Aza Man offers a free, AI-driven alternative to costly financial apps, empowering users in regions like Nigeria. Its open-source design and Spaces deployment foster innovation in lightweight finance tools.
Implementation Insights

Challenges: API key setup, Spaces configuration.
Resources: Runs on modest hardware with internet.
Scalability: SQLite for prototype; needs cloud database for growth.
Best Practices: Use virtual environments, monitor LangSmith, test with check_state.py.

## Setup Guide

Obtain API Keys: Register at Groq, OpenRouter, Together AI, and LangSmith.
Configure .env (or Spaces Secrets):GROQ_API_KEY=<your_groq_key>
OPENROUTER_API_KEY=<your_openrouter_key>
TOGETHER_API_KEY=<your_together_key>
PROVIDER=openrouter
MODEL=google/gemini-2.0-flash-lite-preview-02-05:free
USER_ID=<your_userid>  # 4-10 chars, last 2 digits, e.g., jake00
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=<your_langsmith_key>
LANGCHAIN_PROJECT=AzaMan-2025


Install Dependencies: pip install -r requirements.txt.
Launch Locally:
CLI: python main.py
Streamlit: streamlit run app.py



## Future Roadmap

Persistence: Upgrade to PostgreSQL.
Tools: Add forecasting and internet data retrieval.
Visuals: Introduce interactive budget forecasts.
Performance: Optimize LLM calls for speed.

## Conclusion
Aza Man proves AI can simplify financial management with cross-platform functionality, rigorous evaluation, and accessible deployment. It’s fast, efficient, and user-friendly—ideal for streamlined money management. Future iterations will deepen its impact and scalability.
Tags: agents, finance, supervisorHub: #chinonsoodiakaLicense: MITSpaces: Deployed Aza Man

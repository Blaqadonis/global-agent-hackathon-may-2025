import streamlit as st
from uuid import uuid4
from langchain_core.messages import AIMessage, HumanMessage
import graph
from st_callable_util import get_streamlit_cb
import re
import os
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="Aza Man", page_icon="azaman2.png", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    :root {
        --primary-red: #FF0000;
        --dark-bg: #0A0A0A;
        --card-bg: #1A1A1A;
    }
    .stApp {
        background-color: var(--dark-bg);
        color: white;
    }
    .stChatInput input {
        background-color: var(--card-bg) !important;
        color: white !important;
        border: 1px solid var(--primary-red) !important;
    }
    .stButton>button {
        background-color: var(--primary-red) !important;
        color: white !important;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.8;
        transform: scale(1.05);
    }
    .assistant-message {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-red);
        margin: 1rem 0;
    }
    .user-message {
        background: #2A2A2A;
        padding: 1rem;
        border-radius: 10px;
        border-right: 4px solid #FFFFFF;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: var(--dark-bg) !important;
        border-right: 1px solid var(--primary-red);
    }
    .intro-text {
        text-align: center;
        font-size: 1.1rem;
        color: #CCCCCC;
        line-height: 1.6;
    }
    .active-header {
        background: var(--card-bg);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-red);
        margin-bottom: 1rem;
        text-align: center;
        font-size: 1.2rem;
    }
    .dont-show-again {
        margin-top: 15px;
        display: flex;
        align-items: center;
    }
    /* Custom dialog styling */
    [data-testid="stDialog"] {
        background: var(--card-bg);
        border-left: 4px solid var(--primary-red);
        border-radius: 10px;
        color: white;
        width: 80%;
        max-width: 500px;
    }
    </style>
""", unsafe_allow_html=True)

def invoke_our_graph(input_messages, config, callables=None):
    """Invoke the LangGraph graph with streaming support, using the checkpointer for persistence."""
    response = {"messages": []}
    for chunk in graph.graph.stream({"messages": input_messages}, config, stream_mode="updates"):
        for node, updates in chunk.items():
            if "messages" in updates and updates["messages"]:
                response["messages"].extend(updates["messages"])
                if callables and node == "call_model":
                    for msg in updates["messages"]:
                        if isinstance(msg, AIMessage):
                            for cb in callables:
                                cb.on_llm_new_token(msg.content)
    return response

def show_welcome_popup():
    # Initialize session state variables if not present
    if "hide_welcome_popup" not in st.session_state:
        st.session_state.hide_welcome_popup = False
    if "show_popup" not in st.session_state:
        st.session_state.show_popup = not st.session_state.hide_welcome_popup

    # Use st.dialog for the how-to popup for new users.
    if not st.session_state.hide_welcome_popup and st.session_state.show_popup:
        @st.dialog("Welcome to Aza Man!")
        def welcome_dialog():
            st.markdown('<h2 style="color: var(--primary-red);">Welcome to Aza Man!</h2>', unsafe_allow_html=True)
            st.markdown('<p><strong>Navigation:</strong> Use the sidebar to switch between Home, Chat, and Dashboard pages.</p>', unsafe_allow_html=True)
            st.markdown('<p><strong>Login Details:</strong> Enter a User ID (4-10 chars, ending with 2 digits, e.g., odogwu19) to start. New users can create a unique ID.</p>', unsafe_allow_html=True)
            st.markdown('<p><strong>Session Management:</strong> Sessions are saved per User ID. Click \'RETURN TO BASE\' to reset and log out. Returning users load their previous data.</p>', unsafe_allow_html=True)
            st.markdown('<p><strong>Chat Management:</strong> Type your message and click \'Send\' to interact with Aza Man.', unsafe_allow_html=True)
            st.markdown('<p><strong>New user? Start here!</strong> Create a User ID and explore the features.</p>', unsafe_allow_html=True)

            # Checkbox for "Don't show this again"
            st.markdown('<div class="dont-show-again">', unsafe_allow_html=True)
            dont_show = st.checkbox("Don't show this again")
            if dont_show:
                st.session_state.hide_welcome_popup = True
                st.session_state.show_popup = False
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        welcome_dialog()

def login_page():
    # Show welcome popup on first load
    show_welcome_popup()
    
    st.markdown("<h1 style='color: #FF0000; text-align: center;'>Welcome to Aza Man</h1>", unsafe_allow_html=True)
    st.markdown("<p class='intro-text'>Enter your User ID to begin (4-10 chars, last 2 digits, e.g., jake00)</p>", unsafe_allow_html=True)
    user_id = st.text_input("User ID", max_chars=10)
    if st.button("New user? Start here!"):
        st.session_state.show_popup = True
        st.rerun()
    
    if st.button("Login"):
        if re.match(r"^[a-zA-Z]{2,8}\d{2}$", user_id):
            # Store user_id and thread_id in session_state to persist across reruns
            st.session_state.user_id = user_id
            st.session_state.thread_id = f"thread_{user_id}"
            # Initialize config in session_state if not already set
            if "config" not in st.session_state:
                st.session_state.config = {"configurable": {"user_id": user_id, "thread_id": st.session_state.thread_id}}
            else:
                st.session_state.config["configurable"]["user_id"] = user_id
                st.session_state.config["configurable"]["thread_id"] = st.session_state.thread_id
            # Load state from checkpointer using the user's unique thread_id
            current_state = graph.graph.get_state(st.session_state.config).values or {}
            st.session_state.messages = current_state.get("messages", [])
            if current_state.get("username"):
                st.session_state.messages.append(AIMessage(content=f"Welcome back, {current_state['username']}! Your last session data is loaded. How can I assist you today?"))
            else:
                st.session_state.messages = [AIMessage(content="Welcome to Aza Man, your financial assistant! What is your name?")]
            st.session_state.page = "Home"
            st.rerun()
        else:
            st.error("Invalid User ID! Must be 4-10 characters, ending with 2 digits (e.g., odogwu19).")

def landing_page():
    st.markdown("<h1 style='color: #FF0000; text-align: center; font-family: Arial;'>Aza Man</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FFFFFF;'>AI-Powered Financial Guardian</h3>", unsafe_allow_html=True)
    st.image('azaman2.png', use_container_width=True)
    st.markdown("<div class='intro-text'>Welcome to your personal financial command center. Select 'Chat' from the sidebar to begin.</div>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #FFFFFF;'>Key Features</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div style='text-align: center;'><span style='font-size: 2rem;'>🔥</span><h3>Smart Budgeting</h3><p>Plan your finances with AI precision</p></div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align: center;'><span style='font-size: 2rem;'>💸</span><h3>Expense Tracking</h3><p>Monitor spending in real-time</p></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div style='text-align: center;'><span style='font-size: 2rem;'>📈</span><h3>Savings Goals</h3><p>Set and achieve financial targets</p></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; margin-top: 2rem;'><small>Developed by </small><a href='https://www.linkedin.com/in/chinonsoodiaka/' style='color: var(--primary-red); text-decoration: none; font-weight: bold;'>🅱🅻🅰🆀</a></div>", unsafe_allow_html=True)

def chat_interface():
    if "config" not in st.session_state:
        st.error("Please log in first!")
        return
    
    # Display **active** banner
    st.markdown(
        """
        <div class='active-header'>
            <div style='color: var(--primary-red); font-weight: bold;'>AZA:</div>
            **Aza Man is NOW ACTIVE**. How can I assist you today?
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Load state 
    current_state = graph.graph.get_state(st.session_state.config).values or {}
    st.session_state.messages = current_state.get("messages", [])
    
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if isinstance(msg, AIMessage):
                content = re.sub(r'<[^>]+>\s*', '', msg.content, flags=re.DOTALL).strip()
                # Skip the "Aza Man is NOW ACTIVE" message if it exists in the history
                if "Aza Man is NOW ACTIVE" in content:
                    continue
                st.markdown(f"<div class='assistant-message'><div style='color: var(--primary-red); font-weight: bold;'>AZA:</div>{content}</div>", unsafe_allow_html=True)
            elif isinstance(msg, HumanMessage):
                st.markdown(f"<div class='user-message'><div style='color: white; font-weight: bold;'>YOU:</div>{msg.content}</div>", unsafe_allow_html=True)

    prompt = st.text_input("Send secure message...", placeholder="Type your message here...", key="chat_input")
    if st.button("Send"):
        if prompt:
            new_message = [HumanMessage(content=prompt)]
            with st.spinner("**...Thinking...**"):
                st_callback = get_streamlit_cb(chat_container)
                response = invoke_our_graph(new_message, st.session_state.config, callables=[st_callback])
                # Update messages from checkpointer
                st.session_state.messages = graph.graph.get_state(st.session_state.config).values["messages"]
                st.rerun()

def dashboard_page():
    if "config" not in st.session_state:
        st.error("Please log in first!")
        return
    
    # Load state 
    current_state = graph.graph.get_state(st.session_state.config).values or {}
    
    st.subheader("Summary Metrics")
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Total Income", f"{current_state.get('income', 0.0):,.2f} {current_state.get('currency', '')}")
    with col2: st.metric("Total Expenses", f"{current_state.get('expense', 0.0):,.2f} {current_state.get('currency', '')}")
    with col3: st.metric("Remaining Budget", f"{current_state.get('budget_for_expenses', 0.0) - current_state.get('expense', 0.0):,.2f} {current_state.get('currency', '')}")
    with col4: st.metric("Current Savings", f"{current_state.get('savings', 0.0):,.2f} {current_state.get('currency', '')}")

    st.subheader("Savings Progress")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number", value=current_state.get('savings', 0.0), domain={'x': [0, 1], 'y': [0, 1]},
        title={"text": "Savings vs Goal"}, gauge={"axis": {"range": [0, current_state.get('savings_goal', 0.0)]}, "bar": {"color": "green"}}
    ))
    st.plotly_chart(fig_gauge)

    st.subheader("Expense Distribution")
    expenses = current_state.get('expenses', [])
    if expenses:
        fig_pie = px.pie(values=[e["amount"] for e in expenses], names=[e["category"] for e in expenses], color_discrete_sequence=px.colors.sequential.Reds)
        st.plotly_chart(fig_pie)
    else:
        st.write("No expenses logged yet.")

    st.subheader("Expense Trends")
    if expenses:
        dates = [datetime.now().date() if 'date' not in e else datetime.strptime(e['date'], '%Y-%m-%d').date() for e in expenses]
        amounts = [e["amount"] for e in expenses]
        fig_line = px.line(x=dates, y=amounts, labels={"x": "Date", "y": f"Amount ({current_state.get('currency', '')})"})
        st.plotly_chart(fig_line)
    else:
        st.write("No expense trends to display yet.")

def main():
    if "page" not in st.session_state:
        st.session_state.page = "Login"

    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox("Select Page", ["Home", "Chat", "Dashboard"], disabled=(st.session_state.page == "Login"))
    if st.session_state.page == "Login":
        login_page()
    elif page == "Home":
        landing_page()
    elif page == "Chat":
        chat_interface()
    elif page == "Dashboard":
        dashboard_page()

    if st.sidebar.button("◀ RETURN TO BASE"):
        st.session_state.clear()
        st.session_state.page = "Login"
        st.rerun()

if __name__ == "__main__":
    main()
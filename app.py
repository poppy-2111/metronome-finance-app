import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# Page setup
st.set_page_config(page_title="Metronome", page_icon="💰", layout="wide")

# Session-wide datasets
if "finance_data" not in st.session_state:
    st.session_state.finance_data = pd.DataFrame(columns=["date", "spending", "saving"])
if "needs_wants" not in st.session_state:
    st.session_state.needs_wants = pd.DataFrame(columns=["item", "type"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Colors
PRIMARY_COLOR = "#6A5ACD"
SECONDARY_COLOR = "#F8FAFF"
WARNING_COLOR = "#FF5C5C"

st.markdown(f"""
<style>
    body {{ background-color: {SECONDARY_COLOR}; }}
    .stButton>button {{ background-color: {PRIMARY_COLOR} !important; color: white !important; border-radius: 8px; }}
</style>
""", unsafe_allow_html=True)

st.title("Metronome — Personal Finance Tracker")

# Sidebar
menu = ["Welcome", "Add Data", "Graph", "Calendar", "Needs vs Wants", "About", "Chatbot"]
choice = st.sidebar.selectbox("Navigate", menu)

# Chatbot response
def chatbot_response(user_input: str) -> str:
    user_input = user_input.lower()
    if any(w in user_input for w in ["hi", "hello", "hey"]):
        return "Hello! 👋 I'm your finance buddy. Ask me how to save or what counts as a need."
    if "save" in user_input:
        return "Try saving 15–25% of your income. Even ₹50 daily adds up!"
    if "spend" in user_input:
        return "Track every purchase. Cut one 'want' per week to see real change."
    if "need" in user_input:
        return "Needs are essentials: food, rent, bills, transport."
    if "want" in user_input:
        return "Wants are extras: gadgets, snacks, subscriptions."
    return "I’m still learning — try: 'How can I save?' or 'What is a need?'"

# Pages
if choice == "Welcome":
    st.header("Welcome 👋")
    st.write("Use 'Add Data' to enter your spending & saving. Then view graphs, calendar, and chatbot tips.")
elif choice == "Add Data":
    st.header("Enter Your Finance Data")
    with st.form("data_entry"):
        date = st.date_input("Date", datetime.date.today())
        spending = st.number_input("Spending (₹)", min_value=0, step=10)
        saving = st.number_input("Saving (₹)", min_value=0, step=10)
        submitted = st.form_submit_button("Add record")
    if submitted:
        new_row = {"date": pd.to_datetime(date), "spending": spending, "saving": saving}
        st.session_state.finance_data = pd.concat([st.session_state.finance_data, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added record for {date}")
    st.subheader("Current Data")
    st.dataframe(st.session_state.finance_data)
elif choice == "Graph":
    st.header("Spending vs Saving Graph")
    if st.session_state.finance_data.empty:
        st.warning("No data yet. Please add some in 'Add Data'.")
    else:
        df = st.session_state.finance_data
        total_spend = df["spending"].sum()
        total_save = df["saving"].sum()
        st.write(f"Total Spending: **{total_spend}**  |  Total Saving: **{total_save}**")
        if total_spend > total_save:
            st.markdown(f"<h4 style='color:{WARNING_COLOR};'>Warning: spending > saving</h4>", unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(df["date"], df["spending"], label="Spending", linewidth=2)
        ax.plot(df["date"], df["saving"], label="Saving", linewidth=2)
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount")
        ax.legend()
        plt.tight_layout()
        st.pyplot(fig)
elif choice == "Calendar":
    st.header("Check Data by Date")
    if st.session_state.finance_data.empty:
        st.warning("No data yet. Add some first.")
    else:
        df = st.session_state.finance_data
        date_selected = st.date_input("Pick a date", df["date"].min().date())
        row = df[df["date"] == pd.to_datetime(date_selected)]
        if not row.empty:
            spend = int(row["spending"].iloc[0])
            save = int(row["saving"].iloc[0])
            st.write(f"On {date_selected}: 💸 Spending {spend} | 💰 Saving {save}")
        else:
            st.info("No record for this date.")
elif choice == "Needs vs Wants":
    st.header("Needs vs Wants")
    with st.form("needs_wants_form"):
        item = st.text_input("Enter item (e.g., Rent, Netflix, Groceries)")
        category = st.radio("Select category", ["Need", "Want"], horizontal=True)
        submitted = st.form_submit_button("Add item")
    if submitted and item.strip() != "":
        new_row = {"item": item.strip(), "type": category}
        st.session_state.needs_wants = pd.concat([st.session_state.needs_wants, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added '{item}' as {category}")
    st.subheader("Your Needs")
    needs_df = st.session_state.needs_wants[st.session_state.needs_wants["type"] == "Need"]
    if not needs_df.empty:
        st.table(needs_df[["item"]].reset_index(drop=True))
    else:
        st.info("No Needs added yet.")
    st.subheader("Your Wants")
    wants_df = st.session_state.needs_wants[st.session_state.needs_wants["type"] == "Want"]
    if not wants_df.empty:
        st.table(wants_df[["item"]].reset_index(drop=True))
    else:
        st.info("No Wants added yet.")
elif choice == "About":
    st.header("About this project")
    st.write("This app helps you track spending & saving, visualize progress, and chat with a finance helper.")
elif choice == "Chatbot":
    st.header("Finance Chatbot & Needs vs Wants Advisor")
    bot_names = ["Lilly","Leo","Charlotte","James","William","John","Jonny","Joppy","Jane","Jiva","Legend of the Universe","God","Cookie","Daisy","Pinky"]
    selected_bot = st.selectbox("Select your chatbot's name", bot_names)
    st.write(f"You are now chatting with **{selected_bot}** 🤖")
    with st.form("needs_wants_form_chatbot"):
        item = st.text_input("Enter an item (e.g., Rent, Netflix, Groceries)", key="item_input_chatbot")
        category = st.radio("Select category", ["Need", "Want"], horizontal=True)
        submitted = st.form_submit_button("Add item")
    if submitted and item.strip() != "":
        new_row = {"item": item.strip(), "type": category}
        st.session_state.needs_wants = pd.concat([st.session_state.needs_wants, pd.DataFrame([new_row])], ignore_index=True)
        st.success(f"Added '{item}' as {category}")
        st.session_state.item_input_chatbot = ""
    st.subheader("Your Needs")
    needs_df = st.session_state.needs_wants[st.session_state.needs_wants["type"]=="Need"]
    if not needs_df.empty:
        st.table(needs_df[["item"]].reset_index(drop=True))
    else:
        st.info("No Needs added yet.")
    st.subheader("Your Wants")
    wants_df = st.session_state.needs_wants[st.session_state.needs_wants["type"]=="Want"]
    if not wants_df.empty:
        st.table(wants_df[["item"]].reset_index(drop=True))
    else:
        st.info("No Wants added yet.")
    st.subheader(f"Ask {selected_bot} about your items")
    def generate_advice(item, category):
        if category=="Need":
            return f"{selected_bot}: '{item}' is essential. Prioritize it in your budget!"
        else:
            return f"{selected_bot}: '{item}' is a Want. Consider it only if your Needs are well-covered."
    with st.form("chat_form_chatbot"):
        chat_input = st.text_input("Ask about an item in your list")
        chat_submitted = st.form_submit_button("Send")
    if chat_submitted and chat_input.strip()!="":
        df = st.session_state.needs_wants
        match =

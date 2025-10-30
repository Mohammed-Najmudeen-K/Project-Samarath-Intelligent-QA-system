import streamlit as st
import pandas as pd

# Load datasets
rain = pd.read_csv("Sub_Division_IMD_2017.csv")
agri = pd.read_csv("datafile (1).csv")

# Clean columns
rain.columns = [c.strip().lower() for c in rain.columns]
agri.columns = [c.strip().lower() for c in agri.columns]

# Preprocess column names based on your dataset
if "sub-division" in rain.columns:
    rain.rename(columns={"sub-division": "state"}, inplace=True)
if "yield (quintal/ hectare)" in agri.columns:
    agri.rename(columns={"yield (quintal/ hectare)": "yield"}, inplace=True)

# --- Core Question Answering Function ---
def answer_question(query):
    query = query.lower()

    # Compare rainfall
    if "compare rainfall" in query:
        words = query.split()
        states = [w for w in words if w.istitle()]
        if len(states) >= 2:
            s1, s2 = states[0], states[1]
            year = 2017
            r1 = rain[rain['state'].str.contains(s1, case=False, na=False)]
            r2 = rain[rain['state'].str.contains(s2, case=False, na=False)]

            if not r1.empty and not r2.empty:
                avg1 = r1.iloc[:, -1].mean()
                avg2 = r2.iloc[:, -1].mean()
                return (f"Average annual rainfall in {s1}: {avg1:.2f} mm\n"
                        f"Average annual rainfall in {s2}: {avg2:.2f} mm\n"
                        f"Source: Sub_Division_IMD_2017.csv")
            else:
                return "Data not found for given states."

    # Top crops
    elif "top" in query and "crops" in query:
        for state in agri["state"].unique():
            if state.lower() in query:
                data = agri[agri["state"].str.contains(state, case=False, na=False)]
                top = data.groupby("crop")["yield"].mean().sort_values(ascending=False).head(3)
                return f"Top 3 crops in {state} based on yield:\n{top}\nSource: datafile.csv"

    # Default
    else:
        return "Sorry, I couldn’t understand the question."

# --- Streamlit Frontend ---
st.set_page_config(page_title="Project Samarth Q&A", page_icon="🌾")
st.title("🌦️ Project Samarth — Intelligent Q&A System")
st.markdown("Ask natural questions like:")
st.markdown("""
• Compare rainfall between Tamil Nadu and Kerala in 2017  
• Top 3 crops in Maharashtra  
• Correlation between rainfall and yield for Rice in 2017  
""")

query = st.text_input("💬 Ask your question here:")

if st.button("Get Answer"):
    if query:
        answer = answer_question(query)
        st.success(answer)
    else:
        st.warning("Please enter a question.")

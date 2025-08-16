import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="General Discussion League", layout="wide")

# --- Home Page Content ---
st.title("2025 General Discussions Fantasy Premier League")
st.markdown("""
Welcome to the 2025/2026 General Discussion Fantasy Premier League.
""")

st.image("https://fantasy.premierleague.com/static/media/fpl-logo.7e5f1f7f.png", width=200)

st.markdown("### 🔥 Features")
st.markdown("""
- 📊 View live **Overall League Standings**  
- 📆 Analyze performance in **4-week Block Tables**  
- 👤 Explore detailed **Player Profiles**  
- 🧠 Plan ahead with gameweek insights and chip usage
""")

st.markdown("### 🚀 Get Started")
st.markdown("Use the sidebar to navigate between pages.")

# Optional: Quick Navigation Buttons (requires Streamlit 1.25+)
if st.button("Go to Overall Table"):
    st.switch_page("pages/1_Overall_Table.py")

if st.button("Go to Block Table"):
    st.switch_page("pages/2_Block_Table.py")

if st.button("Go to Players"):
    st.switch_page("pages/3_Players.py")

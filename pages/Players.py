import streamlit as st
import pandas as pd
from utils.api_requests import get_gameweek_points
import datetime

# --- Page Config ---
st.set_page_config(page_title="Player Team", layout="wide")

# --- Check for Selected Manager ---
if "selected_entry_id" not in st.session_state or "selected_manager_name" not in st.session_state:
    st.error("No manager selected. Please go back and choose a manager.")
    st.stop()

entry_id = st.session_state.selected_entry_id
manager_name = st.session_state.selected_manager_name

# --- Determine Current Gameweek ---
today = datetime.datetime.today()
current_gw = 1 if today.month < 8 else min(((today - datetime.datetime(today.year, 8, 1)).days // 7) + 1, 38)

# --- Fetch Team Picks ---
picks_data = get_gameweek_points(entry_id, current_gw)
picks = picks_data.get("picks", []) if picks_data else []

# --- Display Team ---
st.title(f"👤 {manager_name}'s Team — Gameweek {current_gw}")

if picks:
    team_df = pd.DataFrame([{
        "Player ID": pick["element"],
        "Position": pick["position"],
        "Captain": pick["is_captain"],
        "Vice Captain": pick["is_vice_captain"]
    } for pick in picks])
    st.dataframe(team_df)
else:
    st.warning("Team data not available. The season may not have started or the entry ID is invalid.")

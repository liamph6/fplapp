import streamlit as st
import pandas as pd
from utils.api_requests import get_league_standings, get_player_summary

# --- Page Config ---
st.set_page_config(page_title="Overall League Table", layout="wide")

# --- League ID ---
LEAGUE_ID = 888020

# --- Fetch League Data ---
league_data = get_league_standings(LEAGUE_ID)

# --- Build Standings Table ---
st.title("General Discussions Standings")

standings = league_data['standings']['results'] if league_data and league_data['standings']['results'] else None

if standings:
    rows = []
    for team in standings:
        entry_id = team['entry']
        player_data = get_player_summary(entry_id)
        overall_rank = player_data.get("summary_overall_rank", "N/A") if player_data else "N/A"

        rows.append({
            "Rank": team['rank'],
            "Team Name": team['entry_name'],
            "Manager": team['player_name'],
            "Points": team['total'],
            "Overall Rank": overall_rank
        })

    df = pd.DataFrame(rows)
else:
    st.warning("Live data not available. Using mock data for design purposes.")
    df = pd.DataFrame([
        {
            "Rank": 1,
            "Team Name": "Cesc, Drogs and Ashley Cole",
            "Manager": "Liam Hennigan",
            "Points": 812,
            "Overall Rank": 12345
        },
        {
            "Rank": 2,
            "Team Name": "iniesta fc",
            "Manager": "Art Moore",
            "Points": 798,
            "Overall Rank": 23456
        },
        {
            "Rank": 3,
            "Team Name": "Beamos",
            "Manager": "Adam Beamish",
            "Points": 790,
            "Overall Rank": 34567
        }
    ])

# --- Display Table Without Index ---
st.dataframe(df, use_container_width=True, hide_index=True)

# --- Select Manager to View Team ---
selected_manager = st.selectbox("Select a manager to view their team", df["Manager"])

# Find entry ID from standings or mock data
if standings:
    selected_entry = next((team for team in standings if team['player_name'] == selected_manager), None)
    entry_id = selected_entry['entry'] if selected_entry else None
else:
    # Fallback mock entry IDs
    mock_entry_ids = {
        "Liam Hennigan": 2563143,
        "Art Moore": 6051733,
        "Adam Beamish": 6366332
    }
    entry_id = mock_entry_ids.get(selected_manager)

# Store in session and navigate
if st.button("View Team"):
    st.session_state.selected_entry_id = entry_id
    st.session_state.selected_manager_name = selected_manager
    st.switch_page("pages/Players.py")





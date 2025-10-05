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

def find_best_gameweek(league_id):
    standings = get_league_standings(league_id)['standings']['results']
    best_score = 0
    best_entry = None
    best_gw = None

    for manager in standings:
        history = get_manager_history(manager['entry'])['current']
        for gw_data in history:
            if gw_data['points'] > best_score:
                best_score = gw_data['points']
                best_entry = manager['entry']
                best_gw = gw_data['event']

    return best_entry, best_gw, best_score

def display_team(manager_id, gw):
    picks = get_manager_team(manager_id, gw)
    player_map = get_player_name_map()

    st.subheader(f"Gameweek {gw} Team")
    st.write(f"Chips used: {picks.get('active_chip', 'None')}")
    st.write(f"Captain ID: {picks['picks'][0]['captain']}")

    team_data = []
    for pick in picks['picks']:
        player_name = player_map.get(pick['element'], "Unknown")
        team_data.append({
            "Player": player_name,
            "Is Captain": pick['is_captain'],
            "Is Vice": pick['is_vice_captain'],
            "Multiplier": pick['multiplier']
        })

    df = pd.DataFrame(team_data)
    st.dataframe(df)

# Streamlit UI
st.title("🏆 Best FPL Gameweek in League 888020")

with st.spinner("Fetching data..."):
    manager_id, gw, score = find_best_gameweek(LEAGUE_ID)
    st.success(f"Best Gameweek: GW {gw} by Manager {manager_id} with {score} points")
    display_team(manager_id, gw)

import streamlit as st
import pandas as pd
import requests
import datetime
from utils.api_requests import get_league_standings, get_gameweek_points, get_current_gameweek, get_player_summary

# --- Page Config ---
st.set_page_config(page_title="Block League Table", layout="wide")

# --- League ID ---
LEAGUE_ID = 888020

# --- Determine Current Gameweek ---
today = datetime.datetime.today()
current_gw = get_current_gameweek()

# --- Calculate Block Range ---
block_start = ((current_gw - 1) // 4) * 4 + 1
block_end = min(block_start + 3, 38)
block_range = list(range(block_start, block_end + 1))

st.title(f"🧱 Block Table — Gameweeks {block_start} to {block_end}")

# --- Fetch League Data ---
league_data = get_league_standings(LEAGUE_ID)
standings = league_data['standings']['results'] if league_data and league_data['standings']['results'] else None

if not standings:
    st.error("❌ Unable to retrieve live league data. Please check your connection or try again later.")
    st.stop()

# --- Load FPL Player & Team Metadata ---
players_url = "https://fantasy.premierleague.com/api/bootstrap-static/"
players_response = requests.get(players_url)
players_data = players_response.json()

# Map player ID to name, position, team ID, and current GW points
player_map = {
    player["id"]: {
        "name": f"{player['first_name']} {player['second_name']}",
        "position": player["element_type"],  # 1=GK, 2=DEF, 3=MID, 4=FWD
        "team_id": player["team"],
        "points": player["event_points"]
    }
    for player in players_data["elements"]
}

# Map team ID to team code (used for badge URL)
team_map = {
    team["id"]: team["code"]
    for team in players_data["teams"]
}

# --- Calculate Block Points ---
block_scores = []

for team in standings:
    entry_id = team['entry']
    manager_name = team['player_name']
    team_name = team['entry_name']
    total_block_points = 0

    for gw in block_range:
        gw_data = get_gameweek_points(entry_id, gw)
        if gw_data and "entry_history" in gw_data:
            total_block_points += gw_data["entry_history"].get("points", 0)

    block_scores.append({
        "Manager": manager_name,
        "Team Name": team_name,
        "Block Points": total_block_points,
        "Entry ID": entry_id
    })

# --- Sort by Block Points ---
block_scores = sorted(block_scores, key=lambda x: x["Block Points"], reverse=True)

# --- Display Each Manager's Team ---
for i, team in enumerate(block_scores, start=1):
    entry_id = team["Entry ID"]
    manager_name = team["Manager"]
    team_name = team["Team Name"]
    block_points = team["Block Points"]

    with st.expander(f"#{i} — {manager_name} ({team_name}) — {block_points} pts"):
        st.markdown(f"### Gameweek {current_gw} Team Formation")

        picks_data = get_gameweek_points(entry_id, current_gw)
        picks = picks_data.get("picks", []) if picks_data else []

        if not picks:
            st.warning("Team data not available.")
            continue

        # Organize players by position
        formation = {1: [], 2: [], 3: [], 4: []}  # GK, DEF, MID, FWD
        captain_id = picks_data.get("captain")
        vice_captain_id = picks_data.get("vice_captain")

        for pick in picks:
            player_id = pick["element"]
            info = player_map.get(player_id)

            if not info:
                continue

            team_id = info["team_id"]
            team_code = team_map.get(team_id, 1)
            badge_url = f"https://resources.premierleague.com/premierleague/badges/t{team_code}.png"

            player_card = {
                "name": info["name"],
                "photo": badge_url,
                "points": info["points"],
                "is_captain": player_id == captain_id,
                "is_vice": player_id == vice_captain_id
            }

            if pick["position"] <= 11:
                formation[info["position"]].append(player_card)

        # Display formation
        def display_line(players, label):
            if not players:
                return
            st.markdown(f"**{label}**")
            cols = st.columns(len(players))
            for col, player in zip(cols, players):
                caption = player["name"]
                if player["is_captain"]:
                    caption += " 🧢"
                elif player["is_vice"]:
                    caption += " 🎩"
                col.markdown(
                    f"""
                    <div style='text-align:center;'>
                        <img src="{player['photo']}" width="80"><br>
                        <span style='font-size:0.9em;'>{caption}</span><br>
                        <span style='font-size:0.85em; color:gray;'>Points: {player['points']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        display_line(formation[1], "🧤 Goalkeeper")
        display_line(formation[2], "🛡️ Defenders")
        display_line(formation[3], "🎯 Midfielders")
        display_line(formation[4], "⚔️ Forwards")


import streamlit as st
import pandas as pd
import requests
from utils.api_requests import get_league_standings, get_player_summary, get_current_gameweek, get_gameweek_points, get_manager_history, get_manager_team

# --- Page Config ---
st.set_page_config(page_title="Overall League Table", layout="wide")

# --- League ID ---
LEAGUE_ID = 888020

BASE_URL = "https://fantasy.premierleague.com/api"

url = f"{BASE_URL}/bootstrap-static/"

# --- Fetch League Data ---
league_data = get_league_standings(LEAGUE_ID)

# --- Build Standings Table ---
st.title("General Discussions Standings")

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

# --- Display Each Manager's Team ---
for team in standings:
    entry_id = team['entry']
    manager_name = team['player_name']
    team_name = team['entry_name']
    total_points = team['total']
    rank = team['rank']

    with st.expander(f"#{rank} — {manager_name} ({team_name}) — {total_points} pts"):
        current_gw = get_current_gameweek()
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
            team_code = team_map.get(team_id, 1)  # fallback to 1 if missing
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
        st.markdown(f"### Gameweek {current_gw} Team Formation")

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

def get_player_data():
    url = f"{BASE_URL}/bootstrap-static/"
    return requests.get(url).json()['elements']

def get_player_gw_data(gw):
    url = f"{BASE_URL}/event/{gw}/live/"
    return requests.get(url).json()['elements']

def get_player_points_map(gw):
    gw_data = get_player_gw_data(gw)
    return {p['id']: p['stats']['total_points'] for p in gw_data}


def get_player_info_map():
    players = get_player_data()
    return {
        p['id']: {
            "name": f"{p['first_name']} {p['second_name']}",
            "position": p['element_type'],  # 1: GK, 2: DEF, 3: MID, 4: FWD
            "team_id": p['team']
        }
        for p in players
    }

def get_team_code_map():
    url = f"{BASE_URL}/bootstrap-static/"
    teams = requests.get(url).json()['teams']
    return {team['id']: team['code'] for team in teams}

def get_player_name_map():
    players = get_player_data()
    return {p['id']: f"{p['first_name']} {p['second_name']}" for p in players}

def find_best_gameweek(LEAGUE_ID):
    standings = get_league_standings(LEAGUE_ID)['standings']['results']
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
    picks_data = get_manager_team(manager_id, gw)
    picks = picks_data.get("picks", []) if picks_data else []
    if not picks:
        st.warning("Team data not available.")
        return

    player_info_map = get_player_info_map()
    team_code_map = get_team_code_map()
    points_map = get_player_points_map(gw)

    captain_id = next((p['element'] for p in picks if p['is_captain']), None)
    vice_captain_id = next((p['element'] for p in picks if p['is_vice_captain']), None)

    formation = {1: [], 2: [], 3: [], 4: []}  # GK, DEF, MID, FWD

    for pick in picks:
        player_id = pick['element']
        info = player_info_map.get(player_id)
        if not info:
            continue

        team_code = team_code_map.get(info['team_id'], 1)
        badge_url = f"https://resources.premierleague.com/premierleague/badges/t{team_code}.png"
        base_points = points_map.get(player_id, 0)
        total_points = base_points * pick['multiplier']

        player_card = {
            "name": info['name'],
            "photo": badge_url,
            "points": total_points,
            "is_captain": player_id == captain_id,
            "is_vice": player_id == vice_captain_id
        }

        if pick["position"] <= 11:
            formation[info["position"]].append(player_card)

    st.markdown(f"### Gameweek {gw} Team Formation")
    st.write(f"Chips used: {picks_data.get('active_chip', 'None')}")

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



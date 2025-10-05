
import streamlit as st
import requests

@st.cache_data(ttl=3600)
def get_league_standings(league_id):
    url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings/"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_player_summary(entry_id):
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_gameweek_points(entry_id, gw):
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/event/{gw}/picks/"
    res = requests.get(url)
    return res.json() if res.status_code == 200 else None

@st.cache_data(ttl=3600)
def get_current_gameweek():
    response = requests.get("https://fantasy.premierleague.com/api/bootstrap-static/")
    data = response.json()
    current_gw = next((event['id'] for event in data['events'] if event['is_current']), None)
    return current_gw

@st.cache_data(ttl=3600)
def get_manager_history(entry_id):
    url = f"https://fantasy.premierleague.com/api/entry/{entry_id}/history/"
    response = requests.get(url)
    return response.json()

@st.cache_data(ttl=3600)
def get_manager_team(manager_id, gw):
    url = f"https://fantasy.premierleague.com/api/entry/{manager_id}/event/{gw}/picks/"
    return requests.get(url).json()

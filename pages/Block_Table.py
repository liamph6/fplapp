import requests
from datetime import datetime
import sys
from utils.api_requests import get_league_standings, get_player_summary, get_manager_history, get_current_gameweek
import streamlit as st


def calculate_block_points(history, block_start, block_end):
    return sum(gw['points'] for gw in history['current'] if block_start <= gw['event'] <= block_end)

LEAGUE_ID = '888020'
BLOCK_SIZE = 4

def main():

    st.title("Current Block standings") 	


    current_gw = get_current_gameweek()
    if not current_gw:
        print("Could not determine current gameweek.")
        sys.exit(1)

    block_start = ((current_gw - 1) // BLOCK_SIZE) * BLOCK_SIZE + 1
    block_end = block_start + BLOCK_SIZE - 1
    print(f"\n📦 Block Gameweeks: {block_start} to {block_end}\n")

    standings = get_league_standings(LEAGUE_ID)
    managers = standings['standings']['results']

    block_table = []

    for manager in managers:
        entry_id = manager['entry']
        name = f"{manager['player_name']} ({manager['entry_name']})"
        history = get_manager_history(entry_id)
        block_points = calculate_block_points(history, block_start, block_end)
        block_table.append((name, block_points))

    # Sort by block points descending
    block_table.sort(key=lambda x: x[1], reverse=True)

    st.table(block_table)

if __name__ == "__main__":
    main()

import streamlit as st
import requests
import pandas as pd
from collections import defaultdict

FPL_BASE = "https://fantasy.premierleague.com/api"

league_id = 888020

def get_bootstrap():
    return requests.get(f"{FPL_BASE}/bootstrap-static/").json()


def get_league_standings(league_id, page=1):
    url = f"{FPL_BASE}/leagues-classic/{league_id}/standings/?page_standings={page}"
    return requests.get(url).json()


def get_entry_history(entry_id):
    url = f"{FPL_BASE}/entry/{entry_id}/history/"
    return requests.get(url).json()


def load_all_league_entries(league_id):
    """Load all managers from a classic league"""
    entries = []
    page = 1

    while True:
        data = get_league_standings(league_id, page)
        results = data["standings"]["results"]
        entries.extend(results)

        if page >= data["standings"]["total_pages"]:
            break
        page += 1

    return entries


def calculate_block_scores(entry_id):
    """
    Returns a dict:
    {
        block_number: total_points_in_block
    }
    """
    history = get_entry_history(entry_id)["current"]

    block_scores = defaultdict(int)

    for gw in history:
        block = (gw["event"] - 1) // 4 + 1
        block_scores[block] += gw["points"]

    return block_scores


def block_winners_page():
    st.title("🏆 FPL Block Winners")

    league_id = st.number_input(
        "Enter Classic League ID",
        min_value=1,
        step=1
    )

    if not league_id:
        return

    with st.spinner("Loading league data..."):
        entries = load_all_league_entries(league_id)

    st.success(f"Loaded {len(entries)} managers")

    # Store block results
    blocks = defaultdict(list)

    with st.spinner("Calculating block scores..."):
        for e in entries:
            entry_id = e["entry"]
            name = e["entry_name"]
            player_name = f"{e['player_name']}"

            block_scores = calculate_block_scores(entry_id)

            for block, score in block_scores.items():
                blocks[block].append({
                    "entry_id": entry_id,
                    "team": name,
                    "manager": player_name,
                    "score": score
                })

    winners = defaultdict(int)
    seconds = defaultdict(int)

    for block, results in blocks.items():
        df = pd.DataFrame(results).sort_values("score", ascending=False)

        if len(df) >= 1:
            winners[df.iloc[0]["manager"]] += 1
        if len(df) >= 2:
            seconds[df.iloc[1]["manager"]] += 1

    summary = []

    all_managers = set(winners.keys()) | set(seconds.keys())

    for manager in all_managers:
        summary.append({
            "Manager": manager,
            "Blocks Won": winners.get(manager, 0),
            "Second Place Finishes": seconds.get(manager, 0)
        })

    summary_df = (
        pd.DataFrame(summary)
        .sort_values(["Blocks Won", "Second Place Finishes"], ascending=False)
        .reset_index(drop=True)
    )

    st.subheader("📊 Block Winners Summary")
    st.dataframe(summary_df, use_container_width=True)

    st.caption("A block is every 4 gameweeks (1–4, 5–8, etc.)")

block_winners_page()


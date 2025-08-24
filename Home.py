import streamlit as st

# --- Page Config ---
st.set_page_config(page_title="General Discussion League", layout="wide")
people = [
    {
        "name": "Liam Hennigan",
        "photo": "https://randomuser.me/api/portraits/women/44.jp",
        "description": "Extremely proficient in both data analytics and football, Liam is the heavy favourite to win the fantasy premier league this year. Regarded as having one of the most incredible minds in fantasy football today"
    },
    {
        "name": "Art Moore",
        "photo": "utils/images/Art.jpg",
        "description": "A die hard West Ham fan and a die hard competitor, Art's bizarre picks have him tipped to be everywhere from the top of the league to the bottom at some point this year."
    },
    {
        "name": "Iarfhlaith Farrell",
        "photo": "utils/images/Iarfhlaith.jpg",
        "description": "A truly deluded Liverpool fan. However, was one of the stronger competitors in the league in the last season"
    },
    {
        "name": "Adam Beamish",
        "photo": "utils/images/Adam.jpg",
        "description": "Usually A midtable competitor, no outlandish picks, just solid and calculated fanasy premier league gameplay"
    },
    {
        "name": "Diarmaid Phelan",
        "photo": "",
        "description": "Diarmaid was very lucky to bypass the fpl rules and rejoin the league this year having not submitted a sufficient forfeit from last year. With the pending forfeit looming over his head, can he be successfull this year?"
    },
    {
        "name": "Ben Donovan",
        "photo": "utils/images/Ben.jpg",
        "description": "Ben tends to go for the differential strategy, picking a lot of uncommon players. A bold and aggressive strategy that has not worked well for him in 3 years"
    },
    {
        "name": "Jack Cardoso Murphy",
        "photo": "utils/images/Javk.jpg",
        "description": "A decent competitor, has somehow managed to win some silverware in the past few years"
    },
    {
        "name": "Stephen Forde",
        "photo": "https://randomuser.me/api/portraits/women/68.jpg",
        "description": "Exclusively watches football through twitter"
    },
    {
        "name": "Sam Lilburn",
        "photo": "https://randomuser.me/api/portraits/women/68.jpg",
        "description": "Exclusively watches football through instagram"
    },
    {
        "name": "Hugh Jeffrey",
        "photo": "https://randomuser.me/api/portraits/women/68.jpg",
        "description": "Hugh enjoys to watch football. However, He puts together truly absimal fantasy premier league squads."
    }
]
# --- Home Page Content ---
st.title("2025 General Discussions Fantasy Premier League")
st.markdown("""
Welcome to the 2025/2026 General Discussion Fantasy Premier League.
""")

st.markdown("### 🔥2025/2026 Contenders🔥 ")
st.title("👥 Meet the Team")

# Display each person in an expandable row
for person in people:
    with st.expander(person["name"]):
        st.markdown(
            f"""
            <div style='text-align:center;'>
                <img src="{person['photo']}" width="120" style='border-radius:50%;'><br>
                <p style='font-size:0.95em;'>{person['description']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
st.markdown("""
Winner (overall) - Receives €10 from each player (apart from 2nd position)
Winner (at christmas) - Receives €5 from each player (apart from 2nd position)
winner (Each block) - Receives €2 from each player (apart from 2nd position)

Loser - FORFEIT (To be determined, potentially marathon or 24 hours in pub)
""")

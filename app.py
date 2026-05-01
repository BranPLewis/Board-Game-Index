import streamlit as st
import pandas as pd
import psycopg

# Configure page
st.set_page_config(page_title="Board Game Index", page_icon="🎲", layout="wide")

# CSS to remove whitespace at the top of the sidebar and main page
st.markdown("""
    <style>
    /* Remove padding at the top of the sidebar */
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1rem;
    }
    /* Remove padding at the top of the main container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

import os

# --- Database Connection ---
@st.cache_resource
def get_db_connection():
    # Use DATABASE_URL if provided (e.g., Railway), otherwise fallback to local DB
    db_url = os.environ.get("DATABASE_URL", "dbname=bgg user=risky host=localhost")
    return psycopg.connect(db_url)

conn = get_db_connection()

# --- Fetch Dimension Data (Cached) ---
@st.cache_data
def get_dimension_names(table_name):
    query = f"SELECT name FROM {table_name} ORDER BY name;"
    with conn.cursor() as cur:
        cur.execute(query)
        return [row[0] for row in cur.fetchall()]

try:
    mechanics_list = get_dimension_names("mechanics")
    themes_list = get_dimension_names("themes")
    categories_list = get_dimension_names("subcategories")
except Exception as e:
    st.error(f"Could not load dimensions from database. Ensure the DB is running and populated. Error: {e}")
    st.stop()

# --- Sidebar Filters ---
st.sidebar.markdown("### Filter Games")

# Reset Button directly under the title
if st.sidebar.button("Reset"):
    st.session_state.clear()
    st.rerun()

st.sidebar.markdown("---")

search_name = st.sidebar.text_input("Search by Name", key="search_name")

col1, col2 = st.sidebar.columns(2)
min_players = col1.number_input("Min Players", min_value=1, max_value=99, value=1, key="min_players")
max_players = col2.number_input("Max Players", min_value=1, max_value=99, value=99, key="max_players")

rating_range = st.sidebar.slider("Avg Rating", 0.0, 10.0, (0.0, 10.0), 0.1, key="rating_range")
weight_range = st.sidebar.slider("Game Weight (Complexity)", 0.0, 5.0, (0.0, 5.0), 0.1, key="weight_range")
year_range = st.sidebar.slider("Year Published", 1900, 2025, (1900, 2025), key="year_range")
playtime_max = st.sidebar.slider("Max Playtime (mins)", 0, 1000, 1000, 15, key="playtime_max")

selected_mechanics = st.sidebar.multiselect("Mechanics", mechanics_list, key="selected_mechanics")
selected_themes = st.sidebar.multiselect("Themes", themes_list, key="selected_themes")
selected_categories = st.sidebar.multiselect("Categories", categories_list, key="selected_categories")

st.sidebar.markdown("---")
limit = st.sidebar.selectbox("Max Results", [50, 100, 500, 1000, 5000], index=1, key="limit")

# --- Build SQL Query ---
query_base = """
SELECT 
    g.bgg_id, 
    g.name, 
    g.year_published, 
    g.avg_rating, 
    g.game_weight, 
    g.min_players, 
    g.max_players, 
    g.mfg_playtime,
    g.num_user_ratings
FROM games g
WHERE 1=1
"""
params = []

if search_name:
    query_base += " AND g.name ILIKE %s"
    params.append(f"%{search_name}%")

query_base += " AND g.min_players >= %s AND g.max_players <= %s"
params.extend([min_players, max_players])

query_base += " AND g.avg_rating >= %s AND g.avg_rating <= %s"
params.extend([rating_range[0], rating_range[1]])

query_base += " AND g.game_weight >= %s AND g.game_weight <= %s"
params.extend([weight_range[0], weight_range[1]])

query_base += " AND g.year_published >= %s AND g.year_published <= %s"
params.extend([year_range[0], year_range[1]])

query_base += " AND g.mfg_playtime <= %s"
params.append(playtime_max)

def add_dimension_filter(selected_items, join_table, dim_table, dim_pk):
    global query_base
    for item in selected_items:
        query_base += f"""
        AND EXISTS (
            SELECT 1 FROM {join_table} jt
            JOIN {dim_table} dt ON jt.{dim_pk} = dt.{dim_pk}
            WHERE jt.bgg_id = g.bgg_id AND dt.name = %s
        )
        """
        params.append(item)

add_dimension_filter(selected_mechanics, "game_mechanics", "mechanics", "mechanic_id")
add_dimension_filter(selected_themes, "game_themes", "themes", "theme_id")
add_dimension_filter(selected_categories, "game_subcategories", "subcategories", "subcategory_id")

query_base += " ORDER BY g.num_user_ratings DESC LIMIT %s"
params.append(limit)

# --- Top Page Header & Display ---
st.title("🎲 Board Game Index")

try:
    with conn.cursor() as cur:
        cur.execute(query_base, params)
        rows = cur.fetchall()
        colnames = [desc.name for desc in cur.description]
    
    df = pd.DataFrame(rows, columns=colnames)
    
    st.write(f"**Found {len(df)} games matching your criteria:**")
    
    if not df.empty:
        df['avg_rating'] = df['avg_rating'].astype(float).round(2)
        df['game_weight'] = df['game_weight'].astype(float).round(2)
        
        st.dataframe(
            df, 
            column_config={
                "bgg_id": "BGG ID",
                "name": "Game Name",
                "year_published": st.column_config.NumberColumn("Year", format="%d"),
                "avg_rating": st.column_config.NumberColumn("Avg Rating", format="⭐ %.2f"),
                "game_weight": st.column_config.NumberColumn("Complexity (1-5)", format="🧠 %.2f"),
                "min_players": "Min Play",
                "max_players": "Max Play",
                "mfg_playtime": "Time (m)",
                "num_user_ratings": st.column_config.NumberColumn("Total Ratings", format="%d")
            },
            hide_index=True,
            width='stretch',
            height=600  # Adjusted to nicely fit the screen with the sidebar layout
        )
    else:
        st.info("No games found matching these filters. Try broadening your search or click 'Reset'.")

except Exception as e:
    st.error(f"Error executing query: {e}")

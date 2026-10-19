import pandas as pd
import streamlit as st

st.title("🎵 My Album Tier List Generator")

# 1. Load data
@st.cache_data
def load_data():
    return pd.read_csv("albumratings.csv")

df = load_data()

# 2. Sidebar input to add a new album
st.sidebar.header("Add a New Album")
new_album = st.sidebar.text_input("Album Name")
new_rating = st.sidebar.slider("Rating", 1.0, 10.0, 8.0)

if st.sidebar.button("Add Album"):
    # Append new album to dataframe (and save to CSV)
    new_row = {"album": new_album, "rating": new_rating}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv("albumratings.csv", index=False)
    st.sidebar.success(f"Added {new_album}!")

# 3. Recalculate Tiers dynamically
df["Tier"] = pd.qcut(
    df["rating"], 
    q=5, 
    labels=["D Tier", "C Tier", "B Tier", "A Tier", "S Tier"]
)

# 4. Display Tiers on the main page
for tier in ["S Tier", "A Tier", "B Tier", "C Tier", "D Tier"]:
    group = df[df["Tier"] == tier]
    if not group.empty:
        min_rating = group["rating"].min()
        max_rating = group["rating"].max()
        
        st.subheader(f"{tier} (Scores: {min_rating} to {max_rating})")
        for album in group["album"]:
            st.write(f"- {album}")

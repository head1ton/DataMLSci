import ssl
import urllib.request
import certifi
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

context = ssl.create_default_context(cafile=certifi.where())

base_dir = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout='wide')

def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image specified by the given image file.

    Parameters:
        image_file (str): The path to the image file to be used as the background.

    Returns:
        None
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

back_path = os.path.join(base_dir, 'dwight-howard.jpg')
set_background(back_path)

st.title('NBA Player Stats Explorer')

st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Basketball-reference.com](https://www.basketball-reference.com/).
""")

st.sidebar.header("User Input Features")
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950, 2024))))

@st.cache_data
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    response = urllib.request.urlopen(url, context=context)
    # print(response.read())
    html = pd.read_html(response.read(), header=0)
    df = html[0]
    # df.to_csv('per_game_sample.csv')
    # raw = df.drop(df[df.Age == 'Age'].index)
    # raw = raw.fillna(0)
    # playerstats = raw.drop(['Rk'], axis=1)
    df['Player'] = df['Player'].astype(str)
    df['Team'] = df['Team'].astype(str)
    df['Pos'] = df['Pos'].astype(str)
    df['Awards'] = df['Awards'].astype(str)
    playerstats = df.drop(['Rk'], axis=1)
    return playerstats

player_stats = load_data(selected_year)
# print(player_stats.columns)
# print(player_stats.Team.unique())
sorted_unique_team = sorted(player_stats.Team.astype(str).unique())
# print(sorted_unique_team)
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

unique_pos = ['C', 'PF', 'SF', 'PG', 'SG']
selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

df_selected_team = player_stats[(player_stats.Team.isin(selected_team)) & (player_stats.Pos.isin(selected_pos))]

st.header('Display Player Stats of Selected Team(s)')
st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
st.dataframe(df_selected_team)

def fileDownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="player_stats.csv">Download CSV File</a>'
    return href

st.markdown(fileDownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('InterCorrelation Heatmap'):
    st.header('InterCorrelation Matrix Heatmap')
    df_selected_team.to_csv('output.csv', index=False)
    save_path = os.path.join(base_dir, 'output.csv')
    df = pd.read_csv(save_path)

    corr = df[['Age', 'G', 'GS', 'MP', 'FG', 'FGA', 'FG%',
       '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%',
       'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']].corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True

    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True, ax=ax)
    st.pyplot(f)

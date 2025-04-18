import os

import streamlit as st

CURRENT_THEME = "light"
IS_DARK_THEME = False
EXPANDER_TEXT = """
This is Streamlit's default *Light* theme. It should be enabled by default 🎈
If not, you can enable it in the app menu (☰ -> Settings -> Theme).
"""

base_dir = os.path.dirname(os.path.abspath(__file__))


st.set_page_config(layout='wide')

# """
#     This is Streamlit's default *Dark* theme. You can enable it in the app menu
#     (☰ -> Settings -> Theme) or by copying the following code to
#     `.streamlit/config.toml`:

#     ```python
#     [theme]
#     primaryColor="#d33682"
#     backgroundColor="#002b36"
#     secondaryBackgroundColor="#586e75"
#     textColor="#fafafa"
#     font="sans serif"
#     ```
# """

# """
# This is a custom theme. You can enable it by copying the following code
# to `.streamlit/config.toml`:

# ```python
# [theme]
# primaryColor="#d33682"
# backgroundColor="#002b36"
# secondaryBackgroundColor="#586e75"
# textColor="#fafafa"
# font="sans serif"
# ```
# """

top_image = os.path.join(base_dir, "palette.png")

st.image(top_image, width=100)

"""
# Try out Theming!

Click on the images below to view this app with different themes.
"""

""

THEMES = [
    "light",
    "dark",
    "green",
    "blue",
]
GITHUB_OWNER = "streamlit"

cols = st.columns(len(THEMES))
for col, theme in zip(cols, THEMES):
    if theme == "light":
        repo = "theming-showcase"
    else:
        repo = f"theming-showcase-{theme}"

    if theme == CURRENT_THEME:
        border_color = "red"
    else:
        border_color = "lightgrey" if IS_DARK_THEME else "black"

    col.markdown(
        f'<p align=center><a href="https://apps.streamlitusercontent.com/{GITHUB_OWNER}/{repo}/main/streamlit_app.py/+/"><img style="border: 1px solid {border_color}" alt="{theme}" src="https://raw.githubusercontent.com/{GITHUB_OWNER}/theming-showcase/main/thumbnails/{theme}.png" width=150></a></p>',
        unsafe_allow_html=True,
    )

    if theme in ["light", "dark"]:
        theme_descriptor = theme.capitalize() + " theme"
    else:
        theme_descriptor = "Custom theme"
    col.write(f"<p align=center>{theme_descriptor}</p>", unsafe_allow_html=True)

""

with st.expander("Not loading?"):
    st.write(
        "You probably played around with themes before and overrode this app's theme. Go to ☰ -> Settings -> Theme and select *Custom Theme*."
    )
with st.expander("How can I use this theme in my app?"):
    st.write(EXPANDER_TEXT)

def draw_all(key, plot=False):
    num = ['1', '2', '3', '4', '5', '6', '7', '8']
    st.write(
        """
        # Example Widgets
        
        These widgets don't do anything. But look at all the new colors they got 👀
        ```python
        # First some code.
        streamlit = "cool"
        theming = "fantastic"
        both = "💥"
        ```
        """
    )

    st.checkbox("Is this cool or what?", key=key+num[0])
    st.radio(
        "How many balloons?",
        ["1 balloon 🎈", "2 balloons 🎈🎈", "3 balloons 🎈🎈🎈"],
        key=key+num[1],
    )
    st.button("🤡 Click me", key=key+num[2])

    # if plot:
    #     st.write("Oh look, a plot:")
    #     x1 = np.random.randn(200) - 2
    #     x2 = np.random.randn(200)
    #     x3 = np.random.randn(200) + 2

    #     hist_data = [x1, x2, x3]
    #     group_labels = ["Group 1", "Group 2", "Group 3"]

    #     fig = ff.create_distplot(hist_data, group_labels, bin_size=[0.1, 0.25, 0.5])

    #     st.plotly_chart(fig, use_container_width=True)

    st.file_uploader("You can now upload with style", key=key+num[3])
    st.slider(
        "From 10 to 11, how cool are themes?", min_value=10, max_value=11,
        key=key+num[4]
    )
    # st.select_slider("Pick a number", [1, 2, 3], key=key)
    st.number_input("So many numbers", key=key+num[5])
    st.text_area("A little writing space for you :)", key=key+num[6])
    st.selectbox(
        "My favorite thing in the world is...",
        ["Streamlit", "Theming", "Baloooons 🎈 "],
        key=key+num[7],
    )
    # st.multiselect("Pick a number", [1, 2, 3], key=key)
    # st.color_picker("Colors, colors, colors", key=key)
    with st.expander("Expand me!"):
        st.write("Hey there! Nothing to see here 👀 ")
    st.write("")
    # st.write("That's our progress on theming:")
    # st.progress(0.99)
    if plot:
        st.write("And here's some data and plots")
        st.json({"data": [1, 2, 3, 4]})
        st.dataframe({"data": [1, 2, 3, 4]})
        st.table({"data": [1, 2, 3, 4]})
        st.line_chart({"data": [1, 2, 3, 4]})
        # st.help(st.write)
    st.write("This is the end. Have fun building themes!")


draw_all("main", plot=True)

with st.sidebar:
    draw_all("sidebar", plot=False)

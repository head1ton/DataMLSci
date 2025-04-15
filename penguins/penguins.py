import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os

base_dir = os.path.dirname(os.path.abspath(__file__))


from sklearn.ensemble import RandomForestClassifier

def user_input_features():
    island = st.sidebar.selectbox('Island', ('Biscoe', 'Dream', 'Torgersen'))
    sex = st.sidebar.selectbox('Sex', ('male', 'female'))
    bill_length_mm = st.sidebar.slider('Bill length (mm)', 32.1, 59.6, 43.9)
    bill_depth_mm = st.sidebar.slider('Bill depth (mm)', 13.1, 21.5, 17.2)
    flipper_length_mm = st.sidebar.slider('Flipper length (mm)', 172.0, 231.0, 201.0)
    body_mass_g = st.sidebar.slider('Body mass (g)', 2700.0, 6300.0, 4207.0)

    data = {'island': island,
            'bill_length_mm': bill_length_mm,
            'bill_depth_mm': bill_depth_mm,
            'flipper_length_mm': flipper_length_mm,
            'body_mass_g': body_mass_g,
            'sex': sex}

    features = pd.DataFrame(data, index=[0])
    return features

st.write("""
# Penguin Prediction

This app predicts the **Palmer Penguin** species!

Data obtained from the [palmerpenguins library](https://github.com/allisonhorst/palmerpenguins) in R by Allison Horst.
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
[Example CSV input file](https://raw.githubusercontent.com/head1ton/DataProfessor/refs/heads/main/penguins/penguins_example.csv)
""")

uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
else:
    input_df = user_input_features()

csv_path = os.path.join(base_dir, 'penguins_cleaned.csv')
penguins_raw = pd.read_csv(csv_path)
penguins = penguins_raw.drop(columns=['species'])
df = pd.concat([input_df, penguins], axis=0)

# https://www.kaggle.com/pratik1120/penguin-dataset-eda-classification-and-clustering
encode = ['sex', 'island']
for col in encode:
    dummy = pd.get_dummies(df[col], prefix=col)
    df = pd.concat([df, dummy], axis=1)
    del df[col]

df = df[:1]
# print(df.columns)
st.subheader('User Input features')

if uploaded_file is not None:
    st.write(df)
else:
    st.write('Awaiting CSV file to be uploaded. Currently using example input parameters (shown below).')
    st.write(df)

model_path = os.path.join(base_dir, 'penguins_clf.pkl')
load_clf = pickle.load(open(model_path, 'rb'))

prediction = load_clf.predict(df)
prediction_proba = load_clf.predict_proba(df)

penguins_species = np.array(['Adelie', 'Chinstrap', 'Gentoo'])

st.subheader('Class Name')
st.write(penguins_species)


st.subheader('Prediction')
st.write(penguins_species[prediction])

st.subheader('Prediction Probability')
st.write(prediction_proba)

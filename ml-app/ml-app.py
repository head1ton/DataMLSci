import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing, load_diabetes

st.set_page_config(page_title='The Machine Learning App', layout='wide')

def build_model(df):
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=(100-split_size) / 100)

    st.markdown('**1.2. Data splits**')
    st.write('Training set')
    st.info(X_train.shape)
    st.write('Test set')
    st.info(X_test.shape)

    st.markdown('**1.3. Variable details**')
    st.write('X variable')
    st.info(list(X.columns))
    st.write('Y variable')
    st.info(y.name)

    rf = RandomForestRegressor(n_estimators=parameter_n_estimators,
                               random_state=parameter_random_state,
                               max_features=parameter_max_features,
                               criterion=parameter_criterion,
                               min_samples_split=parameter_min_samples_split,
                               min_samples_leaf=parameter_min_samples_leaf,
                               bootstrap=parameter_bootstrap,
                               oob_score=parameter_oob_score,
                               n_jobs=parameter_n_jobs)
    rf.fit(X_train, Y_train)

    st.subheader('2. Model Performance')

    st.markdown('**2.1. Training set**')
    Y_pred_train = rf.predict(X_train)
    st.write('Coefficient of determination ($R^2$):')
    st.info(r2_score(Y_train, Y_pred_train))

    st.write('Error (squared_error or absolute_error):')
    st.info(mean_squared_error(Y_train, Y_pred_train))

    st.markdown('**2.2. Test set**')
    Y_pred_test = rf.predict(X_test)
    st.write('Coefficient of determination ($R^2$):')
    st.info(r2_score(Y_test, Y_pred_test))

    st.write('Error (squared_error or absolute_error):')
    st.info(mean_squared_error(Y_test, Y_pred_test))

    st.subheader('3. Model Parameters')
    st.write(rf.get_params())

st.write("""
# The Machine Learning

In this implementation, the *<span style="color:red;">RandomForestRegressor()</span>* function is used in this app for build a regression model using the **Random Forest** algorithm.

Try adjusting the hyperparameters!
""", unsafe_allow_html=True)

with st.sidebar.header('1. Upload your CSV data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])
    st.sidebar.markdown("""
    [Example CSV input file](https://raw.githubusercontent.com/head1ton/DataMLSci/refs/heads/main/solubility/delaney_solubility_with_descriptors.csv)
    """)

with st.sidebar.header('2. Set Parameers'):
    split_size = st.sidebar.slider('Data split ratio (% for Training Set)', 10, 90, 80, 5)

with st.sidebar.subheader('2.1. Learning Parameters'):
    parameter_n_estimators = st.sidebar.slider('Number of estimators (n_estimators)', 0, 1000, 100, 100)
    parameter_max_features = st.sidebar.select_slider('Max features (max_features)', options=['sqrt', 'log2', None])
    parameter_min_samples_split = st.sidebar.slider('Minimum number of samples required to split an internal node (min_samples_split)', 1, 10, 2, 1)
    parameter_min_samples_leaf = st.sidebar.slider('Minimum number of samples required to be at a leaf node (min_samples_leaf)', 1, 10, 2, 1)

with st.sidebar.subheader('2.2. General Parameters'):
    parameter_random_state = st.sidebar.slider('Seed number (random_state)', 0, 1000, 42, 1)
    parameter_criterion = st.sidebar.select_slider('Performance measure (criterion)', options=['squared_error', 'absolute_error'])
    parameter_bootstrap = st.sidebar.select_slider('Bootstrap samples when building trees (bootstrap)', options=[True, False])
    parameter_oob_score = st.sidebar.select_slider('Whether to use out-of-bag sample to estimate the R^2 on unseen data (oob_score)', options=[False, True])
    parameter_n_jobs = st.sidebar.select_slider('Number of jobs to run in parallel (n_jobs)', options=[1, -1])

st.subheader('1. Dataset')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df)

    with st.spinner("Wait for it...", show_time=True):
        build_model(df)
else:
    st.info('Awaiting for CSV file to be uploaded.')
    if st.button('Press to use Example Dataset'):
        ## Diabetes dataset
        # diabetes = load_diabetes()
        # X = pd.DataFrame(diabetes.data, columns=diabetes.feature_names)
        # y = pd.Series(diabetes.target, name='response')
        # df = pd.concat([X, y], axis=1)
        #
        # st.markdown('The Diabetes dataset is used as the example.')
        # st.write(df.head(5))

        ## California housing dataset
        X, y = fetch_california_housing(return_X_y=True, as_frame=True)
        # n_samples, n_features = X.shape
        df = pd.concat([X, y], axis=1)
        # print(df.head())
        st.markdown('The California housing dataset is used as the example.')
        st.write(df.head(5))

        with st.spinner("Wait for it...", show_time=True):
            build_model(df)

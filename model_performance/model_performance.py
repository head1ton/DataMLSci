import base64
import os.path

import pandas as pd
import streamlit as st
from PIL import Image
from sklearn.metrics import accuracy_score, balanced_accuracy_score, \
    precision_score, recall_score, matthews_corrcoef, f1_score, \
    cohen_kappa_score
from sklearn.metrics import confusion_matrix

st.set_page_config(layout='wide')

base_dir = os.path.dirname(os.path.abspath(__file__))

st.sidebar.header('Input panel')
st.sidebar.markdown("""
[Example CSV file](https://raw.githubusercontent.com/head1ton/DataMLSci/refs/heads/main/model_performance/Y_example.csv)
""")

uploaded_file = st.sidebar.file_uploader('Upload your input CSV file', type=['csv'])

performance_metrics = ['Accuracy', 'Balanced_Accuracy', 'Precision', 'Recall', 'MCC', 'F1', 'Cohen_Kappa']
selected_metrics = st.sidebar.multiselect('Performance metrics', performance_metrics, performance_metrics)

image = Image.open(os.path.join(base_dir, 'roc-curve.png'))
st.image(image, width=500)
st.title('Model Performance Calculator')
st.markdown("""
This app calculates the model performance metrics given the actual and predicted values.
* **Python libraries:** `base64`, `pandas`, `streamlit`, `scikit-learn`
""")

def calc_confusion_matrix(input_data):
    Y_actual = input_data.iloc[:, 0]
    Y_predicted = input_data.iloc[:, 1]
    confusion_matrix_array = confusion_matrix(Y_actual, Y_predicted)
    confusion_matrix_df = pd.DataFrame(confusion_matrix_array, columns=['Actual', 'Predicted'], index=['Actual', 'Predicted'])
    return confusion_matrix_df

def calc_metrics(input_data):
    Y_actual = input_data.iloc[:, 0]
    Y_predicted = input_data.iloc[:, 1]
    acc = accuracy_score(Y_actual, Y_predicted)
    balanced_accuracy = balanced_accuracy_score(Y_actual, Y_predicted)
    precision = precision_score(Y_actual, Y_predicted, average='weighted')
    recall = recall_score(Y_actual, Y_predicted, average='weighted')
    mcc = matthews_corrcoef(Y_actual, Y_predicted)
    f1 = f1_score(Y_actual, Y_predicted, average='weighted')
    cohen_kappa = cohen_kappa_score(Y_actual, Y_predicted)

    acc_series = pd.Series([acc], name='Accuracy')
    balanced_accuracy_series = pd.Series([balanced_accuracy], name='Balanced_Accuracy')
    precision_series = pd.Series(precision, name='Precision')
    recall_series = pd.Series(recall, name='Recall')
    mcc_series = pd.Series(mcc, name='MCC')
    f1_series = pd.Series(f1, name='F1')
    cohen_kappa_series = pd.Series(cohen_kappa, name='Cohen_Kappa')

    df = pd.concat([acc_series, balanced_accuracy_series, precision_series, recall_series, mcc_series, f1_series, cohen_kappa_series], axis=1)

    return df

def load_example_data():
    df = pd.read_csv(os.path.join(base_dir, 'Y_example.csv'))
    return df

def fileDownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="metrics.csv">Download CSV File</a>'
    return href

if uploaded_file is not None:
    input_df = pd.read_csv(uploaded_file)
    confusion_matrix_df = calc_confusion_matrix(input_df)
    metrics_df = calc_metrics(input_df)
    selected_metrics_df = metrics_df[selected_metrics]

    st.header('Input data')
    st.write(input_df)
    st.header('Confusion matrix')
    st.write(confusion_matrix_df)
    st.header('Performance metrics')
    st.write(selected_metrics_df)
    st.markdown(fileDownload(selected_metrics_df), unsafe_allow_html=True)
else:
    st.info('Awaiting the upload of the input file.')
    if st.button('Use Example Data'):
        input_df = load_example_data()
        confusion_matrix_df = calc_confusion_matrix(input_df)
        metrics_df = calc_metrics(input_df)
        selected_metrics_df = metrics_df[selected_metrics]

        st.header('Input data')
        st.write(input_df)
        st.header('Confusion matrix')
        st.write(confusion_matrix_df)
        st.header('Performance metrics')
        st.write(selected_metrics_df)
        st.markdown(fileDownload(selected_metrics_df), unsafe_allow_html=True)



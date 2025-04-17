import base64
import zipfile

import pandas as pd
import streamlit as st

st.set_page_config(layout='wide')

st.markdown("""
# **Excel File Merge**

This is the **Excel File Merge** created in Python using Streamlit library.
""")

with st.sidebar.header('1. Upload your Zip file'):
    uploaded_file = st.sidebar.file_uploader("Excel-containing Zip file", type=["zip"])
    st.sidebar.markdown("""
    [Example Zip input file](https://github.com/head1ton/DataProfessor/excel-file/raw/main/nba_data.zip)
    """)

def excel_file_merge(zip_file_name):
    df = pd.DataFrame()
    archieve = zipfile.ZipFile(zip_file_name, 'r')
    with zipfile.ZipFile(zip_file_name, "r") as f:
        for file in f.namelist():
            xlfile = archieve.open(file)
            if file.endswith('.xlsx'):
                df_xl = pd.read_excel(xlfile, engine='openpyxl')
                df_xl['Note'] = file
                df = pd.concat([df, df_xl], ignore_index=True)

    df = df.sort_values(by='Note', ascending=True)
    return df

def fileDownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="merged_file.csv">Download Merged File as CSV</a>'
    return href

def xlDownload(df):
    df.to_excel("data.xlsx", index=False)
    data = open("data.xlsx", "rb").read()
    b64 = base64.b64encode(data).decode('UTF-8')
    # b64 = base64.b64encode(xl.encode()).decode()
    href = f'<a href="data:file/xls;base64,{b64}" download="merged_file.xlsx">Download Merged File as XLSX</a>'
    return href

if st.sidebar.button('Submit'):
    df = excel_file_merge(uploaded_file)
    st.header('**Merged data**')
    st.write(df)
    st.markdown(fileDownload(df), unsafe_allow_html=True)
    st.markdown(xlDownload(df), unsafe_allow_html=True)
else:
    st.info('Awaiting for Zip file to be uploaded.')
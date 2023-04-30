import streamlit as st
import requests 
import pandas as pd
import csv
import base64
from io import StringIO

# read a data from github repositry. This data is updated daily.
url = 'https://api.github.com/repos/satoshi-sh/baseball-git-scraper/contents/data/central.csv'
response = requests.get(url)

if response.status_code == 200:
    response_json = response.json()
    file_contents = base64.b64decode(response_json['content']).decode('utf-8')
    df = pd.read_csv(StringIO(file_contents))
    # Display the original DataFrame
    st.dataframe(df)

    # Add a sidebar for filtering
    sidebar = st.sidebar

    # Get a list of all the columns in the DataFrame
    columns = df['チーム名'].unique()
    # Add a multiselect widget to the sidebar with all the column names
    selected_columns = sidebar.multiselect("Select Teams to display", columns)

    # Filter the DataFrame based on the selected columns
    filtered_df = df[df['チーム名'].isin(selected_columns)]
    # Display the filtered DataFrame
    st.dataframe(filtered_df)

else:
    print('Error:', response.status_code)




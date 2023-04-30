import streamlit as st
import requests 
import pandas as pd
import base64
from io import StringIO
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter
import japanize_matplotlib
matplotlib.rcParams['text.usetex'] = False

# read a data from github repositry. This data is updated daily.
url = 'https://api.github.com/repos/satoshi-sh/baseball-git-scraper/contents/data/central.csv'
@st.cache_data
def get_data(url):
   response = requests.get(url)
   return response
response = get_data(url)
if response.status_code == 200:
    response_json = response.json()
    file_contents = base64.b64decode(response_json['content']).decode('utf-8')
    df = pd.read_csv(StringIO(file_contents))
    df['date'] = pd.to_datetime(df['date'])
    # Display the original DataFrame
    st.dataframe(df.tail(6))

    # Add a sidebar for filtering
    sidebar = st.sidebar

    # Get a list of all the columns in the DataFrame
    teams = df['チーム名'].unique()
    columns = df.columns[2:-1]
    # Add a multiselect widget to the sidebar with all the column names
    selected_values = sidebar.multiselect("Select Teams to display", teams)

    # Add a multiselect widget to the sidebar with all the column names
    selected_columns = sidebar.selectbox("Select column to display", columns)


    # Filter the DataFrame based on the selected columns
    filtered_df = df[df['チーム名'].isin(selected_values)]
    # Display the filtered DataFrame
    st.dataframe(filtered_df)

    # show line plot 
    if len(selected_values)>0:
        # define color for each hue category
        colors = {'DeNA': 'blue', '阪神': 'yellow', 'ヤクルト': 'purple','広島':'red','巨人':'orange','中日':'black'}
        show_column = selected_columns or '勝率'
        fig,ax = plt.subplots()
        sns.lineplot(filtered_df,x='date',y=show_column, hue='チーム名',ax=ax,palette=colors)

        # Format x-axis date labels
        date_form = DateFormatter("%m/%d")
        ax.xaxis.set_major_formatter(date_form)
        plt.xticks(rotation=45)
                
        st.pyplot(fig)

else:
    print('Error:', response.status_code, response.json()['message'])




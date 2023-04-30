import streamlit as st
import pandas as pd
import base64

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.dates import DateFormatter
import japanize_matplotlib

matplotlib.rcParams['text.usetex'] = False


df = pd.read_csv('./data/central.csv')
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






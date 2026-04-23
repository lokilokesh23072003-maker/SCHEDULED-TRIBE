import streamlit as st
import pandas as pd

# Re-load the DataFrame from the original Excel file since the kernel state shows df is empty
df = pd.read_excel("scheduled_tribes_aba.xlsx.xlsx")

# Re-process the Year column as done previously
df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)

# Define the correct expenditure column name
expenditure_column = 'Expenditure Incurred (UOM:INR(IndianRupees)), Scaling Factor:10000000'

st.title("DAPST Expenditure Analysis")

# Ensure only unique years are shown in the selectbox
year_options = sorted(df['Year'].unique())
year = st.selectbox("Select Year", year_options)

filtered_df = df[df['Year'] == year]

st.write(f"### Data for Year: {year}")
st.dataframe(filtered_df)

# Ensure the data for line chart is prepared correctly
# Aggregate expenditure by year for the line chart
expenditure_by_year = df.groupby('Year')[expenditure_column].sum().reset_index()

# Rename the column to an Altair-friendly name for plotting
expenditure_by_year.rename(columns={expenditure_column: 'Total Expenditure'}, inplace=True);
expenditure_by_year = expenditure_by_year.sort_values('Year')

st.write("### Total Expenditure Trend Over Years")
st.line_chart(expenditure_by_year.set_index('Year')['Total Expenditure'])

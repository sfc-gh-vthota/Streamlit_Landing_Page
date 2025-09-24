# Simple Data Explorer - Streamlit App
# Shows sample data with basic filtering and display options

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# Snowflake connector
from snowflake.snowpark.context import get_active_session

# Initialize connection
@st.cache_resource
def init_connection():
    return get_active_session()

def generate_sample_data():
    """Generate some sample data for demonstration"""
    # Sample sales data
    data = []
    regions = ['North', 'South', 'East', 'West']
    products = ['Widget A', 'Widget B', 'Gadget X', 'Gadget Y', 'Tool Z']
    
    for i in range(50):
        data.append({
            'Date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'Region': random.choice(regions),
            'Product': random.choice(products),
            'Sales': random.randint(100, 1000),
            'Quantity': random.randint(1, 20)
        })
    
    return pd.DataFrame(data)

def main():
    st.title("📊 Simple Data Explorer")
    st.caption("Explore sample sales data with basic filtering")
    
    # Generate sample data
    df = generate_sample_data()
    
    st.subheader("Data Overview")
    st.write(f"Total records: {len(df)}")
    
    # Simple filters
    col1, col2 = st.columns(2)
    
    with col1:
        selected_region = st.selectbox(
            "Filter by Region",
            options=['All'] + sorted(df['Region'].unique().tolist())
        )
    
    with col2:
        selected_product = st.selectbox(
            "Filter by Product", 
            options=['All'] + sorted(df['Product'].unique().tolist())
        )
    
    # Apply filters
    filtered_df = df.copy()
    if selected_region != 'All':
        filtered_df = filtered_df[filtered_df['Region'] == selected_region]
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
    
    # Display results
    st.subheader("Filtered Data")
    st.dataframe(filtered_df, use_container_width=True)
    
    # Simple metrics
    if not filtered_df.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Sales", f"${filtered_df['Sales'].sum():,}")
        
        with col2:
            st.metric("Total Quantity", f"{filtered_df['Quantity'].sum()}")
        
        with col3:
            st.metric("Avg Sale", f"${filtered_df['Sales'].mean():.0f}")

if __name__ == "__main__":
    main()




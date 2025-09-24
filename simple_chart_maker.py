# Simple Chart Maker - Streamlit App
# Create basic charts from sample data

import streamlit as st
import pandas as pd
import random

# Snowflake connector
from snowflake.snowpark.context import get_active_session

# Initialize connection
@st.cache_resource
def init_connection():
    return get_active_session()

def generate_chart_data(chart_type):
    """Generate appropriate sample data for different chart types"""
    
    if chart_type == "Bar Chart":
        categories = ['A', 'B', 'C', 'D', 'E']
        values = [random.randint(10, 100) for _ in categories]
        return pd.DataFrame({'Category': categories, 'Value': values})
    
    elif chart_type == "Line Chart":
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        values = [random.randint(20, 80) for _ in months]
        return pd.DataFrame({'Month': months, 'Sales': values})
    
    elif chart_type == "Area Chart":
        days = [f'Day {i}' for i in range(1, 8)]
        values = [random.randint(30, 90) for _ in days]
        return pd.DataFrame({'Day': days, 'Traffic': values})

def main():
    st.title("📈 Simple Chart Maker")
    st.caption("Create basic charts with sample data")
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Chart Type",
        options=["Bar Chart", "Line Chart", "Area Chart"]
    )
    
    # Generate data for selected chart type
    data = generate_chart_data(chart_type)
    
    st.subheader(f"Sample Data for {chart_type}")
    st.dataframe(data, use_container_width=True)
    
    # Create and display the chart
    st.subheader(f"Generated {chart_type}")
    
    if chart_type == "Bar Chart":
        st.bar_chart(data.set_index('Category')['Value'])
        
    elif chart_type == "Line Chart":
        st.line_chart(data.set_index('Month')['Sales'])
        
    elif chart_type == "Area Chart":
        st.area_chart(data.set_index('Day')['Traffic'])
    
    # Chart customization options
    st.subheader("Chart Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        show_data_values = st.checkbox("Show Data Values", value=True)
        
    with col2:
        use_custom_colors = st.checkbox("Use Custom Colors", value=False)
    
    if show_data_values:
        st.write("**Data Summary:**")
        if chart_type == "Bar Chart":
            st.write(f"• Highest: {data['Value'].max()} (Category {data.loc[data['Value'].idxmax(), 'Category']})")
            st.write(f"• Lowest: {data['Value'].min()} (Category {data.loc[data['Value'].idxmin(), 'Category']})")
            st.write(f"• Average: {data['Value'].mean():.1f}")
            
        elif chart_type == "Line Chart":
            st.write(f"• Peak Sales: {data['Sales'].max()} ({data.loc[data['Sales'].idxmax(), 'Month']})")
            st.write(f"• Lowest Sales: {data['Sales'].min()} ({data.loc[data['Sales'].idxmin(), 'Month']})")
            st.write(f"• Average: {data['Sales'].mean():.1f}")
            
        elif chart_type == "Area Chart":
            st.write(f"• Peak Traffic: {data['Traffic'].max()} ({data.loc[data['Traffic'].idxmax(), 'Day']})")
            st.write(f"• Lowest Traffic: {data['Traffic'].min()} ({data.loc[data['Traffic'].idxmin(), 'Day']})")
            st.write(f"• Average: {data['Traffic'].mean():.1f}")
    
    # Generate new data button
    if st.button("Generate New Data", type="primary"):
        st.rerun()

if __name__ == "__main__":
    main()



